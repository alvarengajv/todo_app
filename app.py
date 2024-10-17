from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_list')
def list():
    return render_template('add_list.html')

if __name__ == '__main__':
    app.run(debug=True)