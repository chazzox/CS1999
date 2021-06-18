import copy
from flask import Flask, render_template, request, jsonify, redirect
import sqlite3 as sql
from functools import wraps
from validate import database_friendly, validate_data, calc_price
from constants import DEFAULTS, DATABASE_FILE

# Initialise websever
app = Flask(__name__)
# Means that the jsonify function does not sort keys alphabetically and keeps the nice order
app.config["JSON_SORT_KEYS"] = False


# Decorator function used to ensure session cookie
def cookie_required(func):
    @wraps(func)
    def check_cookie(*args, **kwargs):
        if "session" not in request.cookies:
            return render_template("login.jinja"), 401
        return func(*args, **kwargs)

    return check_cookie


@app.route("/")
@cookie_required
def home():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    buggies = cur.fetchall()
    return render_template("buggies.jinja", buggies=buggies)


@app.route("/new", methods=["POST", "GET"])
@cookie_required
def create_buggy():
    if request.method == "GET":
        return render_template("buggy-form.jinja", data=DEFAULTS, url="/new")

    elif request.method == "POST":
        # Validating, msg will become either the validated and converted form data or the error message, and isValid is a boolean
        isValid, msg = validate_data(request.form)
        # Assuming validation passes
        status = 200
        if isValid:
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            keys = ", ".join([*DEFAULTS.keys(), "total_cost"])
            values = ", ".join(
                map(lambda a: str(database_friendly(a)), [*msg.values(), calc_price(msg)])
            )
            try:
                cur.execute(f"INSERT INTO buggies ({keys}) VALUES ({values})")
                con.commit()
                msg = "Record successfully saved"
            except Exception as e:
                con.rollback()
                print(repr(e))
                msg = "Error in update operation"
                status = 400
            finally:
                con.close()
        else:
            status = 400
        return render_template("updated.jinja", msg=msg, success=isValid), status


@app.route("/delete/<buggy_id>", methods=["POST", "GET"])
@cookie_required
def del_buggy(buggy_id):
    if request.method == "POST":
        con = sql.connect(DATABASE_FILE)
        con.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
        con.commit()
        return redirect("/")
    elif request.method == "GET":
        return page_not_found(404)


@app.route("/edit/<buggy_id>", methods=["POST", "GET"])
@cookie_required
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
        buggy_db = cur.fetchone()
        if buggy_db:
            # Copying dict and overwritting the defaults with the buggy values
            return render_template(
                "buggy-form.jinja",
                data={
                    k: {**v, "defaults": dict(buggy_db)[k]}
                    for (k, v) in copy.deepcopy(DEFAULTS).items()
                },
                url=f"/edit/{buggy_id}",
            )
        else:
            return page_not_found(404)
    elif request.method == "POST":
        isValid, msg = validate_data(request.form)
        if isValid:
            update_keys = ", ".join(map(lambda a: a + "=?", [*DEFAULTS.keys(), "total_cost"]))
            try:
                cur.execute(
                    f"UPDATE buggies set {update_keys} WHERE id=?",
                    (
                        *msg.values(),
                        calc_price(msg),
                        buggy_id,
                    ),
                )
                con.commit()
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect("/")


# TODO: make buggy json's locked to the og user
@app.route("/json/<buggy_id>")
def json(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
    record = cur.fetchone()
    return jsonify(dict(record or {}))


# TODO: when users are implemented only return buggies that match the user ID
@app.route("/json")
def jsonAll():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    buggies = cur.fetchall()
    return jsonify(list((dict(buggy) for buggy in buggies)))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja"), 404


@app.route("/poster")
def poster():
    return render_template("poster.jinja")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

"""
Session Functionality:
- Session 'Token'
    - Secret 
    - Validate the token server side
    - Store part of token on client (JS?)
    - Expiration of token
- Ability to log out/in
- Block edit access based on token expiration/validity

step 1 - protect routes
    require that request has a secret
"""
