from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from flask_cors import CORS
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import sqlite3
from mobiles import mobiles

app = Flask(__name__)

app.secret_key = "infinix_secret_key"

CORS(app)


def create_database():

    conn = sqlite3.connect("auth.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()

create_database()


def get_db():

    conn = sqlite3.connect("auth.db")
    conn.row_factory = sqlite3.Row

    return conn


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user"] = user["username"]
            session["email"] = user["email"]

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not username or not email or not password:
            return render_template(
                "signup.html",
                error="All fields are required"
            )

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users(username, email, password) VALUES(?, ?, ?)",
                (username, email, generate_password_hash(password))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "signup.html",
                error="Email already registered"
            )
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/")
def home():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["user"],
        email=session["email"]
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )



@app.route("/mobiles")
def get_mobiles():

    if "user" not in session:

        return jsonify({
            "status": "unauthorized",
            "message": "Please login first"
        }), 401

    min_price = request.args.get(
        "min_price",
        default=0,
        type=int
    )

    max_price = request.args.get(
        "max_price",
        default=100000,
        type=int
    )

    ram = request.args.get(
        "ram",
        type=int
    )

    storage = request.args.get(
        "storage",
        type=int
    )

    result = []

    for mobile in mobiles:

        if not (
            min_price <= mobile["price"] <= max_price
        ):
            continue

        if ram is not None and mobile["ram"] != ram:
            continue

        if storage is not None and mobile["storage"] != storage:
            continue

        result.append(mobile)

    if len(result) == 0:

        return jsonify({
            "status": "not_found",
            "message": "No mobile found for this combination"
        })

    return jsonify({
        "status": "success",
        "count": len(result),
        "data": result
    })

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )