from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
import uuid

# Registra os callbacks da tela de cadastro de navio
def register_callbacks(app):

    @app.callback(
        Output("store-navio-info", "data"),
        Output("redirect-layout", "pathname"),
        Input("btn-continuar-layout", "n_clicks"),
        State("input-nome-navio", "value"),
        State("input-num-bays", "value"),
        State("input-num-rows", "value"),
        State("input-tiers-hold", "value"),
        State("input-tiers-deck", "value"),
        State("input-volume-combustivel", "value"),
        State("input-density-combustivel", "value"),
        State("input-volume-lastro", "value"),
        State("input-density-lastro", "value"),
        prevent_initial_call=True
    )
    def armazenar_info_navio(
        n_clicks, nome, num_bays, num_rows, tiers_hold, tiers_deck,
        fuel_vol, fuel_dens, ballast_vol, ballast_dens
    ):
        # Validação simples
        if not all([nome, num_bays, num_rows, tiers_hold, tiers_deck,
                    fuel_vol, fuel_dens, ballast_vol, ballast_dens]):
            raise PreventUpdate

        # Gera um ID único para o navio
        navio_id = str(uuid.uuid4())[:8]

        # Monta o dicionário com todas as informações do navio
        navio_data = {
            "pk_id": navio_id,
            "nome": nome,
            "num_bays": int(num_bays),
            "num_rows": int(num_rows),
            "tiers_hold": int(tiers_hold),
            "tiers_deck": int(tiers_deck),
            "fuel_volume": float(fuel_vol),
            "fuel_density": float(fuel_dens),
            "ballast_volume": float(ballast_vol),
            "ballast_density": float(ballast_dens)
        }

        # Redireciona para a próxima etapa
        return navio_data, "/navios/layout"