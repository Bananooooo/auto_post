# downloader.py
import os
import socket
import logging
import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

def create_driver():
    options = Options()
    hostname = socket.gethostname()
    if hostname == "blp1":
        profile_path = "/home/banano/.mozilla/firefox/a2npx81j.getmov"
    elif hostname == "bsrv5":
        profile_path = "/home/banano/.mozilla/firefox/h2vcwip9.getmov"
    elif hostname == "BPC":
        profile_path = r"C:\Users\banane\AppData\Roaming\Mozilla\Firefox\Profiles\1jhkt8um.get"
    options.set_preference("profile", profile_path)
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)

async def tiktokdownloadonline(bot, url: str) -> str:
    driver = create_driver()
    try:
        driver.get("https://tiktokdownload.online/de")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main_page_text"))).send_keys(url)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit"))).click()

        download_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/section[1]/section/div/div/div/div/div[2]/a[1]'))
        )
        video_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/main/section[1]/section/div/div[2]/div/div/div[1]/div[2]/h2'))
        )
        output_dir = os.path.join(os.getcwd(), "videos")
        os.makedirs(output_dir, exist_ok=True)
        video_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{video_name_element.text}.mp4"
        output_path = os.path.join(output_dir, video_name)
        href = download_link.get_attribute('href')
        subprocess.run(f'yt-dlp "{href}" -o "{output_path}"', shell=True, check=True)
        return video_name
    finally:
        driver.quit()

async def fallback_download(bot, url: str) -> str:
    try:
        await bot.get_channel(ADMIN_CHAT_ID).send(f"FALLBACK DOWNLOAD !!!")
        return
    except Exception as e:
        logger.error(f"Fallback fehlgeschlagen: {e}")

async def download_video(url: str) -> str:
    try:
        return await tiktokdownloadonline(url)
    except Exception as e:
        logger.warning(f"Selenium fehlgeschlagen: {e}, versuche Fallback...")
        return await fallback_download(url)
