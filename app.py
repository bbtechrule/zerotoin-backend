from flask import Flask, request, jsonify

app = Flask(__name__)

videos = []

@app.route("/")
def home():
    return "Zerotoin Backend Running Successfully!"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    title = data.get("title")
    link = data.get("link")

    videos.append({
        "title": title,
        "link": link
    })

    return jsonify({"message": "Video uploaded successfully!"})

@app.route("/videos")
def get_videos():
    return jsonify(videos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)