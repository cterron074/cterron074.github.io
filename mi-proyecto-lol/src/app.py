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
@app.route('/api/stats', methods=['GET'])
def get_all_stats():
    """Endpoint único que consolida todas las consultas para evitar múltiples peticiones"""
    try:
        with engine.connect() as conn:
            # 1. KPIs Generales
            res1 = conn.execute(text("SELECT COUNT(*) as total_games, (SELECT COUNT(*) FROM Champions) as total_champions, (SELECT ROUND(AVG(duration)/60, 1) FROM Games) as avg_duration FROM Games")).mappings().first()
            
            # 2. Top Campeones
            res2 = conn.execute(text("SELECT c.champion_name, COUNT(p.game_id) as games_played FROM Participants p JOIN Champions c ON p.champion_id = c.champion_id GROUP BY c.champion_name ORDER BY games_played DESC LIMIT 6")).mappings().all()
            
            # 3. Stats por Rol
            res3 = conn.execute(text("SELECT position, ROUND(SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(game_id), 1) as win_rate FROM Participants WHERE position IN ('TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT') GROUP BY position")).mappings().all()
            
            # 4. Mejor Campeón
            res4 = conn.execute(text("SELECT c.champion_name, ROUND(SUM(p.win)*100.0/COUNT(p.game_id), 1) as win_rate FROM Participants p JOIN Champions c ON p.champion_id = c.champion_id GROUP BY c.champion_name HAVING COUNT(p.game_id) >= 10 ORDER BY win_rate DESC LIMIT 1")).mappings().first()
            
            # 5. Victorias Totales
            res5 = conn.execute(text("SELECT COUNT(*) as total_wins FROM Games WHERE win = 1")).mappings().first()

            return jsonify({
                "general": dict(res1),
                "top_champions": [dict(r) for r in res2],
                "roles": [dict(r) for r in res3],
                "best_champ": dict(res4) if res4 else {},
                "wins": dict(res5)
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
