import sqlite3

# Caminho do banco de dados
DB_PATH = "Stow_Planing.db"

# Função principal para obter conexão
def get_connection():
    return sqlite3.connect(DB_PATH)

# Insere um novo navio na tabela Vessel
def insert_vessel(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Vessel (
            PK_Id, Name, num_bays, num_rows, tiers_hold, tiers_deck,
            fuel_volume, fuel_density, ballast_volume, ballast_density
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["pk_id"],
        data["nome"],
        data["num_bays"],
        data["num_rows"],
        data["tiers_hold"],
        data["tiers_deck"],
        data["fuel_volume"],
        data["fuel_density"],
        data["ballast_volume"],
        data["ballast_density"]
    ))

    conn.commit()
    conn.close()

# Retorna todos os navios cadastrados (para dropdowns)
def get_all_vessels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT PK_Id, Name FROM Vessel ORDER BY Name")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Retorna as bays disponíveis para um navio
def get_bays_by_vessel(vessel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT Bay
        FROM Vessel_Stow
        WHERE FK_Vessel_Id = ?
        ORDER BY Bay
    """, (vessel_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Retorna as posições (row, tier, bay_side, type) para uma bay de um navio
def get_positions_for_bay(vessel_id, bay):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Row, Tier, Bay_side, Position, Type
        FROM Vessel_Stow
        WHERE FK_Vessel_Id = ? AND Bay = ?
    """, (vessel_id, bay))
    rows = cursor.fetchall()
    conn.close()
    return rows

def atualizar_tipo_posicao(navio_id, bay, bay_side, row, tier, novo_tipo):
    """Atualiza o tipo (C, W, F ou None) de uma posição no layout."""
    conn = get_connection()
    cur = conn.cursor()

    if novo_tipo:
        # Atualiza se já existe, senão insere
        cur.execute("""
            INSERT INTO Vessel_Stow (vessel_id, bay, bay_side, row, tier, type)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(vessel_id, bay, bay_side, row, tier)
            DO UPDATE SET type = excluded.type
        """, (navio_id, bay, bay_side, row, tier, novo_tipo))
    else:
        # Se tipo é None, deletar a posição
        cur.execute("""
            DELETE FROM Vessel_Stow
            WHERE vessel_id = ? AND bay = ? AND bay_side = ? AND row = ? AND tier = ?
        """, (navio_id, bay, bay_side, row, tier))

    conn.commit()
    conn.close()

def obter_layout_dict(navio_id, bay, bay_side):
    """Retorna um dicionário com as posições existentes e seus tipos para a bay atual."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT row, tier, type FROM Vessel_Stow
        WHERE vessel_id = ? AND bay = ? AND bay_side = ?
    """, (navio_id, bay, bay_side))
    resultados = cur.fetchall()
    conn.close()

    return {f"{row}_{tier}": tipo for row, tier, tipo in resultados}
