import dash
import dash_bootstrap_components as dbc
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'password'
}

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server
app.scripts.config.serve_locally = True
server = app.server