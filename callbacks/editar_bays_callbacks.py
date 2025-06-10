import dash
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.layout_editar_bays_utils import gerar_grid_layout


def register_callbacks(app):

    @app.callback(
        Output("row-dropdown-wf", "style"),
        Output("dropdown-wf", "options"),
        Input("radio-tipo-posicao", "value")
    )
    def toggle_dropdown(tipo):
        if tipo == "C":
            return {"display": "none"}, []
        return {"display": "none"}, []

    @app.callback(
        Output("store-selection-mode", "data"),
        Input("radio-tipo-posicao", "value"),
        Input("dropdown-wf", "value")
    )
    def update_selection_mode(tipo, tanque_id):
        if tipo == "C":
            return {"type": "C"}
        return {"type": tipo, "w_f_id": tanque_id} if tanque_id else {"type": tipo}

    @app.callback(
        Output("tabs-bays", "children"),
        Output("dropdown-bay-origem", "options"),
        Output("dropdown-bay-destino", "options"),
        Input("store-navio-info", "data"),
        Input("store-bays-apenas-frente", "data")
    )
    def gerar_abas_layout(navio_info, dict_apenas_frente):
        if not navio_info:
            raise PreventUpdate

        abas = []
        num_bays = navio_info["num_bays"]
        num_rows = navio_info["num_rows"]
        tiers_hold = navio_info["tiers_hold"]
        tiers_deck = navio_info["tiers_deck"]

        bays = [2 + 4 * i for i in range(num_bays)]
        dropdown_options = [{"label": f"Bay {b:02d}", "value": b} for b in bays]

        for bay in bays:
            bay_side_frente = bay - 1
            bay_side_tras = bay + 1

            layout_frente = dcc.Graph(
                id=f"graph-{bay}-front",
                figure=gerar_grid_layout(bay, bay_side_frente, num_rows, tiers_hold, tiers_deck, lado="Frente"),
                config={"displayModeBar": False}
            )

            checkbox = dbc.Checkbox(
                id={"type": "check-bay-apenas-frente", "index": bay},
                label="Esta Bay possui apenas Bay_Side Frente",
                value=dict_apenas_frente.get(str(bay), False),
                className="mt-2"
            )

            children = [
                html.Div(layout_frente, style={"width": "49%", "display": "inline-block"})
            ]

            if not dict_apenas_frente.get(str(bay), False):
                layout_tras = dcc.Graph(
                    id=f"graph-{bay}-rear",
                    figure=gerar_grid_layout(bay, bay_side_tras, num_rows, tiers_hold, tiers_deck, lado="Trás"),
                    config={"displayModeBar": False}
                )
                children.append(html.Div(layout_tras, style={"width": "49%", "display": "inline-block"}))

            abas.append(
                dbc.Tab(label=f"Bay {bay:02d}", tab_id=f"tab-{bay}", children=[
                    html.Div(children),
                    html.Div(checkbox),
                    html.P("Clique nas posições da Bay Frente para ativar/desativar.")
                ])
            )

        return dbc.Tabs(abas, active_tab="tab-2"), dropdown_options, dropdown_options

    @app.callback(
        Output("store-layout-bays", "data"),
        Input("btn-copiar-layout", "n_clicks"),
        State("dropdown-bay-origem", "value"),
        State("dropdown-bay-destino", "value"),
        State("store-layout-bays", "data"),
        prevent_initial_call=True
    )
    def copiar_layout(n_clicks, bay_origem, bays_destino, layout_data):
        if not bay_origem or not bays_destino:
            raise PreventUpdate
        if f"{bay_origem}" not in layout_data:
            raise PreventUpdate

        layout_origem = layout_data[str(bay_origem)]
        for destino in bays_destino:
            layout_data[str(destino)] = layout_origem.copy()
        return layout_data

    @app.callback(
        Output("store-bays-apenas-frente", "data"),
        Input({"type": "check-bay-apenas-frente", "index": dash.ALL}, "value"),
        State({"type": "check-bay-apenas-frente", "index": dash.ALL}, "id"),
        State("store-bays-apenas-frente", "data"),
        prevent_initial_call=True
    )
    def atualizar_flags_apenas_frente(valores, ids, atual):
        if not atual:
            atual = {}
        for v, i in zip(valores, ids):
            atual[str(i["index"])] = v
        return atual
