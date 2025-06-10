import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/navios/layout",
    name="Layout das Bays"
)

layout = html.Div([
    html.H3("Definir Layout das Bays do Navio"),

    html.P("Clique nas posições da Bay Frente para ativar/desativar. "
           "Posições ativadas serão refletidas automaticamente no lado Trás, se aplicável."),

    # Seletor do tipo de posição (C, W, F)
    dbc.Row([
        dbc.Col([
            dbc.Label("Tipo de posição:"),
            dcc.RadioItems(
                id="radio-tipo-posicao",
                options=[
                    {"label": "C (Container)", "value": "C"},
                    {"label": "W (Água de Lastro)", "value": "W"},
                    {"label": "F (Combustível)", "value": "F"},
                ],
                value="C",
                inline=True
            )
        ])
    ], className="mb-3"),

    # Dropdown oculto (mantido para compatibilidade futura)
    dbc.Row([
        dbc.Col([
            html.Div(id="row-dropdown-wf", children=[
                dbc.Label("Tanque associado (opcional):"),
                dcc.Dropdown(id="dropdown-wf", options=[])
            ], style={"display": "none"})
        ])
    ], className="mb-3"),

    html.Hr(),

    html.H5("Gerenciar Layout das Bays"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Bay de origem (copiar layout):"),
            dcc.Dropdown(id="dropdown-bay-origem", options=[], placeholder="Escolha a Bay"),
        ], md=4),

        dbc.Col([
            dbc.Label("Bay(s) de destino:"),
            dcc.Dropdown(id="dropdown-bay-destino", options=[], multi=True, placeholder="Selecione Bays"),
        ], md=5),

        dbc.Col([
            dbc.Label(" "),
            dbc.Button("Copiar Layout", id="btn-copiar-layout", color="secondary", className="mt-2"),
        ], md=3)
    ], className="mb-4"),

    html.Div(id="tabs-bays", className="mb-4"),

    dbc.Button("Salvar Layout", id="btn-salvar-layout", color="success"),

    html.Div(id="mensagem-status", className="mt-3"),

    # Stores (dados temporários)
    dcc.Store(id="store-navio-info", storage_type="session"),
    dcc.Store(id="store-selection-mode", storage_type="session"),
    dcc.Store(id="store-layout-bays", data={}, storage_type="session"),
    dcc.Store(id="store-bays-apenas-frente", data={}, storage_type="session")
])