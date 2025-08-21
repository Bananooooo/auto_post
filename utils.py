# utils.py
import os
import json
import logging
import subprocess

from config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

VIDEO_DIR = "videos"

def ensure_video_dir():
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
        logger.info(" 'videos/' Ordner erstellt.")
        print(" 'videos/' Ordner erstellt.")

def get_video_path(name: str) -> str:
    return os.path.join(VIDEO_DIR, name)

async def get_duration(file_path):
    print(f"Getting duration for {file_path}...")
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        duration_data = json.loads(result.stdout)
        duration = float(duration_data['format']['duration'])
        print(f"Duration for {file_path}: {duration:.2f} seconds")
        return duration
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e2:
            print(f"Error deleting file {file_path}: {e2}")
        return 0

async def delete_long_videos(bot=None):
    """
    Löscht Videos länger als 180 Sekunden. 
    Wenn ein Discord-Bot übergeben wird, wird der Admin benachrichtigt.
    """
    deleted_files = []
    for file in os.listdir(VIDEO_DIR):
        if file.endswith(".mp4"):
            path = get_video_path(file)
            duration = await get_duration(path)
            if duration > 180:
                os.remove(path)
                deleted_files.append(file)
                logger.info(f" Gelöscht (zu lang): {file}")
                print(f" Gelöscht (zu lang): {file}")
                if bot:
                    try:
                        admin = await bot.fetch_user(ADMIN_CHAT_ID)
                        await admin.send(f"🗑️ Gelöscht (zu lang): {file}")
                    except Exception as e:
                        print(f"[ERROR] Admin-Nachricht konnte nicht gesendet werden: {e}")
    return deleted_files
