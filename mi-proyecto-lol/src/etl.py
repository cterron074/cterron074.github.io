import os
import sys  # <-- Necesario para reportar errores reales a Render
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN Y RUTA
# ==========================================
DB_USER = "avnadmin"
DB_PASSWORD = "AVNS_pu8DuuDDpatGY7euatj"  
DB_HOST = "mysql-mi-proyecto-lol.b.aivencloud.com"
DB_PORT = "15368"
DB_NAME = "defaultdb"

# Corrección de Ruta: Detecta automáticamente la carpeta 'src' en Render o Local
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ORIGEN = "data_limpio.csv"  # <-- Usa el archivo limpio generado por preparar_etl.py

def get_db_engine():
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def run_etl():
    engine = get_db_engine()
    path_origen = os.path.join(DIRECTORIO_ACTUAL, ARCHIVO_ORIGEN)
    
    if not os.path.exists(path_origen):
        print(f"[Error] No se encontró el archivo '{ARCHIVO_ORIGEN}' en la ruta: {path_origen}")
        sys.exit(1) # <-- Frenamos con error real para que Render nos avise

    # Corregido: Identación del print arreglada
    print(f"Leyendo origen de datos desde: {path_origen}...")
    
    # LÍNEA DE DIAGNÓSTICO:
    print(f"⚠️ [DEBUG RENDER] El tamaño real de 'data_limpio.csv' es: {os.path.getsize(path_origen)} bytes")
    
    df_raw = pd.read_csv(path_origen)
    
    # Tratamiento seguro de fechas
    if "mastery_lastPlayTime" in df_raw.columns:
        df_raw["mastery_lastPlayTime"] = pd.to_numeric(df_raw["mastery_lastPlayTime"], errors="coerce")
        df_raw["mastery_lastPlayTime"] = df_raw["mastery_lastPlayTime"].replace(0, np.nan)
        df_raw["mastery_lastPlayTime"] = pd.to_datetime(df_raw["mastery_lastPlayTime"], unit="ms", errors="coerce")
        df_raw["mastery_lastPlayTime"] = df_raw["mastery_lastPlayTime"].where(df_raw["mastery_lastPlayTime"].notnull(), None)

    if "start_utc" in df_raw.columns:
        df_raw["start_utc"] = pd.to_datetime(df_raw["start_utc"], errors="coerce")

    # 1. TABLA: Teams
    print("Cargando dimensión 'Teams'...")
    df_teams = df_raw[["team_name"]].dropna().drop_duplicates()
    df_teams.to_sql("Teams", con=engine, if_exists="append", index=False)

    # 2. TABLA: Champions
    print("Cargando dimensión 'Champions'...")
    df_champs = df_raw[["champion_id", "champion_name"]].dropna().drop_duplicates(subset=["champion_id"])
    df_champs.to_sql("Champions", con=engine, if_exists="append", index=False)

    # 3. TABLA: Games
    print("Cargando entidad 'Games'...")
    cols_games = ["game_id", "start_utc", "duration", "queue", "platform_id", "map_id", "game_mode", "game_version"]
    df_games = df_raw[cols_games].drop_duplicates(subset=["game_id"])
    
    # Reemplazo seguro de nulos antes de insertar en la base de datos cloud
    df_games = df_games.replace({np.nan: None})
    df_games.to_sql("Games", con=engine, if_exists="append", index=False)

    # Recuperar el mapa de IDs autoincrementales generados por la base de datos
    df_db_teams = pd.read_sql("SELECT team_id, team_name FROM Teams", con=engine)

    # 4. TABLA: GameTeams
    print("Cargando relación 'GameTeams'...")
    df_gt_raw = df_raw[["game_id", "team_name", "side"]].drop_duplicates(subset=["game_id", "side"])
    df_gameteams = pd.merge(df_gt_raw, df_db_teams, on="team_name", how="inner")[["game_id", "team_id", "side"]]
    df_gameteams.to_sql("GameTeams", con=engine, if_exists="append", index=False)

    # 5. TABLA: Participants
    print("Cargando detalle 'Participants'...")
    all_part_cols = [
        "participant_id", "game_id", "champion_id", "side", "position", "win",
        "kills", "deaths", "assists", "kda_ratio", "kill_participation", 
        "gold_earned", "gold_spent", "gold_per_min", "damage_dealt", "damage_per_min",
        "damage_to_champ", "damage_champ_per_min", "damage_taken", "vision_score",
        "item0", "item1", "item2", "item3", "item4", "item5", "item6",
        "solo_tier", "solo_rank", "solo_lp", "solo_wins", "solo_losses",
        "flex_tier", "flex_rank", "flex_lp", "flex_wins", "flex_losses",
        "mastery_level", "mastery_points", "mastery_lastPlayTime", 
        "mastery_pointsSinceLastLevel", "mastery_pointsUntilNextLevel", "mastery_tokens",
        "final_abilityHaste", "final_abilityPower", "final_armor", "final_attackDamage",
        "final_attackSpeed", "final_movementSpeed", "final_health", "final_healthMax",
        "final_lifesteal", "final_omnivamp", "final_power", "final_powerMax", "final_spellVamp"
    ]
    cols_presentes = [c for c in all_part_cols if c in df_raw.columns]
    df_part = pd.merge(df_raw[cols_presentes + ["team_name"]], df_db_teams, on="team_name", how="inner")
    df_part = df_part.drop_duplicates(subset=["game_id", "participant_id"])[cols_presentes + ["team_id"]]
    
    # Tratamiento robusto de vacíos para evitar que Aiven proteste con los tipos de datos
    df_part = df_part.replace({np.nan: None, 'None': None, 'nan': None})
    df_part.to_sql("Participants", con=engine, if_exists="append", index=False)

    # 6. TABLA: TeamStats
    print("Cargando métricas 'TeamStats'...")
    cols_stats = ["game_id", "side", "team_baronKills", "team_dragonKills", "team_towerKills", "team_champKills", "team_riftHeraldKills", "team_inhibitorKills"]
    df_ts_raw = df_raw[cols_stats + ["team_name"]].drop_duplicates(subset=["game_id", "side"])
    df_ts = pd.merge(df_ts_raw, df_db_teams, on="team_name", how="inner")[cols_stats + ["team_id"]]
    df_ts.to_sql("TeamStats", con=engine, if_exists="append", index=False)

if __name__ == "__main__":
    print("=== INICIANDO REINTENTO PIPELINE ===")
    try:
        run_etl()
        print("=== PROCESO FINALIZADO CON ÉXITO SIN ERRORES ===")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO DEL ETL]: {e}")
        sys.exit(1) # <-- Forzamos la salida con error para romper el despliegue si la BD falla
