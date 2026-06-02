import os
import pandas as pd
from sqlalchemy import create_engine

# Tus credenciales de Aiven
DB_USER = "avnadmin"
DB_PASSWORD = "AVNS_pu8DuuDDpatGY7euatj"  
DB_HOST = "mysql-mi-proyecto-lol.b.aivencloud.com"
DB_PORT = "15368"
DB_NAME = "defaultdb"

def run_etl():
    # Ruta al archivo que generó preparar_etl.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_origen = os.path.join(base_dir, "data_limpio.csv")
    
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    df = pd.read_csv(path_origen)
    
    # Carga simple a la tabla 'Games' para probar la conexión
    # Si esto funciona, podemos añadir el resto de tablas después
    print("Intentando cargar datos en Aiven...")
    df.to_sql("Games_Test", con=engine, if_exists="replace", index=False)
    print("¡Carga exitosa!")

if __name__ == "__main__":
    run_etl()
