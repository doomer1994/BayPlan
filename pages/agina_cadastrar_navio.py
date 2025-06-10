import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/navios/cadastrar",
    name="Cadastrar Navio"
)

layout = html.Div([
    html.H3("Cadastro de Novo Navio"),

    # Formulário do navio
    dbc.Row([
        dbc.Col([
            dbc.Label("Nome do Navio:"),
            dbc.Input(id="input-nome-navio", type="text", placeholder="Ex: MV Brasil"),
        ], md=6),

        dbc.Col([
            dbc.Label("Número de Bays (pares):"),
            dbc.Input(id="input-num-bays", type="number", min=1, step=1),
        ], md=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Número total de Rows (pares):"),
            dbc.Input(id="input-num-rows", type="number", min=2, step=2),
        ], md=4),

        dbc.Col([
            dbc.Label("Tiers no Porão (Hold):"),
            dbc.Input(id="input-tiers-hold", type="number", min=1, step=1),
        ], md=4),

        dbc.Col([
            dbc.Label("Tiers no Convés (Deck):"),
            dbc.Input(id="input-tiers-deck", type="number", min=0, step=1),
        ], md=4),
    ], className="mb-4"),

    html.Hr(),
    html.H4("Informações dos Tanques"),

    # Tanque de combustível
    dbc.Row([
        dbc.Col([
            dbc.Label("Volume do Tanque de Combustível (m³):"),
            dbc.Input(id="input-volume-combustivel", type="number", step=0.1),
        ], md=6),

        dbc.Col([
            dbc.Label("Densidade do Combustível (kg/m³):"),
            dbc.Input(id="input-density-combustivel", type="number", step=0.01),
        ], md=6),
    ], className="mb-3"),

    # Tanque de lastro
    dbc.Row([
        dbc.Col([
            dbc.Label("Volume do Tanque de Lastro (m³):"),
            dbc.Input(id="input-volume-lastro", type="number", step=0.1),
        ], md=6),

        dbc.Col([
            dbc.Label("Densidade da Água de Lastro (kg/m³):"),
            dbc.Input(id="input-density-lastro", type="number", step=0.01),
        ], md=6),
    ], className="mb-4"),

    html.Hr(),

    dbc.Button("Continuar para Layout das Bays", id="btn-continuar-layout", color="primary", className="mt-3"),

    # Armazenamento temporário
    dcc.Store(id="store-navio-info", storage_type="session"),
    dcc.Store(id="store-wf-list", data=[], storage_type="session"),

    # Redirecionamento após salvar
    dcc.Location(id="redirect-layout", refresh=True)
])