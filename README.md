# auto_post
Simple Python Script to post to Instagram and download Tik Toks

1. Clone everything
2. create .env file like so (Fill it out with your info):
  BOT_TOKEN=<>
  ADMIN_CHAT_ID=<>
  INSTAGRAM_USERNAME=<>
  INSTAGRAM_PASSWORD=<>

3. create cronjob like this
   45 6 * * * /bin/bash -c 'cd /daten/@projekte/auto_post && /usr/bin/python3 /daten/@projekte/auto_post/main.py'
   30 6 * * * pkill -f /daten/@projekte/auto_post/main.py

4. Enjoy the little automation!
