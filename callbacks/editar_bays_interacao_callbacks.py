from dash import Input, Output, State, no_update
from utils.layout_editar_bays_utils import gerar_grid_layout
from database import atualizar_tipo_posicao


def register_navio_layout_interaction_callbacks(app):
    @app.callback(
        Output('layout-figura', 'figure'),
        Input('layout-figura', 'clickData'),
        State('store-navio-id', 'data'),
        State('dropdown-bay', 'value'),
        State('tabs-bay-side', 'value'),
        State('store-layout-atual', 'data'),
        prevent_initial_call=True
    )
    def marcar_posicao(click_data, navio_id, bay, bay_side, layout_data):
        if not click_data or not layout_data:
            return no_update

        ponto = click_data['points'][0]
        row = ponto['x']
        tier = ponto['y']

        key = f"{row}_{tier}"
        posicao_atual = layout_data.get(key)

        # Alternar entre os tipos C -> W -> F -> None -> C ...
        if posicao_atual == 'C':
            novo_tipo = 'W'
        elif posicao_atual == 'W':
            novo_tipo = 'F'
        elif posicao_atual == 'F':
            novo_tipo = None
        else:
            novo_tipo = 'C'

        # Atualiza dicionário local
        if novo_tipo:
            layout_data[key] = novo_tipo
        else:
            layout_data.pop(key, None)

        # Atualizar no banco de dados
        atualizar_tipo_posicao(navio_id, bay, bay_side, row, tier, novo_tipo)

        # Gerar nova figura atualizada
        nova_figura = gerar_grid_layout(navio_id, bay, bay_side, layout_data)
        return nova_figura
