import os
import re
import time
from datetime import datetime

DOWNLOAD_DIR = "downloads"

def ensure_download_folder():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def get_today_folder():
    date_folder = datetime.now().strftime("%Y-%m-%d")
    full_path = os.path.join(DOWNLOAD_DIR, date_folder)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def clean_old_downloads(folder, max_age_hours=24):
    now = time.time()
    cutoff = now - (max_age_hours * 3600)
    for root, dirs, files in os.walk(folder):
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.getmtime(file_path) < cutoff:
                os.remove(file_path)
