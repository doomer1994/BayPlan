from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
from database import get_all_vessels, get_bays_by_vessel, get_positions_for_bay
from utils.visualizar_bays_utils import gerar_grid_visual

def register_visual_callbacks(app):

    # Preenche o dropdown de navios
    @app.callback(
        Output("vessel-dropdown", "options"),
        Input("vessel-dropdown", "id")
    )
    def carregar_navios(_):
        vessels = get_all_vessels()
        return [{"label": name, "value": pk} for pk, name in vessels]

    # Preenche o dropdown de bays com base no navio
    @app.callback(
        Output("bay-dropdown", "options"),
        Input("vessel-dropdown", "value")
    )
    def carregar_bays(vessel_id):
        if not vessel_id:
            raise PreventUpdate
        bays = get_bays_by_vessel(vessel_id)
        return [{"label": str(b[0]), "value": b[0]} for b in bays]

    # Gera os gráficos ao clicar no botão
    @app.callback(
        Output("store-positions-bay", "data"),
        Output("bay-graphs", "children"),
        Input("btn-carregar-bay", "n_clicks"),
        State("vessel-dropdown", "value"),
        State("bay-dropdown", "value"),
        prevent_initial_call=True
    )
    def gerar_graficos(n_clicks, vessel_id, bay):
        if not vessel_id or not bay:
            raise PreventUpdate

        posicoes = get_positions_for_bay(vessel_id, bay)

        # Identifica se a bay possui só um lado (Bay_Side == Bay)
        bay_sides = {p[2] for p in posicoes}
        apenas_um_lado = (len(bay_sides) == 1 and bay in bay_sides)

        if apenas_um_lado:
            fig = dcc.Graph(
                figure=gerar_grid_visual(posicoes, bay, bay, lado="Único"),
                style={"width": "100%"}
            )
            return posicoes, [fig]

        # Caso contrário, gerar os dois lados: frente e trás
        bay_side_frente = bay - 1
        bay_side_tras = bay + 1

        fig_frente = dcc.Graph(
            figure=gerar_grid_visual(posicoes, bay, bay_side_frente, lado="Frente"),
            style={"width": "49%"}
        )

        fig_tras = dcc.Graph(
            figure=gerar_grid_visual(posicoes, bay, bay_side_tras, lado="Trás"),
            style={"width": "49%"}
        )

        return posicoes, [fig_frente, fig_tras]
