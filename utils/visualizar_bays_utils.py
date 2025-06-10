from dataclasses import replace

import plotly.graph_objects as go
from database import get_connection

# Gera o layout visual da Bay com base nas posições reais da tabela Vessel_Stow
def gerar_grid_visual(posicoes_db, bay, bay_side, lado="Frente"):
    # Obtem tamanho da bay teórica a partir do navio
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT num_rows, tiers_hold, tiers_deck
        FROM Vessel
        WHERE PK_Id = (SELECT FK_Vessel_Id FROM Vessel_Stow WHERE Bay = ? LIMIT 1)
    """, (bay,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return go.Figure()

    num_rows, tiers_hold, tiers_deck = row
    num_rows_each_side = num_rows // 2

    # Labels de row (pares decrescentes à esquerda, ímpares crescentes à direita)
    row_labels_left = list(range(2 * num_rows_each_side, 0, -2))
    row_labels_right = list(range(1, 2 * num_rows_each_side + 1, 2))
    row_labels = row_labels_left + row_labels_right
    row_map = {i: f"{row_labels[i]:02d}" for i in range(len(row_labels))}

    # Tiers: 02, 04, ..., 78 para Hold; 80, 82... para Deck
    tiers_hold_vals = [2 * i for i in range(1, tiers_hold + 1)]
    tiers_deck_vals = [80 + 2 * i for i in range(tiers_deck)]
    all_tiers = tiers_hold_vals + tiers_deck_vals

    # Mapeia as posições reais (Bay_Side, Row, Tier) com tipo
    posicoes_reais = {
        f"{p[2]}-{int(p[0]):02d}-{int(p[1]):02d}": p[4]  # chave: Bay_Side-Row-Tier → valor: Type (C/W/F)
        for p in posicoes_db if p[2] == bay_side
    }

    shapes = []
    annotations = []
    points = []


    for y_index, tier in enumerate(all_tiers):
        for x_index in range(len(row_labels)):
            row_num = row_map[x_index]
            pos_key = f"{bay_side}-{row_num}-{tier:02d}"

            tipo = posicoes_reais.get(pos_key)
            existe = tipo is not None

            if tipo is not None:
                tipo_label = f"{tipo}"
            else:
                tipo_label = "X"

            # Define estilo da borda
            line_style = dict(color="black", width=1, dash="solid" if existe else "dot")

            # Define cor de preenchimento com base no tipo
            if tipo == "C":
                fill = "#ccffcc"  # verde claro
            elif tipo == "W":
                fill = "#cce5ff"  # azul claro
            elif tipo == "F":
                fill = "#ffd9b3"  # laranja claro
            else:
                fill = "white"    # posição teórica (não cadastrada)

            shapes.append(dict(
                type="rect",
                x0=x_index, x1=x_index + 1,
                y0=y_index, y1=y_index + 1,
                line=line_style,
                fillcolor=fill,
                layer="below",
                name=pos_key
            ))

            annotations.append(dict(
                x=x_index + 0.5, y=y_index + 0.5,
                text= tipo_label,
                showarrow=False,
                font=dict(size=9)
            ))

            points.append(dict(
                x=x_index + 0.5,
                y=y_index + 0.5,
                text=pos_key
            ))

    # Linha divisória entre Hold e Deck
    shapes.append(dict(
        type="line",
        x0=-0.6, x1=len(row_labels) + 0.6,
        y0=len(tiers_hold_vals), y1=len(tiers_hold_vals),
        line=dict(color="black", width=2)
    ))

    # Numeração das Rows
    for i in range(len(row_labels)):
        row_label = row_map[i]
        for y in [-0.4, len(all_tiers) + 0.2]:
            annotations.append(dict(
                x=i + 0.5, y=y,
                text=row_label,
                showarrow=False,
                font=dict(size=10)
            ))

    # Numeração das Tiers
    for y_index, tier in enumerate(all_tiers):
        for x in [-0.6, len(row_labels) + 0.6]:
            annotations.append(dict(
                x=x, y=y_index + 0.5,
                text=f"{tier:02d}",
                showarrow=False,
                font=dict(size=10),
                xanchor='right' if x < 0 else 'left'
            ))

    # Monta o gráfico
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[p["x"] for p in points],
        y=[p["y"] for p in points],
        mode="markers",
        marker=dict(size=20, opacity=0),
        text=[p["text"] for p in points],
        hoverinfo="text"
    ))

    fig.update_layout(
        title=f"Bay {bay} (Bay_Side {bay_side}) - {lado}",
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(range=[-1, len(row_labels) + 1], visible=False, scaleanchor="y"),
        yaxis=dict(range=[-1, len(all_tiers) + 1], visible=False),
        margin=dict(l=40, r=40, t=40, b=40),
        height=600,
        width=500,
        plot_bgcolor="white"
    )

    return fig