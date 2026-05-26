import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configuración de rutas para cargar las variables de entorno (.env)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)
# CORS permite que tu HTML/JS (Frontend) consulte esta API sin bloqueos de seguridad
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
# ENDPOINT 1: RESUMEN GENERAL (KPIs para tarjetas estáticas)
# ----------------------------------------------------
@app.route('/api/general-stats', methods=['GET'])
def get_general_stats():
    query = text("""
        SELECT 
            (SELECT COUNT(*) FROM Games) as total_games,
            (SELECT COUNT(*) FROM Champions) as total_champions,
            (SELECT ROUND(AVG(duration) / 60, 1) FROM Games) as avg_duration_minutes
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            return jsonify(dict(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# ENDPOINT 2: TOP CAMPEONES MÁS JUGADOS (Para gráficos de barras/torta)
# ----------------------------------------------------
@app.route('/api/top-champions', methods=['GET'])
def get_top_champions():
    query = text("""
        SELECT 
            c.champion_name,
            COUNT(p.game_id) as games_played,
            ROUND(AVG(p.kills), 1) as avg_kills,
            ROUND(AVG(p.deaths), 1) as avg_deaths,
            ROUND(AVG(p.assists), 1) as avg_assists,
            ROUND(SUM(CASE WHEN p.win = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(p.game_id), 1) as win_rate
        FROM Participants p
        JOIN Champions c ON p.champion_id = c.champion_id
        GROUP BY c.champion_id, c.champion_name
        ORDER BY games_played DESC
        LIMIT 6
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# ENDPOINT 3: RENDIMIENTO POR ROL/POSICIÓN (Para gráficos de radar)
# ----------------------------------------------------
@app.route('/api/stats-by-role', methods=['GET'])
def get_stats_by_role():
    query = text("""
        SELECT 
            position,
            COUNT(game_id) as games_played,
            ROUND(SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(game_id), 1) as win_rate,
            ROUND(AVG(kills), 1) as avg_kills,
            ROUND(AVG(deaths), 1) as avg_deaths,
            ROUND(AVG(assists), 1) as avg_assists
        FROM Participants
        WHERE position IN ('TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT')
        GROUP BY position
        ORDER BY games_played DESC
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# ENDPOINT 4: HISTORIAL DE PARTIDAS RECIENTES (Para tablas en el portfolio)
# ----------------------------------------------------
@app.route('/api/recent-matches', methods=['GET'])
def get_recent_matches():
    query = text("""
        SELECT 
            g.game_id,
            g.start_utc,
            ROUND(g.duration / 60, 0) as duration_minutes,
            g.game_mode,
            c.champion_name,
            p.position,
            p.kills,
            p.deaths,
            p.assists,
            p.win
        FROM Games g
        JOIN Participants p ON g.game_id = p.game_id
        JOIN Champions c ON p.champion_id = c.champion_id
        ORDER BY g.start_utc DESC
        LIMIT 10
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ejecuta el servidor local en modo desarrollo en el puerto 5000
   app.run(host='0.0.0.0', port=8085, debug=True, use_reloader=False)
   @app.route('http://localhost:8085/api/stats', methods=['GET'])