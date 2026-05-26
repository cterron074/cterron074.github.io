from flask import Flask, jsonify
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
app = Flask(__name__)

@app.route('/stats')
def stats():
    engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}")
    # Simulación de consulta
    return jsonify({"mensaje": "API conectada a tu BD de LoL"})

if __name__ == '__main__':
    app.run(debug=True)