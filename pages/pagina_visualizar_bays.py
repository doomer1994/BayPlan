import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/visual/gerenciar-bays",
    name="Gerenciar Bays"
)

layout = html.Div([
    html.H3("Visualizar Layout de Bay de Navio"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Selecione o Navio:"),
            dcc.Dropdown(id="vessel-dropdown", options=[], value=None),
        ], md=4),

        dbc.Col([
            dbc.Label("Selecione a Bay:"),
            dcc.Dropdown(id="bay-dropdown", options=[], value=None),
        ], md=4),

        dbc.Col([
            dbc.Label(" "),
            dbc.Button("Carregar Visualização", id="btn-carregar-bay", color="primary", className="mt-4"),
        ], md=4),
    ], className="mb-4"),

    html.Div(id="bay-graphs", style={"display": "flex", "gap": "20px"}),

    dcc.Store(id="store-positions-bay")
])