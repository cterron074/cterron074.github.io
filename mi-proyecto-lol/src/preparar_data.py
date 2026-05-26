import os
import pandas as pd

def adaptar_fichero_csv():
    # Definimos la ruta exacta que usas
    ruta_directorio = r"C:\etl\data"
    archivo_entrada = os.path.join(ruta_directorio, "data.csv")
    
    if not os.path.exists(archivo_entrada):
        print(f"[Error] No se encontró el archivo en la ruta: {archivo_entrada}")
        return

    print(f"-> Cargando {archivo_entrada} en memoria...")
    df = pd.read_csv(archivo_entrada)
    original_rows = len(df)
    
    print("-> Limpiando registros corruptos o sin ID...")
    df = df.dropna(subset=["game_id", "participant_id"])
    
    print("-> Adaptando columnas y creando campos relacionales...")
    # 1. Crear el bando (BLUE para participantes 1-5, RED para 6-10)
    df['side'] = df['participant_id'].apply(lambda x: 'BLUE' if int(x) <= 5 else 'RED')
    
    # 2. Asignar nombres estables de equipo
    df['team_name'] = df['side'].apply(lambda x: 'Blue Team' if x == 'BLUE' else 'Red Team')
    
    # 3. Validar la columna 'position' (añadiendo soporte para 'SUPPORT')
    if 'position' in df.columns:
        df['position'] = df['position'].astype(str).str.upper().str.strip()
        df['position'] = df['position'].replace({'SUPPORT': 'SUPPORT', 'UTILITY': 'UTILITY', 'N/A': 'UTILITY', 'NAN': 'UTILITY'})
        valid_positions = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT', 'UTILITY']
        df['position'] = df['position'].apply(lambda x: x if x in valid_positions else 'UTILITY')
    
    # 4. Forzar tipos de datos correctos para MySQL
    if 'win' in df.columns:
        df['win'] = df['win'].astype(str).str.upper().str.strip()
        df['win'] = df['win'].apply(lambda x: True if 'TRUE' in x or '1' in x else False)

    if 'mastery_lastPlayTime' in df.columns:
        df['mastery_lastPlayTime'] = pd.to_numeric(df['mastery_lastPlayTime'], errors='coerce').fillna(0)
    
    df['game_id'] = df['game_id'].astype(int)
    df['participant_id'] = df['participant_id'].astype(int)
    df['champion_id'] = df['champion_id'].astype(int)
    
    # 5. Limpiar nulos de texto para evitar conflictos con MySQL
    columnas_texto = ['solo_tier', 'solo_rank', 'flex_tier', 'flex_rank', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).replace({'N/A': None, 'NaN': None, 'nan': None, 'None': None})
            
    print(f"-> Guardando archivo modificado en: {archivo_entrada}")
    df.to_csv(archivo_entrada, index=False)
    print(f"¡Proceso completado! Se procesaron {original_rows} líneas y se actualizó con éxito el fichero.")

if __name__ == "__main__":
    adaptar_fichero_csv()