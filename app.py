from flask import Flask, render_template, request, jsonify, redirect
import sqlite3 as sql
from validate import database_friendly, validate_data, defaults, calc_price


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
        return render_template("buggy-form.jinja", data=defaults, url="/new")
    elif request.method == "POST":
        # validating, msg will become either the validated and converted form data or the error message, and isValid is a boolean
        isValid, msg = validate_data(dict(request.form), validation_dict)
        # TODO: still *some* validation steps not implemented, do em
        # update code
        if isValid:
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    keys = ", ".join([*defaults.keys(), "total_cost"])
                    values = ", ".join(
                        map(
                            lambda a: str(database_friendly(a)),
                            [*msg.values(), calc_price(msg)],
                        )
                    )
                    cur.execute(f"INSERT INTO buggies ({keys}) VALUES ({values})")
                    con.commit()
                    msg = "Record successfully saved"
            except Exception as e:
                con.rollback()  # type: ignore
                print(e)
                msg = "Error in update operation"
            finally:
                con.close()
        return render_template("updated.jinja", msg=msg)


@app.route("/buggies")
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    buggies = cur.fetchall()
    return render_template("buggy.jinja", buggies=buggies)


@app.route("/delete/<buggy_id>", methods=["POST", "GET"])
def del_buggy(buggy_id):
    if request.method == "POST":
        con = sql.connect(DATABASE_FILE)
        con.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
        con.commit()
        return redirect("/buggies")
    elif request.method == "GET":
        return page_not_found(404)


@app.route("/edit/<buggy_id>", methods=["POST", "GET"])
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    if request.method == "GET":

        cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
        buggy_db = cur.fetchone()
        if buggy_db:
            record = dict(buggy_db)
            new_defaults = dict(defaults.copy())
            for i in new_defaults:
                new_defaults[i]["defaults"] = record[i]
            return render_template(
                "buggy-form.jinja", data=new_defaults, url=f"/edit/{buggy_id}"
            )
        else:
            # if the buggy with that id is not in the database, render the 404 site
            return page_not_found(404)
    elif request.method == "POST":
        print("trying to update", buggy_id)
        # validating, msg will become either the validated and converted form data or the error message, and isValid is a boolean
        isValid, msg = validate_data(dict(request.form), validation_dict)
        # update code
        if isValid:
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    update_values = ", ".join(
                        map(lambda a: a + "=?", [*defaults.keys(), "total_cost"])
                    )
                    cur.execute(
                        f"UPDATE buggies set {update_values} WHERE id=?",
                        (*msg.values(), calc_price(msg), buggy_id),
                    )
                    con.commit()
                    msg = "Record successfully saved"
            except Exception as e:
                con.rollback()  # type: ignore
                print(e)
                msg = "Error in update operation"
            finally:
                con.close()
        return redirect("/buggies")


@app.route("/json/<buggy_id>")
def json(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
    record = cur.fetchone()
    return jsonify(dict(record or {}))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja"), 404


@app.route("/poster")
def poster():
    return render_template("poster.jinja")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
