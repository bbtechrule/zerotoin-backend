from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "database.db"

# ---------- DATABASE ----------

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT
    )""")

    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------

@app.route("/")
def home():
    return jsonify({"status": "Backend Running Successfully"})

# ---------- AUTH ----------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (data["name"], data["email"], data["password"], data["role"])
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Registered successfully"})
    except:
        return jsonify({"success": False, "message": "Email already exists"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({"success": True, "role": row[0]})
    return jsonify({"success": False, "message": "Invalid credentials"})

# ---------- VIDEO ----------

@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.json
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO videos(title,url) VALUES(?,?)",
        (data["title"], data["url"])
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/api/videos")
def videos():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT title,url FROM videos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return jsonify({
        "videos": [{"title": r[0], "url": r[1]} for r in rows]
    })

# ---------- RUN ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
