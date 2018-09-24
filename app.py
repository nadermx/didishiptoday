from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from pony.orm import *
import models
from datetime import datetime
import redis

app = Flask(__name__)
app.config.from_object('config')

r = redis.StrictRedis(host='localhost', port=6379, db=0)

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
        anon_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not r.get(anon_ip):
            end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
            r.setex(anon_ip, 'visited_today', end_of_day)
            models.Ship(yes=True, dt_shipped=datetime.utcnow())
    today_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    shipped = models.select(s for s in models.Ship if s.dt_shipped > today_utc)
    yes = shipped.filter(lambda y: y.yes).count()
    no = shipped.filter(lambda n: n.no).count()
    return render_template('yes.html', shipped=shipped.count(), yes=yes, percent=int(yes)/int(shipped.count()))

@app.route('/no', methods=['POST'])
def no():
    if current_user.is_authenticated:
        models.Ship(no=True, user=models.User[current_user.id], dt_shipped=datetime.utcnow)
    else:
        anon_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not r.get(anon_ip):
            end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
            r.setex(anon_ip, 'visited_today', end_of_day)
            models.Ship(no=True, dt_shipped=datetime.utcnow())
    today_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    shipped = models.select(s for s in models.Ship if s.dt_shipped > today_utc)
    return render_template('no.html')

@app.route('/')
def index():
    return render_template('index.html')

