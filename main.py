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
import sqlite3

from mobiles import mobiles

# ==========================
# APP SETUP
# ==========================

app = Flask(__name__)

app.secret_key = "infinix_secret_key"

CORS(app)

# ==========================
# SQLITE DATABASE
# ==========================

DATABASE = "users.db"


def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def create_table():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


create_table()

# ==========================
# SIGNUP
# ==========================


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        conn = get_db_connection()

        existing_user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:

            conn.close()

            return "User already exists"

        conn.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (username, email, password)
        )

        conn.commit()

        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user"] = user["username"]

            return redirect(url_for("home"))

        return "Invalid Email or Password"

    return render_template("login.html")


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["user"]
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================
# MOBILE FILTER API
# ==========================

@app.route("/mobiles")
def get_mobiles():

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

        "data": result

    })


# ==========================
# VIEW USERS (OPTIONAL)
# ==========================

@app.route("/users")
def view_users():

    conn = get_db_connection()

    users = conn.execute(
        "SELECT id, username, email FROM users"
    ).fetchall()

    conn.close()

    user_list = []

    for user in users:

        user_list.append({

            "id": user["id"],

            "username": user["username"],

            "email": user["email"]

        })

    return jsonify(user_list)


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)

app = app