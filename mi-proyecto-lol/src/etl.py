import os
import pandas as pd

def adaptar_fichero_csv():
    # Obtiene el directorio donde está este archivo (src)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Busca 'data.csv' directamente en 'src'
    archivo_entrada = os.path.join(script_dir, "data.csv")
    archivo_salida = os.path.join(script_dir, "data_limpio.csv")
    
    print(f"Buscando archivo en: {archivo_entrada}")
    
    if not os.path.exists(archivo_entrada):
        print(f"Error: No se encuentra el archivo en {archivo_entrada}")
        return

    df = pd.read_csv(archivo_entrada)
    df = df.dropna(subset=["game_id", "participant_id"])
    df.to_csv(archivo_salida, index=False)
    print("Archivo 'data_limpio.csv' generado correctamente.")

if __name__ == "__main__":
    adaptar_fichero_csv()
