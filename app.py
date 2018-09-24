from flask import Flask, render_template
from flask_login import LoginManager, current_user
from pony.orm import *
import models
from datetime import datetime

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
        models.Ship(yes=True, user=models.User[current_user.id], dt_shipped=datetime.utcnow)
    else:
        models.Ship(yes=True, dt_shipped=datetime.utcnow())
    today_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    shipped = models.select(s for s in models.Ship if s.dt_shipped > today_utc)
    return render_template('yes.html', shipped=shipped)

@app.route('/no', methods=['POST'])
def no():
    return render_template('no.html')

@app.route('/')
def index():
    return render_template('index.html')

