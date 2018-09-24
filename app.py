from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object('config')

@app.route('/yes', methods=['POST'])
def yes():
    return render_template('yes.html')

@app.route('/no', methods=['POST'])
def no():
    return render_template('no.html')

@app.route('/')
def index():
    return render_template('index.html')

