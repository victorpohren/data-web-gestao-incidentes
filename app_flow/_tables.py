from dash import (html, dcc)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from components._tables1 import *


navTables = dbc.Row([
    # html.Div([
    #     dbc.Button("Resultados", color = "light", className = "navBar", style = {"margin": "0px 5px 5px 0px"}),
    #     dbc.Button("Pesquisas", color = "light", className = "navBar", style = {"margin": "0px 5px 5px 0px"}),
    #     dbc.Button("Cobranças", color = "light", className = "navBar", style = {"margin": "0px 5px 5px 0px"}),
    #     dbc.Button("Tratativas", color = "light", className = "navBar", style = {"margin": "0px 5px 5px 0px"}),
    # ], style={"margin":"40px 20px 0px 20px"}),
    html.Div([
        dbc.Row([
            dbc.Col([tableTratativas], style={"margin":"20px 0px 0px 20px"}), 
            dbc.Col([tableVendasSales], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableVendasPipe], style={"margin":"20px 20px 0px 0px"})
        ]),
         dbc.Row([
            dbc.Col([tableFranqueado], style={"margin":"20px 0px 0px 20px"}), 
            dbc.Col([tableCliente], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableInicio], style={"margin":"20px 20px 0px 0px"})
        ]),
         dbc.Row([
            dbc.Col([tableTratativasFranquias], style={"margin":"20px 0px 0px 20px"}), 
            dbc.Col([tableUpsellDownsell], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableDuplicados], style={"margin":"20px 20px 0px 0px"})
        ]),
        dbc.Row([
            dbc.Col([tableFee], style={"margin":"20px 20px 0px 20px"}),
            dbc.Col([tableDataFim], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableTipoFinalizacao], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableTipoChurn], style={"margin":"20px 20px 0px 0px"})
        ]),
        dbc.Row([
            dbc.Col([tableTratativasIdCentral], style={"margin":"20px 20px 0px 20px"}),
            dbc.Col([tableRequisicaoUpDown], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableTabelas], style={"margin":"20px 20px 0px 0px"}),
            dbc.Col([tableDataFimProjeto], style={"margin":"20px 20px 0px 0px"})
        ])
    ], id = "navTabelas")
])
