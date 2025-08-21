# instagram.py
import os
import time
import logging
from instagrapi import Client
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, ADMIN_CHAT_ID
from utils import get_video_path

logger = logging.getLogger(__name__)

def login_instagram() -> Client:
    client = Client()
    try:
        client.load_settings("session.json")
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        logger.info("📲 Instagram-Login erfolgreich.")
    except Exception as e:
        logger.warning(f"⚠️ Login mit Session fehlgeschlagen: {e}")
        # 2FA nur testweise, evtl. manuelle Lösung nötig
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, verification_code="633646")
    return client

async def post_to_instagram(bot):
    time.sleep(5)
    await bot.get_channel(ADMIN_CHAT_ID).send(f" Posting gestartet.")
    videos = sorted([f for f in os.listdir("videos") if f.endswith(".mp4")])
    if not videos:
        await bot.get_channel(ADMIN_CHAT_ID).send(f"⚠️ Keine Videos zum Posten gefunden.")
        return

    video = videos[0]
    caption = f"video von: {video.split('_')[-1].replace('.mp4', '').lower()}"
    path = get_video_path(video)

    print(video, caption, path)
    
    client = login_instagram()
    try:
        media = client.clip_upload(path, caption)
        await bot.get_channel(ADMIN_CHAT_ID).send(f"✅ Erfolgreich gepostet: {video}")
        os.remove(path)
        logger.info(f"✅ Video entfernt nach Upload: {video}")
    except Exception as e:
        logger.error(f"Fehler beim Upload {video}: {e}")
        await bot.get_channel(ADMIN_CHAT_ID).send(f"❌ Fehler beim Posten von {video}: {e}")