import shutil
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from db import db
from models import Note, Timing
import time
from check_timing import CheckTimingThreading
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)

app.add_template_global(utils.strftime, "strftime")

check_threading = CheckTimingThreading(Timing, db, app)
check_threading.start()

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)

@app.route("/notes", methods=['POST', 'PUT', "DELETE"])
def notes_operate():
    if request.method == "POST":
        content = request.form.get("content")
        note = Note(content=content)
        db.session.add(note)
        db.session.commit()

        return redirect(url_for("index"))
    elif request.method == "PUT":
        id = request.form.get("id", type=int)
        content = request.form.get("content")
        note = Note.query.get(id)
        note.content = content

        db.session.add(note)
        db.session.commit()

        return {"success": True}
    elif request.method == "DELETE":
        notes_id = request.form.get("id", type=int)
        db.session.delete(Note.query.get(notes_id))

        return {"success": True}
    
@app.route('/add_notes', methods=['GET'])
def add_notes():
    return render_template("add_notes.html")

@app.route("/update-notes", methods=['GET'])
def update_notes():
    id = request.args.get("id", type=int)
    note = Note.query.get(id)
    
    return render_template("update_notes.html", note=note)

@app.route('/timings', methods=['GET', 'POST', "DELETE"])
def timings():
    if request.method == 'GET':
        timings_list = Timing.query.all()
        return render_template("timings.html", timings=timings_list)
    elif request.method == "POST":
        timing = request.form.get("timing-mins", type=int)
        notes_id = request.form.get("notes_id", type=int)
        try:
            if timing < 0 or timing > 60:
                raise Exception
            timing = timing*60 + int(time.time())
        except:
            return jsonify({"code": 400}), 400
        else:
            print(Note.query.get(notes_id))
            timing_obj = Timing(timestamp=timing, notes=Note.query.get(notes_id))
            db.session.add(timing_obj)
            db.session.commit()

            return jsonify({"code": 201}), 201
    elif request.method == "DELETE":
        timing_id = request.form.get("id", type=int)
        
        db.session.delete(Timing.query.get(timing_id))
        db.session.commit()

        return jsonify({"code": 204}), 204

@app.route('/project/', methods=['GET'])
def project():
    return render_template("project/project.html")

@app.route("/backup-db", methods=['GET', "DELETE"])
def backup_db():
    if request.method == "DELETE":
        db_filename = request.form.get("db_file", type=str)
        os.delete("backup/database/{}".format(db_filename))
        return jsonify({"success": True})
    backup_id = int(time.time())
    shutil.copyfile("notes.db", "backup/database/{}.db".format(backup_id))
    return jsonify({"success": True, "id": backup_id})
    
@app.route("/project/backup-db")
def backup_db_page():
    db_files = os.listdir("backup/database")
    return render_template("project/backup_db.html", db_files=db_files)

if __name__ == "__main__":
    app.run("localhost", 8888, debug=True)
