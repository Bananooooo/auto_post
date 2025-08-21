Ein einfaches Python-Skript zum **automatisierten Posten auf Instagram** und **Herunterladen von TikToks**.  
Perfekt für kleine Automatisierungen mit Cronjobs. 🚀  

---

## ✨ Features
- 📤 Automatisch auf Instagram posten  
- 📥 TikTok-Videos herunterladen  
- ⚙️ Konfiguration über `.env`  
- ⏰ Cronjob-Integration  

---

## 📦 Installation
```bash
# Repository klonen
git clone https://github.com/dein-user/auto_post.git
cd auto_post

# Abhängigkeiten installieren
pip install -r requirements.txt
```

---

## ⚙️ Konfiguration
Lege im Projektordner eine `.env` Datei an und fülle sie mit deinen Daten:  

```env
BOT_TOKEN=dein_bot_token
ADMIN_CHAT_ID=deine_admin_chat_id
INSTAGRAM_USERNAME=dein_instagram_username
INSTAGRAM_PASSWORD=dein_instagram_passwort
```

> 🔒 **Hinweis:** Teile deine `.env` niemals öffentlich – sie enthält sensible Daten!  

---

## ⏰ Cronjob einrichten
Beispiel: Skript täglich um **06:45 Uhr starten** und um **06:30 Uhr beenden**, falls noch ein Prozess läuft:  

```cron
45 6 * * * /bin/bash -c 'cd /auto_post && /usr/bin/python3 /auto_post/main.py'
30 6 * * * pkill -f /auto_post/main.py
```

Cronjob bearbeiten:  
```bash
crontab -e
```

---

## ▶️ Nutzung
Manuell starten:  
```bash
python3 main.py
```

Oder automatisch über Cron.  

---

## 🛠️ Anforderungen
- Python **3.10+**  
- Instagram-Account  
- Discord-Bot 

---

## 🤝 Beitrag leisten
Pull Requests, Feature-Ideen und Bug-Reports sind willkommen!  

---

## ❤️ Support
Falls dir das Projekt gefällt, ⭐ gib dem Repo einen **Star**!  

---
