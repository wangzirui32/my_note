import shutil
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from db import conn_db
import time
from check_timing import CheckTimingThreading
import utils

app = Flask(__name__)
app.config['DATABASE'] = "notes.db"

db_query = conn_db(app)

app.add_template_global(utils.strftime, "strftime")

check_threading = CheckTimingThreading(db_query)
check_threading.start()

@app.route("/")
def index():
    notes = db_query.select("id, content", "notes")
    return render_template("index.html", notes=notes)

@app.route("/notes", methods=['POST', 'PUT', "DELETE"])
def notes_operate():
    if request.method == "POST":
        content = request.form.get("content")
        db_query.insert("notes", "id, content", "{}, '{}'".format(int(time.time()), content))

        return redirect(url_for("index"))
    elif request.method == "PUT":
        id = request.form.get("id", type=int)
        content = request.form.get("content")
        db_query.update("notes", "content='{}'".format(content), "id={}".format(id))

        return {"success": True}
    elif request.method == "DELETE":
        notes_id = request.form.get("id")
        db_query.delete("notes", "id={}".format(notes_id))

        return {"success": True}
    
@app.route('/add_notes', methods=['GET'])
def add_notes():
    return render_template("add_notes.html")

@app.route("/update-notes", methods=['GET'])
def update_notes():
    id = request.args.get("id", type=int)
    notes = list(db_query.select("id, content", "notes", "id={}".format(id)))[0]
    notes_id = notes[0]
    notes_content = notes[1]
    
    return render_template("update_notes.html", notes_id=notes_id, notes_content=notes_content)

@app.route("/add-timing", methods=['POST'])
def add_timing():
    timing = request.form.get("timing-mins", type=int)
    notes_id = request.form.get("notes_id", type=int)
    try:
        if timing < 0 or timing > 60:
            raise Exception
        timing = timing*60 + int(time.time())
    except:
        return jsonify({"code": 400}), 400
    else:
        db_query.insert("timings", "id, timestamp, notes_id", "{}, '{}', {}".format(int(time.time()), timing, notes_id))

        return jsonify({"code": 201}), 201

@app.route('/timings', methods=['GET', 'POST', "DELETE"])
def timings():
    if request.method == 'GET':
        timings_list = db_query.select("id, timestamp, notes_id", "timings")
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
            db_query.insert("timings", "id, timestamp, notes_id", "{}, '{}', {}".format(int(time.time()), timing, notes_id))

            return jsonify({"code": 201}), 201
    elif request.method == "DELETE":
        timing_id = request.form.get("id", type=int)
        db_query.delete("timings", "id={}".format(timing_id))
        return jsonify({"code": 204}), 204

@app.route('/project/', methods=['GET'])
def project():
    return render_template("project/project.html")

@app.route("/backup-db", methods=['GET', "DELETE"])
def backup_db():
    if request.method == "DELETE":
        db_filename = request.form.get("db_file", type=str)
        os.remove("backup/database/{}".format(db_filename))
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
    db_query.close()
