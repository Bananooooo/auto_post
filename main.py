# main.py
import os
import re
import time
import asyncio
import logging
import discord
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

from config import BOT_TOKEN, ADMIN_CHAT_ID
from utils import ensure_video_dir, delete_long_videos
from downloader import download_video
from instagram import post_to_instagram


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # wichtig für message.content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    ensure_video_dir()
    video_count = len([f for f in os.listdir("videos") if f.endswith(".mp4")])
    await bot.get_channel(ADMIN_CHAT_ID).send(f" Bot gestartet. {video_count} Videos vorhanden.")
    await post_to_instagram(bot)
    time.sleep(20)
    await post_to_instagram(bot)
    print(f"Bot ist eingeloggt als {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)  # damit Commands weiterhin funktionieren

    text = message.content.strip()
    if re.match(r'^https?://', text):
        await message.channel.send("🔄 Link erhalten. Verarbeite TikTok-Video...")
        try:
            loop = asyncio.get_running_loop()
            video_name = await loop.run_in_executor(executor, download_video, text)
            await bot.get_channel(ADMIN_CHAT_ID).send(f"✅ Video heruntergeladen: {video_name}")
        except Exception as e:
            logger.error(f"❌ Fehler beim Download: {e}")
            await bot.get_channel(ADMIN_CHAT_ID).send(f"❌ Download-Fehler: {e}")

        await delete_long_videos(bot)
    else:
        await bot.get_channel(ADMIN_CHAT_ID).send("❌ Bitte sende einen gültigen TikTok-Link.")


@bot.event
async def on_error(event_method, *args, **kwargs):
    logger.error(f"Exception in {event_method}", exc_info=True)

def main():
    ensure_video_dir()
    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    main()
