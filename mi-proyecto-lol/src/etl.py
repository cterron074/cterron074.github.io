import os
import pandas as pd
from sqlalchemy import create_engine

def run_etl():
   script_dir = os.path.dirname(os.path.abspath(__file__))
    # Ruta al certificado que acabas de subir a GitHub
    cert_path = os.path.join(os.path.dirname(script_dir), "ca.pem")
    
    # URL de conexión incluyendo el parámetro del certificado
    
   db_url = "mysql+pymysql://avnadmin:AVNS_pu8DuuDDpatGY7euatj@mysql-mi-proyecto-lol.b.aivencloud.com:15368/defaultdb"
      engine = create_engine(db_url, connect_args={'ssl': None}) # Desactiva el SSL temporalmente
    path_origen = os.path.join(script_dir, "data_limpio.csv")
    
    # 2. Configuración de conexión (SQLAlchemy)
    # ¡Asegúrate de que estas credenciales sean las correctas de tu panel Aiven!
    db_url = "mysql+pymysql://avnadmin:AVNS_pu8DuuDDpatGY7euatj@mysql-mi-proyecto-lol.b.aivencloud.com:15368/defaultdb"
    engine = create_engine(db_url)
    
    # 3. Lectura del archivo limpio
    df = pd.read_csv(path_origen)
    
    # 4. Inyección a la base de datos
    print(f"Cargando {len(df)} filas en Aiven...")
    try:
        # if_exists='append' es clave para no borrar lo que ya tenías
        df.to_sql("Games", con=engine, if_exists="append", index=False)
        print("¡Carga exitosa a Aiven!")
    except Exception as e:
        print(f"Error al conectar con Aiven: {e}")

if __name__ == "__main__":
    run_etl()
