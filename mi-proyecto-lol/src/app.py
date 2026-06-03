import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configuración de rutas para cargar las variables de entorno (.env)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)
# CORS permite que tu frontend consulte esta API
CORS(app)

# Configuración de la conexión a la base de datos MySQL
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tu_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "lol_ranked_s15")

CONNECTION_STRING = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(CONNECTION_STRING)

# ----------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------
# ----------------------------------------------------
# NUEVOS ENDPOINTS PARA MÉTRICAS ADICIONALES
# ----------------------------------------------------

@app.route('/api/best-champion', methods=['GET'])
def get_best_champion():
    # Campeón con mejor win_rate y al menos 10 partidas jugadas
    query = text("""
        SELECT 
            c.champion_name,
            ROUND(SUM(p.win) * 100.0 / COUNT(p.game_id), 1) as win_rate
        FROM Participants p
        JOIN Champions c ON p.champion_id = c.champion_id
        GROUP BY c.champion_name
        HAVING COUNT(p.game_id) >= 10
        ORDER BY win_rate DESC
        LIMIT 1
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            return jsonify(dict(result) if result else {"champion_name": "N/A", "win_rate": 0}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/win-summary', methods=['GET'])
def get_win_summary():
    # Total de victorias globales
    query = text("""
        SELECT COUNT(*) as total_wins 
        FROM Games 
        WHERE win = 1
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            return jsonify(dict(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Puerto dinámico para Render
    port = int(os.environ.get("PORT", 8085))
    app.run(host='0.0.0.0', port=port)
