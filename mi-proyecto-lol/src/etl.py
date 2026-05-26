import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def run_etl():
    engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}")
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.csv'))
    
    # Aquí iría tu lógica de carga a SQL
    print("Cargando datos a MySQL...")
    # df.to_sql('Participants', engine, if_exists='append', index=False)
    print("ETL Finalizado.")

if __name__ == "__main__":
    run_etl()