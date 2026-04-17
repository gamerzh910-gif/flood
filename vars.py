#🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "39097403"))
API_HASH = environ.get("API_HASH", "c0a7c90594ca10dd347bd4a2e69ba3ff)
BOT_TOKEN = environ.get("BOT_TOKEN", "8609526873:AAHTig5mcK1TzqqfP_yocCmg3S0MatDW5NY")

OWNER = int(environ.get("OWNER", "7549194607"))
CREDIT = environ.get("CREDIT", "🤍🌸@leavingproperty🤍🌸")

TOTAL_USER = os.environ.get('TOTAL_USERS', '7549194607').split(',')
TOTAL_USERS = [int(user_id) for user_id in TOTAL_USER]

AUTH_USER = os.environ.get('AUTH_USERS', '7549194607').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
