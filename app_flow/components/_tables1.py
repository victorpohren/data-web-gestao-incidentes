from dash import (html, dcc)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

tableTratativas = dbc.Row([
    dbc.Col(id = "check_tratativas", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 10px"})
], style={"height":"42vh"})

tableVendasSales = dbc.Row([
    dbc.Col(id = "check_vendas_sales", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 10px"})
], style={"height":"42vh"})

tableVendasPipe = dbc.Row([
    dbc.Col(id = "check_vendas_pipe", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 0px"})
], style={"height":"42vh"})

tableFranqueado = dbc.Row([
    dbc.Col(id = "check_franqueado", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 10px"})
], style={"height":"42vh"})

tableCliente = dbc.Row([
    dbc.Col(id = "check_cliente", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 10px"})
], style={"height":"42vh"})

tableInicio = dbc.Row([
    dbc.Col(id = "check_inicio", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 0px"})
], style={"height":"42vh"})

tableTratativasFranquias = dbc.Row([
    dbc.Col(id = "check_tratativas_franquias", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 10px"})
], style={"height":"42vh"})

tableUpsellDownsell = dbc.Row([
    dbc.Col(id = "check_upsell_downsell", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 10px"})
], style={"height":"42vh"})

tableDuplicados = dbc.Row([
    dbc.Col(id = "check_dups", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 0px"})
], style={"height":"42vh"})

tableFee = dbc.Row([
    dbc.Col(id = "check_fee", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 10px"})
], style={"height":"42vh"})

tableDataFim = dbc.Row([
    dbc.Col(id = "check_data_fim", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 0px"})
], style={"height":"42vh"})

tableTipoFinalizacao = dbc.Row([
    dbc.Col(id = "check_finalizacao", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 0px"})
], style={"height":"42vh"})

tableTipoChurn = dbc.Row([
    dbc.Col(id = "check_tipo_churn", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 0px"})
], style={"height":"42vh"})

tableTratativasIdCentral = dbc.Row([
    dbc.Col(id = "check_tratativa_central_id", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 10px"})
], style={"height":"42vh"})

tableRequisicaoUpDown = dbc.Row([
    dbc.Col(id = "check_up_down", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 0px"})
], style={"height":"42vh"})

tableTabelas = dbc.Row([
    dbc.Col(id = "check_tabelas", style= {"background-color":"#FFFFFF", "margin":"0px 0px 0px 0px"})
], style={"height":"42vh"})

tableDataFimProjeto = dbc.Row([
    dbc.Col(id = "check_data_fim_projeto", style= {"background-color":"#FFFFFF", "margin":"0px 10px 0px 0px"})
], style={"height":"42vh"})