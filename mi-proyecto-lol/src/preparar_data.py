import os
import pandas as pd

# Ruta dinámica hacia la carpeta data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'data.csv')

def limpiar():
    if not os.path.exists(DATA_PATH):
        print(f"Error: No se encuentra {DATA_PATH}")
        return
    
    df = pd.read_csv(DATA_PATH)
    # Ejemplo de limpieza básica
    df = df.dropna(subset=['game_id'])
    df.to_csv(DATA_PATH, index=False)
    print("Archivo data.csv limpio y listo.")

if __name__ == "__main__":
    limpiar()