from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from validate import validate_data, defaults


# Initialise websever
app = Flask(__name__)

# CONTANTS
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"


# create a dict using key:validation from the defaults dict
validation_dict = dict(map(lambda a: [a[0], a[1]["validation"]], defaults.items()))


@app.route("/")
def home():
    return render_template("index.jinja", server_url=BUGGY_RACE_SERVER_URL)


@app.route("/new", methods=["POST", "GET"])
def create_buggy():
    if request.method == "GET":
        return render_template("buggy-form.jinja", data=defaults)
    elif request.method == "POST":
        # validating, msg will become either the validated and converted form data or the error message, and isValid is a boolean
        isValid, msg = validate_data(dict(request.form), validation_dict)
        if isValid:
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    update_values = ", ".join(map(lambda a: a + "=?", defaults.keys()))
                    print(f"UPDATE buggies set {update_values} WHERE id=?")
                    cur.execute(
                        f"UPDATE buggies set {update_values} WHERE id=?",
                        (*msg.values(), DEFAULT_BUGGY_ID),
                    )
                    con.commit()
                    msg = "Record successfully saved"
            except Exception as e:
                print(e)
                con.rollback()
                msg = "Error in update operation"
            finally:
                con.close()
        # update code
        return render_template("updated.jinja", msg=msg)


@app.route("/buggy")
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone()
    return render_template("buggy.jinja", buggy=record)


@app.route("/edit")
def edit_buggy():
    return render_template("buggy-form.jinja")


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
    return render_template("404.jinja"), 404


@app.route("/poster")
def poster():
    return render_template("poster.jinja")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
