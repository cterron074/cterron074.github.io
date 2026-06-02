import os
import pandas as pd

def adaptar_fichero_csv():
    # Usamos la ruta relativa al archivo actual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_entrada = os.path.join(base_dir, "data.csv")
    archivo_salida = os.path.join(base_dir, "data_limpio.csv")
    
    if not os.path.exists(archivo_entrada):
        print(f"Error: {archivo_entrada} no existe.")
        return

    df = pd.read_csv(archivo_entrada)
    
    # Limpieza mínima necesaria
    df = df.dropna(subset=["game_id", "participant_id"])
    
    # Guardamos el archivo limpio para que etl.py lo encuentre
    df.to_csv(archivo_salida, index=False)
    print(f"Archivo generado con éxito: {archivo_salida}")

if __name__ == "__main__":
    adaptar_fichero_csv()
