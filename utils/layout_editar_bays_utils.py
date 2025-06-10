import plotly.graph_objects as go

# Gera a figura (grid) de uma Bay_Side teórica com base nas configurações do navio
def gerar_grid_layout(bay, bay_side, num_rows, tiers_hold, tiers_deck, lado="Frente"):
    # Divide rows entre esquerda e direita
    num_rows_each_side = num_rows // 2

    # Gera labels para as rows (pares decrescentes à esquerda, ímpares crescentes à direita)
    row_labels_left = list(range(2 * num_rows_each_side, 0, -2))
    row_labels_right = list(range(1, 2 * num_rows_each_side + 1, 2))
    row_labels = row_labels_left + row_labels_right
    row_map = {i: f"{row_labels[i]:02d}" for i in range(len(row_labels))}

    # Gera tiers (02 a N para porão, 80 em diante para deck)
    tiers_hold_vals = [2 * i for i in range(1, tiers_hold + 1)]
    tiers_deck_vals = [80 + 2 * i for i in range(tiers_deck)]
    all_tiers = tiers_hold_vals + tiers_deck_vals

    shapes = []
    annotations = []
    points = []

    for y_index, tier in enumerate(all_tiers):
        for x_index in range(len(row_labels)):
            row_num = row_map[x_index]
            pos_key = f"{bay_side}-{row_num}-{tier:02d}"

            shapes.append(dict(
                type="rect",
                x0=x_index, x1=x_index + 1,
                y0=y_index, y1=y_index + 1,
                line=dict(color="black", width=1, dash="dot"),  # Tracejado: posição ainda não ativada
                fillcolor="white",
                layer="below",
                name=pos_key
            ))

            annotations.append(dict(
                x=x_index + 0.5, y=y_index + 0.5,
                text="X",  # Visual inicial para posição não utilizada
                showarrow=False,
                font=dict(size=10)
            ))

            points.append(dict(
                x=x_index + 0.5,
                y=y_index + 0.5,
                text=pos_key
            ))

    # Linha divisória entre porão e deck
    shapes.append(dict(
        type="line",
        x0=-0.6, x1=len(row_labels) + 0.6,
        y0=len(tiers_hold_vals), y1=len(tiers_hold_vals),
        line=dict(color="black", width=2)
    ))

    # Numeração das rows
    for i in range(len(row_labels)):
        row_label = row_map[i]
        for y in [-0.4, len(all_tiers) + 0.2]:
            annotations.append(dict(
                x=i + 0.5, y=y,
                text=row_label,
                showarrow=False,
                font=dict(size=10)
            ))

    # Numeração das tiers
    for y_index, tier in enumerate(all_tiers):
        for x in [-0.6, len(row_labels) + 0.6]:
            annotations.append(dict(
                x=x, y=y_index + 0.5,
                text=f"{tier:02d}",
                showarrow=False,
                font=dict(size=10),
                xanchor='right' if x < 0 else 'left'
            ))

    # Cria figura Plotly
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