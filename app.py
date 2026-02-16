from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

users = []
videos = []

@app.route("/")
def home():
    return jsonify({"status": "Backend Running Successfully"})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    users.append(data)
    return jsonify({"success": True})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    for u in users:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            return jsonify({"success": True, "role": u["role"]})
    return jsonify({"success": False})

@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.json
    videos.append(data)
    return jsonify({"success": True})

@app.route("/api/videos")
def get_videos():
    return jsonify(videos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
