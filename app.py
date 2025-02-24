import os
import yt_dlp
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Get the user's Downloads folder path
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

def download_youtube_video(url, resolution="1080p"):
    resolution_map = {"1080p": "bv*+ba/b", "720p": "bv*[height<=720]+ba/b", "360p": "bv*[height<=360]+ba/b"}

    if resolution not in resolution_map:
        return None, f"Unsupported resolution: {resolution}"

    # Use a format that **already has video & audio merged**
    ydl_opts = {
        "format": f"{resolution_map[resolution]}[ext=mp4]/best[ext=mp4]",  # Fastest format with both video + audio
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,  # Only download a single video
        "quiet": True,  # Suppress console output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename, None
    except Exception as e:
        return None, str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    video_url = data.get("url")
    
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400

    for res in ["1080p", "720p", "360p"]:
        filename, error = download_youtube_video(video_url, res)
        if filename:
            return jsonify({"success": True, "message": f"Downloaded to {filename}"}), 200

    return jsonify({"success": False, "error": "Failed to download video."}), 500

if __name__ == "__main__":
    app.run(debug=True)