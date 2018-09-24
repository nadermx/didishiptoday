from flask import Flask, render_template
from flask_login import LoginManager, current_user
from pony.orm import *
import models

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return models.User.get(id=id)

@login.unauthorized_handler
def unauthorized():
    return 401

@app.route('/yes', methods=['POST'])
def yes():
    if current_user.is_authenticated:
        print('yes')
    else:
        print('no')
    # shipped = models.select(s for s in models.Shipped)
    return render_template('yes.html')

@app.route('/no', methods=['POST'])
def no():
    return render_template('no.html')

@app.route('/')
def index():
    return render_template('index.html')

