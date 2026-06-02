import os
import pandas as pd
from sqlalchemy import create_engine

def run_etl():
    # 1. Rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_origen = os.path.join(script_dir, "data_limpio.csv")
    
    # 2. Configuración de conexión
    # Usamos la conexión sin SSL temporalmente para descartar errores de certificado
    db_url = "mysql+pymysql://avnadmin:AVNS_pu8DuuDDpatGY7euatj@mysql-mi-proyecto-lol.b.aivencloud.com:15368/defaultdb"
    
    # Creamos el motor de conexión
    engine = create_engine(db_url, connect_args={'ssl': None})
    
    # 3. Lectura del archivo limpio
    if not os.path.exists(path_origen):
        print(f"Error: No se encuentra el archivo en {path_origen}")
        return

    df = pd.read_csv(path_origen)
    

  # 4. Inyección a la base de datos
    print(f"Cargando {len(df)} filas en Aiven...")
    try:
        with engine.connect() as conn:
            # Estas líneas deben estar indentadas (con más espacio a la izquierda)
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            # Nota: Si tu tabla se llama 'Games', asegúrate de que el nombre sea correcto
            conn.execute(text("DROP TABLE IF EXISTS Games;"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            
        # El to_sql va fuera del 'with' o dentro, pero correctamente alineado
        df.to_sql("Games", con=engine, if_exists="replace", index=False)
        print("¡Carga exitosa a Aiven!")
        
    except Exception as e:
        print(f"Error al conectar o insertar en Aiven: {e}")
