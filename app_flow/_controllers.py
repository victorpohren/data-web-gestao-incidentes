from dash import (html, dcc)
import dash_bootstrap_components as dbc
from app import app

controllers = dbc.Row([
    html.Img(id = "logo", src = app.get_asset_url("v4-logo.jpg"), style = {"width":"30%", "border-radius":"10px"}),
    html.H4("""Gestão de Incidentes""", style = {"margin": "30px 0px 15px 0px", "color": "#A8A9AA"}),
    html.P("""Utilize este dashboard para analisar as informações de erros de preenchimentos nos campos fundamentais do processo de gestão das unidades.
    """, style = {"margin": "0px 0px 15px 0px", "color": "#A8A9AA"}),
    dbc.Button(
        id = 'pesquisar', children = 'Ver Erros',
        style = {"width":"200px", "margin":"20px 0px 20px 10px", "font-size": "14px","background-color":"#BF2121","border-color":"#BF2121"}
    )
], style={"margin":"40px 20px 0px 20px"})