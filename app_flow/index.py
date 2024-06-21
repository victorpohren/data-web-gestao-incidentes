from utils.data_extraction import *
from _controllers import controllers
from _tables import navTables

import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np

from app import app

# Check pipe de tratativas e central de projetos (em desligamento x tratativa concluída )

# -------------- Layout Dash ------------- #

app.layout = dbc.Container(
        children=[
                dbc.Row([
                        dbc.Col([controllers], md = 3, style = {"padding":"0px 0px 20px 0px","height":"120vh"}),
                        dbc.Col([navTables], md = 9, style= {"background-color": "#F2F2F2", "padding":"0px 0px 20px 0px"})
                ]),
                html.Footer(
                        html.P("Victor Pohren @2023 - Todos os direitos reservados", style={"padding": "30px 30px 30px 30px", "color": "#A8A9AA", 'margin':'0px 0px 0px 0px'})
                , style={"text-align": "center", "background-color":"#303030"})

        ], fluid=True)



# -------------- Callbacks ------------- #
@app.callback(
    [Output('check_tratativas','children'),
    Output('check_vendas_sales','children'),
    Output('check_vendas_pipe','children'),
    Output('check_franqueado','children'),
    Output('check_cliente','children'),
    Output('check_inicio','children'),
    Output('check_tratativas_franquias','children'),
    Output('check_upsell_downsell','children'),
    Output('check_dups','children'),
    Output('check_fee','children'),
    Output('check_data_fim','children'),
    Output('check_finalizacao','children'),
    Output('check_tipo_churn','children'),
    Output('check_tratativa_central_id','children'),
    Output('check_up_down','children'),
    Output('check_tabelas','children'),
    Output('check_data_fim_projeto','children')],
    Input('pesquisar','n_clicks'),
    prevent_initial_call = True
)
def checkTratativas(n_clicks):
    # Dataframe de tratativas concluídas
    dft = pd.DataFrame(pullFromSqlServerTratativas())

    # Dataframe de projetos
    dfp = pd.DataFrame(pullFromSqlServerProjetos())

    # Dataframe Sales
    dfs = pd.DataFrame(pullFromSqlServerSalesForce())

    # Dataframe Sales
    dfv = pd.DataFrame(pullFromSqlServerPipeVendas())


    dfd = dfp[dfp['current_phase'] == 'Em desligamento']

    dfd.rename(columns={'id':'projeto_central_id'}, inplace=True)

    dfud = pd.DataFrame(pullFromSqlServerPipeUpsellDownsell())

    dftf = pd.DataFrame(pullFromSqlServerTratativasFranquias())

    dftblank = pd.DataFrame(pullFromSqlServerTratativasIDCentralBlank())

    df_updown = pd.DataFrame(pullFromSqlServerRequisicaoUpsell())

    df_tabelas = pd.DataFrame(pullFromSqlServerAtualizacaoTabelas())

    df_dt_fim_projeto = pd.DataFrame(pullFromSqlServerDtFimProjeto())
    #------------------- Dataframe combinando cards em desligamento com tratativa concluída---------------------------------------------------
    dfcombine = dfd.merge(dft, how='inner', on='projeto_central_id')
    cards_concluidos = list(dft['projeto_central_id'])
    results = dfcombine[dfcombine['projeto_central_id'].isin(cards_concluidos)][['projeto_central_id','title_x','card_id']]
    results.rename(columns = {"title_x":"Projeto","card_id":"Tratativa","projeto_central_id":"Central"},inplace=True)
    #results.to_csv('tratativas.csv')
    # Formatação de link clicável do card
    for i in range(0,len(results)):    
        results.iloc[i,0] = "[Projeto](https://app.pipefy.com/open-cards/"+str(results.iloc[i,0])+")"
        results.iloc[i,2] = "[Tratativa](https://app.pipefy.com/open-cards/"+str(results.iloc[i,2])+")"
    
    fig_tabela_tratativas = html.Div([
                html.Label("Tratativas Concluídas Em Desligamento", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'height':'20px','maxWidth':'7vw', 'minWidth':'4vw'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'7vw',
                        'maxWidth':'12vw'
                }]
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                , markdown_options={"html": True}
                )
        ])
   #------------------- Dataframe campos em branco central de projetos ---------------------------------------------------
    dfp.replace('nan',np.nan,inplace=True)
    dfp.replace('NULL',np.nan,inplace=True)
    dfp.replace('None',np.nan,inplace=True)
    dfp.replace('none',np.nan,inplace=True)
    dfp.cliente_database.replace(['[]','["testefevereiro"]','["teste"]','["teste "]'],np.nan,inplace=True)
    dfp.responsavel_pelo_projeto_database.replace(['[]','["Teste da Silva"]'],np.nan,inplace=True)
    dfp.inicio_do_projeto.replace(['None'],np.nan,inplace=True)

    Projeto_Sem_Franqueado = list(dfp.loc[(dfp['responsavel_pelo_projeto_database'].isnull())]['id'])
    
    Projeto_Sem_Cliente_DB = list(dfp.loc[(dfp['cliente_database'].isnull())]['id'])

    Projeto_Sem_Fee = list(dfp.loc[(dfp['valor_do_deal'].isnull())]['id'])

    Projeto_Sem_Inicio = list(dfp.loc[(dfp['inicio_do_projeto'].isnull())]['id'])
    
    Churn_WORST = ['Concluído', 'Em desligamento', '[TEMPORARIO] Transições Antigas','Pausado'] 

    Churn_Sem_Data_Fim = list(dfp.loc[(dfp['current_phase'].isin(Churn_WORST)) & (dfp['data_fim_do_projeto'].isnull() & (dfp['tipo_de_finalizacao']!="Escopo Fechado"))]['id'])

    Churn_Consolidado = ['Concluído', '[TEMPORARIO] Transições Antigas'] 

    Churn_Sem_Finalizacao = list(dfp.loc[(dfp['current_phase'].isin(Churn_Consolidado)) & (dfp['tipo_de_finalizacao'].isnull())]['id'])

    Churn_Sem_Tipo = list(dfp.loc[(dfp['current_phase'].isin(Churn_Consolidado)) & (dfp['tipo_de_churn'].isnull() & (dfp['tipo_de_finalizacao']!="Escopo Fechado"))]['id'])

    Id_Errors = np.unique(Projeto_Sem_Franqueado + Projeto_Sem_Cliente_DB + Projeto_Sem_Inicio + Projeto_Sem_Fee + Churn_Sem_Data_Fim + Churn_Sem_Finalizacao + Churn_Sem_Tipo )

    results_2 = dfp[['id','title']]
    results_2 = results_2[dfp['id'].isin(Id_Errors)].reset_index(drop=True)
    error_columns = ['Sem_Franqueado_DB','Sem_Cliente_DB','Sem_Inicio','Sem_Fee','Churn_Sem_Data_Fim','Churn_Sem_Finalizacao','Churn_Sem_Tipo']
    results_2[error_columns]=0

    for i in range(0,len(results_2)):
        if results_2.iloc[i,0] in Projeto_Sem_Franqueado:
            results_2.iloc[i,2] = 1
        if results_2.iloc[i,0] in Projeto_Sem_Cliente_DB:
            results_2.iloc[i,3] = 1
        if results_2.iloc[i,0] in Projeto_Sem_Inicio:
            results_2.iloc[i,4] = 1
        if results_2.iloc[i,0] in Projeto_Sem_Fee:
            results_2.iloc[i,5] = 1
        if results_2.iloc[i,0] in Churn_Sem_Data_Fim:
            results_2.iloc[i,6] = 1
        if results_2.iloc[i,0] in Churn_Sem_Finalizacao:
            results_2.iloc[i,7] = 1
        if results_2.iloc[i,0] in Churn_Sem_Tipo:
            results_2.iloc[i,8] = 1       
   
    for i in range(0,len(results_2)):    
        results_2.iloc[i,0] = "[Projeto](https://app.pipefy.com/open-cards/"+str(results_2.iloc[i,0])+")"
    
    results_2.rename(columns = {"id":"Central","title":"Projeto"},inplace=True)
    results_Sem_Franqueado = results_2[results_2.Sem_Franqueado_DB == 1][['Central','Projeto']]
    results_Sem_Cliente_DB = results_2[results_2.Sem_Cliente_DB == 1][['Central','Projeto']]    
    results_Sem_Inicio = results_2[results_2.Sem_Inicio == 1][['Central','Projeto']]    
    results_Sem_Fee = results_2[results_2.Sem_Fee == 1][['Central','Projeto']]    
    results_Churn_Sem_Data_Fim = results_2[results_2.Churn_Sem_Data_Fim == 1][['Central','Projeto']]    
    results_Churn_Sem_Finalizacao = results_2[results_2.Churn_Sem_Finalizacao == 1][['Central','Projeto']]    
    results_Churn_Sem_Tipo = results_2[results_2.Churn_Sem_Tipo == 1][['Central','Projeto']]    
        
    fig_tabela_sem_franqueado = html.Div([
                html.Label("Projetos Sem Franqueado DB", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Sem_Franqueado.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Sem_Franqueado.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'15vw',
                        'maxWidth':'15vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_cliente_db = html.Div([
                html.Label("Projetos Sem Cliente DB", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Sem_Cliente_DB.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Sem_Cliente_DB.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'15vw',
                        'maxWidth':'15vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_inicio = html.Div([
                html.Label("Projetos Sem Data de Inicio", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Sem_Inicio.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Sem_Inicio.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'15vw',
                        'maxWidth':'15vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_fee = html.Div([
                html.Label("Projetos Sem Valor do Deal", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Sem_Fee.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Sem_Fee.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'15vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'9vw',
                        'maxWidth':'9vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_data_fim = html.Div([
                html.Label("Concluídos Sem Data Fim", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Churn_Sem_Data_Fim.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Churn_Sem_Data_Fim.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'15vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}                
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'9vw',
                        'maxWidth':'9vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_finalizacao = html.Div([
                html.Label("Concluídos sem Tipo de Finalização", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Churn_Sem_Finalizacao.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Churn_Sem_Finalizacao.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'15vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'9vw',
                        'maxWidth':'9vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

    fig_tabela_sem_tipo = html.Div([
                html.Label("Concluídos Sem Tipo de Churn", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_Churn_Sem_Tipo.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_Churn_Sem_Tipo.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'15vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'8vw',
                        'maxWidth':'8vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])


   #------------------- Dataframe vendas Salesforce sem contrato na central ---------------------------------------------------
    dfs.rename(columns = {"id":"Venda","company":"Empresa"},inplace=True)

    for i in range(0,len(dfs)):    
        dfs.iloc[i,0] = "[Salesforce](https://v4company.lightning.force.com/lightning/r/Opportunity/"+str(dfs.iloc[i,0])+"/view?ws=%2Flightning%2Fr%2FAccount%2F0018c00002ZvCDnAAN%2Fview)"

        
    fig_vendas_nao_criadas_sales = html.Div([
                html.Label("[Sales Force] Ganhos Não Encontradas na Central", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(dfs.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in dfs.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11,"dimension": "ratio"}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'center', 'height':'20px','maxWidth':'12vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Empresa'},
                        'textAlign': 'center',
                        'minWidth':'14vw',
                        'maxWidth':'14vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])

   #------------------- Dataframe vendas pipefy sem cnpj na central ---------------------------------------------------
    dfv.rename(columns = {"card_id":"Venda","title":"Empresa"},inplace=True)

    for i in range(0,len(dfv)): 
        dfv.iloc[i,0] = "[Pipefy](https://app.pipefy.com/open-cards/"+str(dfv.iloc[i,0])+")"

    fig_vendas_nao_criadas_pipe = html.Div([
                html.Label("[Pipefy] Ganhos Não Encontradas na Central", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(dfv.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in dfv.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11,"dimension": "ratio"}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}                
                , style_cell = {'textAlign':'center', 'height':'20px','maxWidth':'12vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Empresa'},
                        'textAlign': 'center',
                        'minWidth':'14vw',
                        'maxWidth':'14vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])
 
#------------------- Dataframe tratativa franquia nao criada no 2.4 ---------------------------------------------------

   
    for i in range(0,len(dftf)):    
        dftf.iloc[i,0] = "[Tratativa](https://app.pipefy.com/open-cards/"+str(dftf.iloc[i,0])+")"
    
    dftf.rename(columns = {"card_id":"Tratativa Franquia","title":"Projeto"},inplace=True)
        
    fig_tabela_tratativa_franquia = html.Div([
                html.Label("Tratativas Franquia Não Criadas na Recuperação", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(dftf.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in dftf.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'8vw',
                        'maxWidth':'13vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])
    
#------------------- Dataframe id card central em branco upsell e downsell ---------------------------------------------------

   
    for i in range(0,len(dfud)):    
        dfud.iloc[i,0] = "[Projeto](https://app.pipefy.com/open-cards/"+str(dfud.iloc[i,0])+")"
    
    dfud.rename(columns = {"card_id":"Upsell/Downsell","title":"Projeto"},inplace=True)
        
    fig_tabela_sem_id_central = html.Div([
                html.Label("Upsell/Downsell Sem Id Card Central", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(dfud.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in dfud.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'15vw',
                        'maxWidth':'15vw'
                }]  
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])
    

   #------------------- Dataframe contratos duplicados na central ---------------------------------------------------
    opp_duplicados = dfp[dfp.id_opp_sales_force.notna()]
    opp_duplicados = opp_duplicados[opp_duplicados.id_opp_sales_force.duplicated(keep=False)].id_opp_sales_force.unique()
    df_dups = dfp[['id','title','contract_id']]
    df_dups['opp_duplicado'] = 0

    for i in range(0,len(df_dups)):
            if df_dups.iloc[i,2] in opp_duplicados :
                df_dups.iloc[i,3]=1

    results_5 = df_dups[df_dups.opp_duplicado == 1][['id','title','contract_id']].sort_values(by='title')
    results_5.rename(columns = {"card_id":"Venda","title":"Projeto","id_opp_sales_force":"ID Opp"},inplace=True)

    for i in range(0,len(results_5)): 
        results_5.iloc[i,0] = "[Projeto](https://app.pipefy.com/open-cards/"+str(results_5.iloc[i,0])+")"

    fig_duplicados_id_contrato = html.Div([
                html.Label("ID Opps Duplicados na Central", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(results_5.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in results_5.columns]
                , style_table={'height': '33vh', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px', 'width':'21vw','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11,"dimension": "ratio"}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}                
                , style_cell = {'textAlign':'center', 'height':'20px','maxWidth':'250px', 'minWidth':'100px', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'8vw',
                        'maxWidth':'8vw'
                }] 
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])
    
#------------------- Dataframe id card central em branco tratativa ---------------------------------------------------

   
    for i in range(0,len(dftblank)):    
        dftblank.iloc[i,0] = "[Tratativa](https://app.pipefy.com/open-cards/"+str(dftblank.iloc[i,0])+")"
    
    dftblank.rename(columns = {"card_id":"Tratativa","title":"Projeto"},inplace=True)
        
    fig_tabela_tratativa_sem_id_central = html.Div([
                html.Label("Trativas sem Id Central", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(dftblank.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in dftblank.columns]
                , style_table={'height': '33vh', 'width':'15vw', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'8vw',
                        'maxWidth':'13vw'
                }]  
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])  
    
#------------------- Dataframe requisicao up/down não criada no pipe ---------------------------------------------------

   
    for i in range(0,len(df_updown)):    
        df_updown.iloc[i,0] = "[Requisição](https://app.pipefy.com/open-cards/"+str(df_updown.iloc[i,0])+")"
    
    df_updown.rename(columns = {"card_id":"Requisição","title":"Projeto"},inplace=True)
        
    fig_tabela_requisicao_up_down = html.Div([
                html.Label("Requisição de Upsell e Downsell Não Criada", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(df_updown.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in df_updown.columns]
                , style_table={'height': '33vh', 'width':'15vw', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'5vw',
                        'maxWidth':'9vw'
                }]  
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])  
      
    
#------------------- Dataframe atualizacao de tabelas fatos pentaho ---------------------------------------------------

    fig_tabela_atualizacao_pentaho = html.Div([
                html.Label("Ultimos Inserts Pentaho", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(df_tabelas.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in df_tabelas.columns]
                , style_table={'height': '33vh', 'width':'15vw', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'7vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])  
#------------------- Dataframe fim do projeto menor do que inicio ---------------------------------------------------

   
    for i in range(0,len(df_dt_fim_projeto)):    
        df_dt_fim_projeto.iloc[i,0] = "[Projeto](https://app.pipefy.com/open-cards/"+str(df_dt_fim_projeto.iloc[i,0])+")"
        
    fig_tabela_dt_fim_projeto = html.Div([
                html.Label("Data Fim < Início", style = {'font-size' : '14px', 'color' : '#303030', 'margin':'15px 0px 0px 10px'}),
                dash_table.DataTable(df_dt_fim_projeto.to_dict('records'), [{"name": i, "id": i, "presentation":"markdown"} for i in df_dt_fim_projeto.columns]
                , style_table={'height': '33vh', 'width':'15vw', 'whiteSpace': 'normal', 'overflow': 'hidden','textOverflow': 'ellipsis','lineHeight': '15px','overflowY': 'auto', 'overflowX': 'auto','margin':'10px 0px 0px 10px','overflowX': 'auto', "color":"#303030", 'font-family': 'system-ui', 'fontSize': 11}
                , fill_width=False
                , style_data = { 'border' : '1px solid #F2F2F2'}
                , style_header = { 'textAlign':'center', 'border' : '1px solid #F2F2F2', 'background-color':'#FFFFFF', 'fontSize': 13}
                , style_cell = {'textAlign':'right', 'height':'20px','maxWidth':'7vw', 'minWidth':'4vw', 'font-family':'Segoe UI', 'color':'#303030'}
                , style_cell_conditional=[{
                        'if': {'column_id': 'Projeto'},
                        'textAlign': 'center',
                        'minWidth':'4vw',
                        'maxWidth':'6vw'
                }]  
                , css=[dict(selector= "p", rule= "margin: 0; text-align: center; color: #303030; font-size: 14")]
                )
        ])  
    
#-------------------------------retorna todas tabelas ----------------------------------------------------------------------- 
    return fig_tabela_tratativas, fig_vendas_nao_criadas_sales, fig_vendas_nao_criadas_pipe, fig_tabela_sem_franqueado, fig_tabela_sem_cliente_db, fig_tabela_sem_inicio, fig_tabela_tratativa_franquia, fig_tabela_sem_id_central, fig_duplicados_id_contrato, fig_tabela_sem_fee, fig_tabela_sem_data_fim, fig_tabela_sem_finalizacao, fig_tabela_sem_tipo, fig_tabela_tratativa_sem_id_central, fig_tabela_requisicao_up_down, fig_tabela_atualizacao_pentaho, fig_tabela_dt_fim_projeto

# -------------- Run Server ------------- #
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=False, port=8050)