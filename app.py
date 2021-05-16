from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from validate import validate_data, defaults


# Initialise websever
app = Flask(__name__)

# CONTANTS
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


@app.route("/")
def home():
    return render_template("index.jinja2", server_url=BUGGY_RACE_SERVER_URL)


@app.route("/new", methods=["POST", "GET"])
def create_buggy():
    if request.method == "GET":
        return render_template("buggy-form.jinja2", data=defaults)
    elif request.method == "POST":

        msg = ""
        print(dict(request.form))
        return render_template("updated.jinja2", msg=msg)


@app.route("/buggy")
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone()
    return render_template("buggy.jinja2", buggy=record)


@app.route("/edit")
def edit_buggy():
    return render_template("buggy-form.jinja2")


@app.route("/json")
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(
        zip([column[0] for column in cur.description], cur.fetchone())
    ).items()
    return jsonify(dict(buggies))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
