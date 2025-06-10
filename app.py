import dash
from dash import html
import dash_bootstrap_components as dbc
from callbacks.visualizar_bays_callbacks import register_visual_callbacks
from callbacks.cadastrar_navio_callbacks import register_callbacks as register_cadastro_callbacks
from callbacks.editar_bays_callbacks import register_callbacks as register_layout_callbacks


# Criação da instância principal do app com suporte a múltiplas páginas
app = dash.Dash(
    __name__,
    use_pages=True,  # Ativa o sistema de páginas do Dash
    external_stylesheets=[dbc.themes.BOOTSTRAP]  # Tema Bootstrap
)

app.title = "BayPlan App"

# Layout principal do aplicativo com menu e container de páginas
app.layout = html.Div([
    # Barra de navegação com menus dropdown
    dbc.NavbarSimple(
        children=[
            # Menu Containers
            dbc.DropdownMenu(
                label="Containers", nav=True, in_navbar=True,
                children=[
                    dbc.DropdownMenuItem("Cadastrar", href="/containers/cadastrar"),
                    dbc.DropdownMenuItem("Pesquisar / Alterar", href="/containers/gerenciar"),
                ]
            ),

            # Menu Navios
            dbc.DropdownMenu(
                label="Navios", nav=True, in_navbar=True,
                children=[
                    dbc.DropdownMenuItem("Cadastrar", href="/navios/cadastrar"),
                    dbc.DropdownMenuItem("Gerenciar Bays e Layout", href="/visual/gerenciar-bays"),
                ]
            ),

            # Menu Operações
            dbc.DropdownMenu(
                label="Operações", nav=True, in_navbar=True,
                children=[
                    dbc.DropdownMenuItem("Nova Operação", href="/operacoes/nova"),
                    dbc.DropdownMenuItem("Pesquisar / Alterar", href="/operacoes/gerenciar"),
                    dbc.DropdownMenuItem("Alocar Containers", href="/operacoes/alocar"),
                ]
            ),

            # Menu Visualizações
            dbc.DropdownMenu(
                label="Visualizações", nav=True, in_navbar=True,
                children=[
                    dbc.DropdownMenuItem("Panorama Geral do Navio", href="/visual/panorama"),
                    dbc.DropdownMenuItem("Panorama Geral Operações", href="/visual/panorama-geral-operacoes"),
                ]
            ),
        ],
        brand="BayPlan App",  # Nome do sistema
        color="primary",      # Cor do navbar
        dark=True             # Tema escuro
    ),

    # Container que renderiza a página ativa
    dash.page_container
])

# Registra os callbacks do módulo Gerenciar bays
register_visual_callbacks(app)

# Registra os callbacks do módulo Cadastro de navio
register_cadastro_callbacks(app)

# Registra os callbacks do módulo Layout das bays
register_layout_callbacks(app)

# Inicia o servidor local de desenvolvimento
if __name__ == "__main__":
    app.run(debug=True)
