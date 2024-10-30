from flask import Flask
from config import Config
from web_routes import web_bp
from api_routes import api_bp
from database import init_db

app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False

init_db()

app.register_blueprint(web_bp)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
