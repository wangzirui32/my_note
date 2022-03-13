from multiprocessing.spawn import import_main_path
from db import db
from models import Timing
from flask import Flask
from check_timing import CheckTimingThreading
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
app.add_template_global(utils.strftime, "strftime")

check_threading = CheckTimingThreading(Timing, db, app)
check_threading.start()

from views import *

if __name__ == "__main__":
    app.run("localhost", 8888, debug=True)
