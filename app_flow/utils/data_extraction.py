import pyodbc as odbc
import pandas as pd
import json
from keys.get_token import get_secret
from tqdm import tqdm

def pullFromSqlServerTratativas():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    # Creating Cursor Conectors and getting data.
    query = """
            SELECT A.projeto_central_id
	        , A.card_id
            , A.title
            , A.current_phase
            , A.created_at
	        FROM [v4company].[pipefy_tratativas] A with(nolock)
	        JOIN (
		            SELECT projeto_central_id, MAX(created_at) AS "created_at" 
			        FROM [v4company].[pipefy_tratativas] with(nolock)
			        GROUP BY projeto_central_id
	            ) B on B.projeto_central_id = A.projeto_central_id
	        WHERE A.projeto_central_id  = B.projeto_central_id and A.created_at  = B.created_at and A.current_phase = 'Concluído'
            """


    df = pd.read_sql(query,conn)
    print('First Extraction Concluded.')
    return df

def pullFromSqlServerProjetos():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    # Creating Cursor Conectors and getting data.
    query = """
            SELECT [id]
                ,[title]
                ,[createdAt]
                ,[current_phase]
                ,[cliente_database]
                ,[responsavel_pelo_projeto_database]
                ,[valor_do_deal]
                ,[vigencia_do_contrato]
                ,[client_id]
                ,[inicio_do_projeto]
                ,[data_fim_do_projeto]
                ,[tipo_de_finalizacao]
                ,[tipo_de_churn]
                ,[franqueado_id]
                ,[id_opp_sales_force]
                ,RIGHT(link_do_contrato,NULLIF(CHARINDEX('=',REVERSE(link_do_contrato)),0)-1) as contract_id
            FROM [v4company].[PipedeProjetos] with(nolock)
            WHERE (createdAt >= '2021-01-01T00:00:00-00:00')
            AND current_phase <> 'Arquivado'
            ORDER by createdAt ASC
    """


    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerSalesForce():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    # Creating Cursor Conectors and getting data.
    query = """
            SELECT A.id, A.company FROM (
            SELECT * FROM fatos.sales_force 
            WHERE Data_fase_historico > '2023-01-01' AND Fase_atual = 'Fechado/Ganho' AND Fase_historico = 'Fechado/Ganho'
                ) A
                LEFT JOIN (
                        SELECT * FROM v4company.PipedeProjetos 
                        ) B ON B.id_opp_sales_force = A.id
                WHERE B.id_opp_sales_force IS NULL
    """

    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerPipeVendas():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """
            SELECT A.card_id, A.title FROM (
            SELECT * FROM v4company.PipedeVendas 
            WHERE created_at > '2023-01-01' AND current_phase = 'Ganho/CS'
            ) A
            LEFT JOIN (
                    SELECT * FROM v4company.PipedeProjetos 
                    ) B ON B.id_card_da_venda = A.card_id
            WHERE B.id_card_da_venda IS NULL
    """

    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerPipeUpsellDownsell():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
            SELECT card_id, title
            FROM v4company.PipedeUpDown with(nolock)
            WHERE current_phase IN ('Upsell','Downsell')
            AND idcard_central = ''
    """

    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerTratativasFranquias():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
            SELECT A.card_id, A.title FROM (
            SELECT * FROM v4company.v4company.pipefy_tratativas_franquias 
            WHERE current_phase = 'CONCLUÍDO - Revisão CST' AND tipo_da_tratativa <> 'Alinhamento com o cliente' AND created_at > '2023-03-30T00:00:00-00:00'
            ) A
            LEFT JOIN (
                    SELECT * FROM v4company.v4company.pipefy_tratativas 
                    WHERE origem_pipe_de_tratativas_dos_franqueados = 'Sim'
                    ) B ON B.id_tratativa_franquia = A.card_id
            WHERE B.card_id IS NULL
    """
    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerTratativasIDCentralBlank():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
            SELECT card_id, title
            FROM v4company.pipefy_tratativas with(nolock)
            WHERE current_phase <> 'Arquivado'
            AND projeto_central_id = ''
    """
    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerRequisicaoUpsell():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
            SELECT A.card_id, A.title FROM (
            SELECT * FROM v4company.v4company.pipefy_alteracao_contratos 
            WHERE created_at > '2022-12-31T00:00:00-00:00' 
            AND escolha_o_tipo_de_altera_o_no_contrato_desejada = '["Alteração de valor (upsell/downsell)"]'
            AND current_phase = 'Concluído'
            ) A
            LEFT JOIN (
                    SELECT * FROM v4company.v4company.PipedeUpDown 
                    ) B ON B.idcard_alteracao_contrato = A.card_id
            WHERE B.idcard_alteracao_contrato IS NULL
    """
    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df

def pullFromSqlServerAtualizacaoTabelas():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
            SELECT 'fatos.sales_force' as Tabelas, MAX(data_insert) as ultimo_insert FROM fatos.sales_force
            UNION ALL
            SELECT 'fatos.pipe_vendas' as Tabela, MAX(data_insert) as ultimo_insert FROM fatos.pipe_vendas
            UNION ALL
            SELECT 'fatos.central_de_projetos' as Tabela, MAX(data_insert) as ultimo_insert FROM fatos.central_de_projetos
            UNION ALL
            SELECT 'fatos.investimentos' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.investimentos
            UNION ALL
            SELECT 'fatos.lead_broker' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.lead_broker
            UNION ALL
            SELECT 'fatos.registro_variavel' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.registro_variavel
            UNION ALL
            SELECT 'fatos.roi_day' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.roi_day
            UNION ALL
            SELECT 'fatos.tratativas_novo' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.tratativas_novo
            UNION ALL
           SELECT 'fatos.upsell_downsell' as Tabela, MAX(dt_insert) as ultimo_insert FROM fatos.upsell_downsell;
    """
    df = pd.read_sql(query,conn)
    print('Final Extraction Concluded.')
    return df

def pullFromSqlServerDtFimProjeto():

    # Connection SQL Server
    server = server
    database = database
    username = username
    password = password
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    query = """ 
        SELECT
        Card_ID AS Projeto,
        [Nome do cliente] AS Empresa,
        CONVERT(VARCHAR(10), inicio_do_projeto, 105) AS [Dt Inicio], -- Formato "dd-mm-aaaa"
        CONVERT(VARCHAR(10), data_fim_do_projeto, 105) AS [Dt Fim]     -- Formato "dd-mm-aaaa"
        FROM
        fatos.central_de_projetos
        WHERE
        inicio_do_projeto > data_fim_do_projeto
        AND
        [Fase atual] = 'Concluído'
        ORDER BY data_fim_do_projeto DESC
    """
    df = pd.read_sql(query,conn)
    print('Extraction Concluded.')
    return df