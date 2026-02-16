from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "database.db"

def db():
    return sqlite3.connect(DB)

def init_db():
    conn = db()
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

@app.route("/")
def home():
    return jsonify({"status": "Backend Running"})

# ---------------- AUTH ------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                    (data["name"], data["email"], data["password"], data["role"]))
        conn.commit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "error": "Email exists"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE email=? AND password=?",
                (data["email"], data["password"]))
    row = cur.fetchone()
    if row:
        return jsonify({"success": True, "role": row[0]})
    return jsonify({"success": False})

# ---------------- ADMIN ------------------

@app.route("/api/admin/users")
def admin_users():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,role FROM users")
    users = cur.fetchall()
    return jsonify({"users": users})

@app.route("/api/admin/videos")
def admin_videos():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id,title,url FROM videos")
    videos = cur.fetchall()
    return jsonify({"videos": videos})

@app.route("/api/admin/delete-user/<int:id>")
def delete_user(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    return jsonify({"success": True})

@app.route("/api/admin/delete-video/<int:id>")
def delete_video(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM videos WHERE id=?", (id,))
    conn.commit()
    return jsonify({"success": True})

# ---------------- VIDEOS ------------------

@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.json
    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO videos(title,url) VALUES(?,?)",
                (data["title"], data["url"]))
    conn.commit()
    return jsonify({"success": True})

@app.route("/api/videos")
def videos():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT title,url FROM videos")
    rows = cur.fetchall()
    return jsonify({"videos": [{"title": r[0], "url": r[1]} for r in rows]})

if __name__ == "__main__":
    app.run()
