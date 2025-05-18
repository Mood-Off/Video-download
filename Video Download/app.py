from flask import Flask, request, render_template
from pytubefix import YouTube
import os
from utils import (
    ensure_download_folder,
    sanitize_filename,
    get_today_folder,
    clean_old_downloads
)

app = Flask(__name__)
ensure_download_folder()
clean_old_downloads("downloads")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a YouTube URL.")
        try:
            yt = YouTube(url)
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            resolutions = [stream.resolution for stream in streams if stream.resolution]
            resolutions = list(dict.fromkeys(resolutions))  # remove duplicates

            return render_template("index.html", url=url, resolutions=resolutions, step="select")
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    resolution = request.form.get("resolution")

    if not url or not resolution:
        return render_template("index.html", error="Missing URL or resolution.")

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if not stream:
            return render_template("index.html", error="Selected resolution not available.")

        safe_title = sanitize_filename(yt.title)
        download_path = get_today_folder()
        filename = stream.download(output_path=download_path, filename=f"{safe_title}.mp4")

        return render_template("index.html", success=True, title=yt.title,
                               filename=os.path.basename(filename), path=download_path)
    except Exception as e:
        return render_template("index.html", error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)