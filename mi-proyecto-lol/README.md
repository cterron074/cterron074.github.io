#🚀 ETL LolRanked S15
#Este proyecto implementa un proceso ETL (Extract, Transform, Load) diseñado para procesar datos masivos de partidas clasificatorias de League of Legends 
# (Temporada 15) desde un archivo CSV hacia una base de datos relacional MySQL.

#📋 Descripción
El objetivo de este sistema es normalizar datos brutos de partidas en un esquema relacional estructurado, permitiendo realizar consultas complejas sobre campeones, 
#rendimiento de jugadores y estadísticas por equipo.

#🛠️ Tecnologías Utilizadas
Python 3.x
Pandas: Para la limpieza y transformación de datos.
SQLAlchemy: Como ORM para la interacción con la base de datos.
MySQL: Motor de base de datos relacional.
Flask: (Opcional) API para servir los datos a tu front-end.

⚙️ Configuración del Entorno
Clonar el repositorio:

Bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
Crear entorno virtual e instalar dependencias:

Bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# Instalar requisitos:
pip install -r requirements.txt
Configuración de Variables de Entorno:
Crea un archivo .env en la raíz del proyecto y añade tus credenciales:

Plaintext
DB_USER=root
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_NAME=lol_ranked_s15
🚀 Cómo ejecutar el Pipeline
Preparar la Base de Datos:
Ejecuta el script /sql/creacion_db.sql en tu gestor de MySQL para inicializar las tablas necesarias.

Limpieza de datos:
Asegúrate de colocar tu data.csv en la carpeta C:\etl\data y ejecuta:

Bash
python preparar_data.py
Carga (ETL):
Ejecuta el script principal para poblar tu base de datos:

Bash
python etl.py
📈 Visualización (API)
Si deseas mostrar estos datos en un portfolio, el proyecto incluye una API básica con Flask.

Ejecutar API: python app.py

El servidor se iniciará en http://127.0.0.1:5000 y servirá los datos en formato JSON para tu frontend.

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras un error o quieres añadir nuevas métricas (como análisis de vision score avanzado), por favor, abre un Issue o envía un Pull Request.

Desarrollado para fines académicos y de análisis estadístico. No afiliado con Riot Games.

Un último consejo:
Para que GitHub muestre el archivo README.md correctamente, asegúrate de que el nombre del archivo sea exactamente README.md (en mayúsculas) y que esté en la raíz de tu carpeta. ¡Con esta estructura, tu portfolio se verá muy profesional para cualquier reclutador!
