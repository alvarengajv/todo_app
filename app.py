from flask import Flask, render_template
from config import Config
from database import init_db
from models import Lista, Tarefa
from routes import api_bp, init_api  

app = Flask(__name__)

app.config.from_object(Config)

session = init_db(app)

init_api(app)

app.register_blueprint(api_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_list')
def add_list():
    return render_template('add_list.html')

@app.route('/add_task')
def add_task():
    return render_template('add_task.html')

if __name__ == '__main__':
    app.run(debug=True)
