
from utils.flood import flood
import asyncio

async def safe_send(bot, chat_id, text, **kwargs):
    return await flood.run(bot.send_message, chat_id, text, **kwargs)

import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

processing_request = False
cancel_requested = False
cancel_message = None

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp ='eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://ibb.co/NgbsRGMP'
photoyt = 'https://ibb.co/NgbsRGMP'
photocp = 'https://ibb.co/NgbsRGMP'
photozip = 'https://ibb.co/NgbsRGMP'

BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/leavingproperty")]])
keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="🛠️ Help", url="https://t.me/leavingproperty"), InlineKeyboardButton(text="🛠️ Divyanshshukla", url="https://t.me/leavingproperty")],
    ]
)

image_urls = [
    "https://ibb.co/NgbsRGMP",
    "https://ibb.co/NgbsRGMP",
]

@bot.on_message(filters.command("addauth") & filters.private)
async def add_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return 
    try:
        new_user_id = int(message.command[1])
        if new_user_id in AUTH_USERS:
            await message.reply_text("**User ID is already authorized.**")
        else:
            AUTH_USERS.append(new_user_id)
            await message.reply_text(f"**User ID `{new_user_id}` added to authorized users.**")
    except (IndexError, ValueError):
        await message.reply_text("**Please provide a valid user ID.**")

@bot.on_message(filters.command("users") & filters.private)
async def list_auth_users(client: Client, message: Message):
    if message.chat.id != OWNER:
        return

    user_list = '\n'.join(map(str, AUTH_USERS))
    await message.reply_text(f"**Authorized Users:**\n{user_list}")

@bot.on_message(filters.command("rmauth") & filters.private)
async def remove_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return

    try:
        user_id_to_remove = int(message.command[1])
        if user_id_to_remove not in AUTH_USERS:
            await message.reply_text("**User ID is not in the authorized users list.**")
        else:
            AUTH_USERS.remove(user_id_to_remove)
            await message.reply_text(f"**User ID `{user_id_to_remove}` removed from authorized users.**")
    except (IndexError, ValueError):
        await message.reply_text("**Please provide a valid user ID.**")

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client: Client, message: Message):
    if message.chat.id != OWNER:
        return
    if not message.reply_to_message:
        await message.reply_text("**Reply to any message (text, photo, video, or file) with /broadcast to send it to all users.**")
        return
    success = 0
    fail = 0
    for user_id in list(set(TOTAL_USERS)):
        try:
            if message.reply_to_message.text:
                await client.send_message(user_id, message.reply_to_message.text)
            elif message.reply_to_message.photo:
                await client.send_photo(
                    user_id,
                    photo=message.reply_to_message.photo.file_id,
                    caption=message.reply_to_message.caption or ""
                )
            elif message.reply_to_message.video:
                await client.send_video(
                    user_id,
                    video=message.reply_to_message.video.file_id,
                    caption=message.reply_to_message.caption or ""
                )
            elif message.reply_to_message.document:
                await client.send_document(
                    user_id,
                    document=message.reply_to_message.document.file_id,
                    caption=message.reply_to_message.caption or ""
                )
            else:
                await client.forward_messages(user_id, message.chat.id, message.reply_to_message.message_id)

            success += 1
        except (FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated):
            fail += 1
            continue
        except Exception as e:
            fail += 1
            continue

    await message.reply_text(f"<b>Broadcast complete!</b>\n<blockquote><b>✅ Success: {success}\n❎ Failed: {fail}</b></blockquote>")

@bot.on_message(filters.command("broadusers") & filters.private)
async def broadusers_handler(client: Client, message: Message):
    if message.chat.id != OWNER:
        return

    if not TOTAL_USERS:
        await message.reply_text("**No Broadcasted User**")
        return

    user_infos = []
    for user_id in list(set(TOTAL_USERS)):
        try:
            user = await client.get_users(int(user_id))
            fname = user.first_name if user.first_name else " "
            user_infos.append(f"[{user.id}](tg://openmessage?user_id={user.id}) | `{fname}`")
        except Exception:
            user_infos.append(f"[{user.id}](tg://openmessage?user_id={user.id})")

    total = len(user_infos)
    text = (
        f"<blockquote><b>Total Users: {total}</b></blockquote>\n\n"
        "<b>Users List:</b>\n"
        + "\n".join(user_infos)
    )
    await message.reply_text(text)


@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        input_message: Message = await client.listen(m.chat.id)

        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        downloaded_path = await input_message.download()

        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("**Send valid text data**")
        return

    text_data = input_message.text.strip()
    await input_message.delete()

    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()
    await editable.delete()

    if raw_textn == '/d':
        custom_file_name = 'txt_file'
    else:
        custom_file_name = raw_textn

    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write(text_data)

    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\n<blockquote>You can now download your content! 📥</blockquote>")
    os.remove(txt_file)

UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)

    editable = await message.reply_text(
        f"Send YouTube Website/Playlist link for convert in .txt file"
    )

    input_message: Message = await bot.listen(editable.chat.id)
    youtube_link = input_message.text.strip()
    await input_message.delete(True)
    await editable.delete(True)

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'force_generic_extractor': True,
        'forcejson': True,
        'cookies': 'youtube_cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(youtube_link, download=False)
            if 'entries' in result:
                title = result.get('title', 'youtube_playlist')
            else:
                title = result.get('title', 'youtube_video')
        except yt_dlp.utils.DownloadError as e:
            await message.reply_text(
                f"<blockquote>{str(e)}</blockquote>"
            )
            return

    videos = []
    if 'entries' in result:
        for entry in result['entries']:
            video_title = entry.get('title', 'No title')
            url = entry['url']
            videos.append(f"{video_title}: {url}")
    else:
        video_title = result.get('title', 'No title')
        url = result['url']
        videos.append(f"{video_title}: {url}")

    txt_file = os.path.join("downloads", f'{title}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))

    await message.reply_document(
        document=txt_file,
        caption=f'<a href="{youtube_link}">__**Click Here to Open Link**__</a>\n<blockquote>{title}.txt</blockquote>\n'
    )

    os.remove(txt_file)

@bot.on_message(filters.command(["yt2m"]))
async def yt2m_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"🔹**Send me the YouTube link**")
    input: Message = await bot.listen(editable.chat.id)
    youtube_link = input.text.strip()
    await input.delete(True)
    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n\n🔗𝐔𝐑𝐋 »  {youtube_link}\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🐦"
    await editable.edit(Show, disable_web_page_preview=True)
    await asyncio.sleep(10)
    try:
        Vxy = youtube_link.replace("www.youtube-nocookie.com/embed", "youtu.be")
        url = Vxy
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url)
        audio_title = response.json().get('title', 'YouTube Video')
        name = f'{audio_title[:60]} {CREDIT}'        
        if "youtube.com" in url or "youtu.be" in url:
            # MAX SPEED - Added external downloader args
            cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp3"'
            print(f"Running command: {cmd}")
            os.system(cmd)
            if os.path.exists(f'{name}.mp3'):
                print(f"File {name}.mp3 exists, attempting to send...")
                try:
                    await editable.delete()
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : {CREDIT}')
                    os.remove(f'{name}.mp3')
                except Exception as e:
                    await editable.delete()
                    await m.reply_text(f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{name}`\n**Url** =>> {url}\n\n**Failed Reason:**\n<blockquote>{str(e)}</blockquote>', disable_web_page_preview=True)

            else:
                await editable.delete()
                await m.reply_text(f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{name}`\n**Url** =>> {url}', disable_web_page_preview=True)

    except Exception as e:
        await m.reply_text(f"**Failed Reason:**\n<blockquote>{str(e)}</blockquote>")

@bot.on_message(filters.command(["ytm"]))
async def txt_handler(bot: Client, m: Message):
    global processing_request, cancel_requested, cancel_message
    processing_request = True
    cancel_requested = False
    editable = await m.reply_text("🔹**Send me the TXT file containing YouTube links.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("**Invalid file input.**")
        os.remove(x)
        return


    await editable.edit(f"🔹**ᴛᴏᴛᴀʟ 🔗 ʟɪɴᴋs ғᴏᴜɴᴅ ᴀʀᴇ --__{len(links)}__--\n🔹sᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1' 

    await editable.delete()      
    await m.reply_text(f"<blockquote><b>{file_name}</b></blockquote>")
    count = int(raw_text)
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            if cancel_requested:
                await m.reply_text("🚦**STOPPED**🚦")
                processing_request = False
                cancel_requested = False
                return
            Vxy = links[i][1].replace("www.youtube-nocookie.com/embed", "youtu.be")
            url = "https://" + Vxy

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{name1[:60]} {CREDIT}'

            if "youtube.com" in url or "youtu.be" in url:
                prog = await m.reply_text(f"<i><b>Audio Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>")
                # MAX SPEED - Added external downloader
                cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp3"'
                print(f"Running command: {cmd}")
                os.system(cmd)
                if os.path.exists(f'{name}.mp3'):
                    await prog.delete(True)
                    print(f"File {name}.mp3 exists, attempting to send...")
                    try:
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : {CREDIT}')
                        os.remove(f'{name}.mp3')
                        count+=1
                    except Exception as e:
                        await m.reply_text(f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {url}', disable_web_page_preview=True)
                        count+=1
                else:
                    await prog.delete(True)
                    await m.reply_text(f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {url}', disable_web_page_preview=True)
                    count+=1

    except Exception as e:
        await m.reply_text(f"<b>Failed Reason:</b>\n<blockquote><b>{str(e)}</b></blockquote>")
    finally:
        await m.reply_text("<blockquote><b>All YouTube Music Download Successfully</b></blockquote>")

m_file_path= "main.py"
@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=cookies_file_path,
            caption="Here is the `youtube_cookies.txt` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")     

@bot.on_message(filters.command("mfile") & filters.private)
async def getmfile_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=m_file_path,
            caption="Here is the `main.py` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["resat"]))
async def restart_handler(_, m):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await safe_send(bot, 
            m.chat.id, 
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**PLEASE /upgrade YOUR PLAN**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        await m.reply_text("🚦**RESAT & RESTARTED**🚦", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    global processing_request, cancel_requested
    if processing_request:
        cancel_requested = True
        await m.delete()
        cancel_message = await m.reply_text("**🚦 Process cancel request received. Stopping after current process...**")
    else:
        cancel_message = None
        await m.reply_text("**⚡ No active process to cancel.**")


@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user = await bot.get_me()

    mention = user.mention
    caption = f"🌟 Welcome {m.from_user.mention} ! 🌟"
    start_message = await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://ibb.co/NgbsRGMP",
        caption=caption
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Initializing Uploader bot... 🤖\n\n"
        f"Progress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Loading features... ⏳\n\n"
        f"Progress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"This may take a moment, sit back and relax! 😊\n\n"
        f"Progress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Checking subscription status... 🔍\n\n"
        f"Progress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n"
    )

    await asyncio.sleep(1)
    if m.chat.id in AUTH_USERS:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Features", callback_data="feat_command")],
            [InlineKeyboardButton("USER CMD", callback_data="user_command"), InlineKeyboardButton("OWNER CMD", callback_data="owner_command")],
            [InlineKeyboardButton("🎫 plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ OWNER", url="https://t.me/leavingproperty")],
        ])

        await start_message.edit_text(
            f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
            f"Great! You are a premium member!\n"
            f"Use button : __**USER CMD**__ to get started 🌟\n\n"
            f"If you face any problem contact -  [{CREDIT}⁬](tg://openmessage?user_id={OWNER})\n", disable_web_page_preview=True, reply_markup=keyboard
        )
    else:
        await asyncio.sleep(2)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Features", callback_data="feat_command")],
            [InlineKeyboardButton("USER CMD", callback_data="user_command"), InlineKeyboardButton("OWNER CMD", callback_data="owner_command")],
            [InlineKeyboardButton("🎫 plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ OWNER", url="https://t.me/leavingproperty")],
        ])
        await start_message.edit_text(
           f" 🎉 Welcome {m.from_user.first_name} to DRM Bot! 🎉\n\n"
           f"**You are currently using the free version.** 🆓\n\n<blockquote expandable>I'm here to make your life easier by downloading videos from your **.txt** file 📄 and uploading them directly to Telegram!</blockquote>\n\n**Want to get started? Press /id**\n\n💬 Contact : [{CREDIT}⁬](tg://openmessage?user_id={OWNER}) to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓\n", disable_web_page_preview=True, reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id}) in My uploader bot**"
    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Features", callback_data="feat_command")],
            [InlineKeyboardButton("USER CMD", callback_data="user_command"), InlineKeyboardButton("OWNER CMD", callback_data="owner_command")],
        [InlineKeyboardButton("🎫 plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ OWNER", url="https://t.me/leavingproperty")],
        ])

    await callback_query.message.edit_media(
      InputMediaPhoto(
        media="https://ibb.co/NgbsRGMP",
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()  

@bot.on_callback_query(filters.regex("user_command"))
async def help_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
  caption = (
        f"💥 𝐁𝐎𝐓𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n" 
        f"📌 𝗠𝗮𝗶𝗻 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:\n\n"  
        f"➥ /start – Bot Status Check\n"
        f"➥ /ishu – Extract from .txt (Auto)\n"
        f"➥ /y2t – YouTube → .txt Converter\n"  
        f"➥ /ytm – YT .txt → .mp3 downloader\n"  
        f"➥ /yt2m – YT link → .mp3 downloader\n"  
        f"➥ /t2t – Text → .txt Generator\n" 
        f"➥ /stop – Cancel Running Task\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ \n" 
        f"⚙️ 𝗧𝗼𝗼𝗹𝘀 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀: \n\n" 
        f"➥ /cookies – Update YT Cookies\n" 
        f"➥ /id – Get Chat/User ID\n"  
        f"➥ /info – User Details\n"  
        f"➥ /logs – View Bot Activity\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        f"💡 𝗡𝗼𝘁𝗲:\n\n"  
        f"• Send any link for auto-extraction\n"  
        f"• Supports batch processing\n\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )

  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
    ),
    reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("owner_command"))
async def owner_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
  caption = (
        f"👤 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n\n" 
        f"➥ /addauth xxxx – Add User ID\n" 
        f"➥ /rmauth xxxx – Remove User ID\n"  
        f"➥ /users – Total User List\n"  
        f"➥ /broadcast – For Broadcasting\n"  
        f"➥ /broadusers – All Broadcasting Users\n"  
        f"➥ /resat – Resat Bot\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )

  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
    ),
    reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("upgrade_command"))
async def upgrade_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
  caption = (
           f" 🎉 Welcome {first_name} to DRM Bot! 🎉\n\n"
           f"You can have access to download all Non-DRM+AES Encrypted URLs 🔐 including\n\n"
           f"<blockquote>• 📚 Appx Zip+Encrypted Url\n"
           f"• 🎓 Classplus DRM+ NDRM\n"
           f"• 🧑‍🏫 PhysicsWallah DRM\n"
           f"• 📚 CareerWill + PDF\n"
           f"• 🎓 Khan GS\n"
           f"• 🎓 Study Iq DRM\n"
           f"• 🚀 APPX + APPX Enc PDF\n"
           f"• 🎓 Vimeo Protection\n"
           f"• 🎓 Brightcove Protection\n"
           f"• 🎓 Visionias Protection\n"
           f"• 🎓 Zoom Video\n"
           f"• 🎓 Utkarsh Protection(Video + PDF)\n"
           f"• 🎓 All Non DRM+AES Encrypted URLs\n"
           f"• 🎓 MPD URLs if the key is known (e.g., Mpd_url?key=key XX:XX)</blockquote>\n\n"
           f"<b>💵 Monthly Plan: 150₹</b>\n\n"
           f"If you want to buy membership of the bot, feel free to contact the Bot Admin.\n"
    )  

  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
    ),
    reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("feat_command"))
async def feature_button(client, callback_query):
  caption = "**✨ My Premium BOT Features :**"
  keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("📌 Auto Pin Batch Name", callback_data="pin_command")],
      [InlineKeyboardButton("💧 Watermark", callback_data="watermark_command"), InlineKeyboardButton("🔄 Resat", callback_data="resat_command")],
      [InlineKeyboardButton("🖨️ Bot Working Logs", callback_data="logs_command")],
      [InlineKeyboardButton("🖋️ File Name", callback_data="custom_command"), InlineKeyboardButton("🏷️ Title", callback_data="titlle_command")],
      [InlineKeyboardButton("🎥 YouTube", callback_data="yt_command")],
      [InlineKeyboardButton("📝 Text File", callback_data="txt_maker_command"), InlineKeyboardButton("📢 Broadcast", callback_data="broadcast_command")],
      [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
  ])
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
    ),
    reply_markup=keyboard
  )


@bot.on_callback_query(filters.regex("pin_command"))
async def pin_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Auto Pin 📌 Batch Name :**\n\nAutomatically Pins the Batch Name in Channel or Group, If Starting from the First Link."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("watermark_command"))
async def watermark_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Custom Watermark :**\n\nSet Your Own Custom Watermark on Videos for Added Personalization."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("resat_command"))
async def restart_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🔄 Resat Command:**\n\nIf You Want to Resat Your Bot, Simply Use Command /resat."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("logs_command"))
async def logs_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🖨️ Bot Working Logs:**\n\n◆/logs - Bot Send Working Logs in .txt File."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("custom_command"))
async def custom_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🖋️ Custom File Name:**\n\nSupport for Custom Name before the File Extension.\nAdd name ..when txt is uploading"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("titlle_command"))
async def titlle_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Custom Title Feature :**\nAdd and customize titles at the starting\n**NOTE 📍 :** The Titile must enclosed within (Title), Best For appx's .txt file."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("broadcast_command"))
async def broadcast_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**📢 Broadcasting Support:**\n\n◆/broadcast - 📢 Broadcast to All Users.\n◆/broadusers - 👁️ To See All Broadcasting User"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("txt_maker_command"))
async def editor_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🤖 Available Commands 🗓️**\n◆/t2t for text to .txt file\n"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_callback_query(filters.regex("yt_command"))
async def y2t_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**YouTube Commands:**\n\n◆/ytm - 🎶 YT .txt → .mp3 downloader\n◆/yt2m - 🎵 YT link → .mp3 downloader\n◆/y2t - 🔪 YouTube Playlist or Web Search → .txt Converter"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://ibb.co/NgbsRGMP",
      caption=caption
      ),
      reply_markup=keyboard
  )

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(f"<blockquote>The ID of this chat id is:</blockquote>\n`{chat_id}`")

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):

    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )

    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=BUTTONSCONTACT
    )

@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")


@bot.on_message(filters.command(["Ankit1"]))
async def txt_handler(bot: Client, m: Message):  
    global processing_request, cancel_requested, cancel_message
    processing_request = True
    cancel_requested = False
    if m.chat.id not in AUTH_USERS:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            await safe_send(bot, m.chat.id, f"<blockquote>__**Oopss! You are not a Premium member\nPLEASE /upgrade YOUR PLAN\nSend me your user id for authorization\nYour User id**__ - `{m.chat.id}`</blockquote>\n")
            return
    editable = await m.reply_text(f"**__Hii, I am non-drm Downloader Bot__\n<blockquote><i>Send Me Your text file which enclude Name with url...\nE.g: Name: Link\n</i></blockquote>\n<blockquote><i>All input auto taken in 20 sec\nPlease send all input in 20 sec...\n</i></blockquote>**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    path = f"./downloads/{m.chat.id}"

    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0

    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")

        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif "v2" in url:
                    v2_count += 1
                elif "mpd" in url:
                    mpd_count += 1
                elif "m3u8" in url:
                    m3u8_count += 1
                elif "drm" in url:
                    drm_count += 1
                elif "youtu" in url:
                    yt_count += 1
                elif "zip" in url:
                    zip_count += 1
                else:
                    other_count += 1
        os.remove(x)
    except:
        await m.reply_text("<b>🔹Invalid file input.</b>")
        os.remove(x)
        return

    await editable.edit(f"**Total 🔗 links found are {len(links)}\n<blockquote>•PDF : {pdf_count}      •V2 : {v2_count}\n•Img : {img_count}      •YT : {yt_count}\n•zip : {zip_count}       •m3u8 : {m3u8_count}\n•drm : {drm_count}      •Other : {other_count}\n•mpd : {mpd_count}</blockquote>\nSend From where you want to download**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'

    if int(raw_text) > len(links):
        await editable.edit(f"**🔹Enter number in range of Index (01-{len(links)})**")
        processing_request = False
        await m.reply_text("**🔹Exiting Task......  **")
        return

    await editable.edit(f"**Enter Batch Name or send /d**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/d'

    if raw_text0 == '/d':
        b_name = file_name.replace('_', ' ')
    else:
        b_name = raw_text0

    await editable.edit("__**Enter resolution or Video Quality (`144`, `240`, `360`, `480`, `720`, `1080`)**__")
    try:
        input2: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text2 = input2.text
        await input2.delete(True)
    except asyncio.TimeoutError:
        raw_text2 = '480'
    quality = f"{raw_text2}p"
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"

    await editable.edit(f"**Enter the Credit Name or send /d\n\n<blockquote><b>Format:</b>\n🔹Send __Admin__ only for caption\n🔹Send __Admin,filename__ for caption and file...Separate them with a comma (,)</blockquote>**")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/d'

    if raw_text3 == '/d':
        CR = f"{CREDIT}"
    elif "," in raw_text3:
        CR, PRENAME = raw_text3.split(",")
    else:
        CR = raw_text3

    await editable.edit("**Enter 𝐏𝐖/𝐂𝐖/𝐂𝐏 Working Token For 𝐌𝐏𝐃 𝐔𝐑𝐋 or send /d**")
    try:
        input4: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text4 = input4.text
        await input4.delete(True)
    except asyncio.TimeoutError:
        raw_text4 = '/d'

    if raw_text4 == '/d':
        cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
        cptoken = "cptoken"
        pwtoken = "pwtoken"
    else:
        cwtoken = raw_text4
        cptoken = raw_text4
        pwtoken = raw_text4

    await editable.edit(f"**Send the Video Thumb URL or send /d**")
    try:
        input6: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text6 = input6.text
        await input6.delete(True)
    except asyncio.TimeoutError:
        raw_text6 = '/d'

    if raw_text6.startswith("http://") or raw_text6.startswith("https://"):
        getstatusoutput(f"wget '{raw_text6}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = raw_text6

    await editable.edit("__**⚠️Provide the Channel ID or send /d__\n\n<blockquote><i>🔹 Make me an admin to upload.\n🔸Send /id in your channel to get the Channel ID.\n\nExample: Channel ID = -100XXXXXXXXXXX</i></blockquote>\n**")
    try:
        input7: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text7 = input7.text
        await input7.delete(True)
    except asyncio.TimeoutError:
        raw_text7 = '/d'

    if "/d" in raw_text7:
        channel_id = m.chat.id
    else:
        channel_id = raw_text7    
    await editable.delete()

    try:
        if raw_text == "1":
            batch_message = await safe_send(bot, chat_id=channel_id, text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>")
            if "/d" not in raw_text7:
                await safe_send(bot, chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
                await bot.pin_chat_message(channel_id, batch_message.id)
                message_id = batch_message.id
                pinning_message_id = message_id + 1
                await bot.delete_messages(channel_id, pinning_message_id)
        else:
             if "/d" not in raw_text7:
                await safe_send(bot, chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
    except Exception as e:
        await m.reply_text(f"**Fail Reason »**\n<blockquote><i>{e}</i></blockquote>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🌟`")


    failed_count = 0
    count =int(raw_text)    
    arg = int(raw_text)


    try:
        for i in range(arg-1, len(links)):
            if cancel_requested:
                await m.reply_text("🚦**STOPPED**🚦")
                processing_request = False
                cancel_requested = False
                return

            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            if "," in raw_text3:
                 name = f'{PRENAME} {name1[:60]}'
            else:
                 name = f'{name1[:60]}'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)", text).group(1)

            if "acecwply" in url:
                # MAX SPEED - Added concurrent fragments and aria2c
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'

            elif "https://cpvod.testbook.com/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                url = f"https://player.marshmallowapi.workers.dev/?video={url}"
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp.com/drm/" in url:
                url = f"https://player.marshmallowapi.workers.dev/?video={url}"
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp" in url:
                signed_api = f"https://player.marshmallowapi.workers.dev/?video={url}"
                response = requests.get(signed_api, timeout=10)
                url = response.text.strip()

            elif "tencdn.classplusapp" in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']  

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{cptoken}'}).json()['url']

            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url: 
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url   = response.json()['url']

            if "edge.api.brightcove.com" in url:
                bcov = f'bcov_auth={cwtoken}'
                url = url.split("bcov_auth")[0]+bcov

            elif "childId" in url and "parentId" in url:
                url = f"https://anonymouspwplayerr-3cfbfedeb317.herokuapp.com/pw?url={url}&token={raw_text4}"

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                url = f"https://anonymouspwplayerr-3cfbfedeb317.herokuapp.com/pw?url={url}&token={raw_text4}"

            if ".pdf*" in url:
                url = f"https://dragoapi.vercel.app/pdf/{url}"

            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

            if "youtu" in url:
                ytf = f"bv*[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[height<=?{raw_text2}]"
            elif "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                # MAX SPEED
                cmd = f'yt-dlp -o "{name}.mp4" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
            elif "webvideos.classplusapp." in url:
               # MAX SPEED
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url:
                # MAX SPEED
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}".mp4'
            else:
                # MAX SPEED - Default command with optimizations
                cmd = f'yt-dlp -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp4"'


            try:
                cc = f'''╔══════[ RAJPUT]══════╗\n╭┈✰┈┈┈╮\n{str(count).zfill(3)}\n╰┈┈┈✰┈╯\n\n**📹 𝗩𝗜𝗗𝗘𝗢 𝗧𝗜𝗧𝗟𝗘 ➬ ** `{name1}\n├── Extention ➫ @praxharaj 💝\n├── Resolution [{res}p] @praxharajmkv`\n\n<blockquote><b>🧿 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘 ➲</b> {b_name}</blockquote>\n\n**💎 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗕𝗬 ➫**\n\n╔.★. .═════════════╗\n\n 𓇼{CR}𓇼\n\n╚═════════════. .★.╝\n\n<blockquote>『────⟡{CR}⟡────』</blockquote>\n\n╔════════════════════╗'''
                cc1 = f'''╔══════[ RAJPUT]══════╗\n╭┈✰┈┈┈╮\n {str(count).zfill(3)}\n╰┈┈┈✰┈╯\n\n**📁 𝗙𝗜𝗟𝗘 𝗧𝗜𝗧𝗟𝗘  ➬** `{name1}`\n├── Extention ➫ @praxharaj 💝\n├── Resolution -@praxharaj.pdf`\n\n<blockquote><b>🧿 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘 ➲</b> {b_name}</blockquote>\n\n**💎 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗕𝗬 ➫**\n\n╔.★. .═════════════╗\n\n 𓇼{CR}𓇼\n\n╚═════════════. .★.╝\n\n<blockquote>『────⟡{CR}⟡────』</blockquote>\n\n╔════════════════════╗'''
                ccimg = f'''\n╭┈✰┈┈┈╮\n {str(count).zfill(3)}\n╰┈┈┈✰┈╯\n\n**Img Title :** `{name1}\n├── Extention ➫ @praxharaj 💝\n├── Resolution.jpg`\n\n<blockquote><b>🧿 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘 ➲</b> {b_name}</blockquote>\n\n**💎 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗕𝗬 ➫**\n\n╔.★. .═════════════╗\n\n 𓇼{CR}𓇼\n\n╚═════════════. .★.╝\n\n<blockquote>『────⟡{CR}⟡────』</blockquote>'''
                ccm = f'''\n╭┈✰┈┈┈╮\n {str(count).zfill(3)}\n╰┈┈┈✰┈╯\n\n**Audio Title :** `{name1}\n├── Extention ➫ @praxharaj💝\n├── Resolution.mp3`\n\n<blockquote><b>🧿 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘 ➲</b> {b_name}</blockquote>\n\n**💎 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗕𝗬 ➫**\n\n╔.★. .═════════════╗\n\n 𓇼{CR}𓇼\n\n╚═════════════. .★.╝\n\n<blockquote>『────⟡{CR}⟡────』</blockquote>'''
                cchtml = f'''\n╭┈✰┈┈┈╮\n {str(count).zfill(3)}\n╰┈┈┈✰┈╯\n\n**Html Title :** `{name1}\n├── Extention ➫ @praxharaj 💝\n├── Resolution.html`\n\n<blockquote><b>🧿 𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘 ➲</b> {b_name}</blockquote>\n\n**💎 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗕𝗬 ➫**\n\n╔.★. .═════════════╗\n\n 𓇼{CR}𓇼\n\n╚═════════════. .★.╝\n\n<blockquote>『────⟡{CR}⟡────』</blockquote>'''

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=channel_id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif ".pdf" in url:
                    if "cwmediabkt99" in url:
                        max_retries = 15
                        retry_delay = 4
                        success = False
                        failure_msgs = []

                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)

                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)
                                    copy = await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                                    count += 1
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)

                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue 
                        for msg in failure_msgs:
                            await msg.delete()

                    else:
                        try:
                            # MAX SPEED for PDF
                            cmd = f'yt-dlp -o "{name}.pdf" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue    

                elif ".ws" in url and  url.endswith(".ws"):
                    try:
                        await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}",f"{name}.html")
                        time.sleep(1)
                        await bot.send_document(chat_id=channel_id, document=f"{name}.html", caption=cchtml)
                        os.remove(f'{name}.html')
                        count += 1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        # MAX SPEED
                        cmd = f'yt-dlp -o "{name}.{ext}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=channel_id, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        # MAX SPEED
                        cmd = f'yt-dlp -o "{name}.{ext}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=channel_id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    


                elif 'encrypted.m' in url:    
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n"                            f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n"                            f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Eɴᴄʀʏᴘᴛᴇᴅ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n"                            f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n'                            f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {name}</blockquote>\n┃\n"                            f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n"                            f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n'                            f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n'                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"🛑**Send** /stop **to stop process**\n┃\n"                            f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>" 
                    prog = await safe_send(bot, channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)  
                    filename = res_file  
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    count += 1  
                    await asyncio.sleep(1)  
                    continue  

                elif 'drmcdni' in url or 'drm/wv' in url:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n"                            f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n"                            f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Eɴᴄʀʏᴘᴛᴇᴅ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n"                            f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n'                            f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {name}</blockquote>\n┃\n"                            f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n"                            f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n'                            f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n'                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"🛑**Send** /stop **to stop process**\n┃\n"                            f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await safe_send(bot, channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                    filename = res_file
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                else:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n"                            f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n"                            f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Eɴᴄʀʏᴘᴛᴇᴅ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n"                            f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n'                            f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n"                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {name}</blockquote>\n┃\n"                            f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n"                            f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n'                            f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n'                            f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"                            f"🛑**Send** /stop **to stop process**\n┃\n"                            f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await safe_send(bot, channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await safe_send(bot, channel_id, f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {url}\n\n<blockquote><i><b>Failed Reason: {str(e)}</b></i></blockquote>', disable_web_page_preview=True)
                count += 1
                failed_count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
        time.sleep(2)

    success_count = len(links) - failed_count
    video_count = v2_count + mpd_count + m3u8_count + yt_count + drm_count + zip_count + other_count
    if raw_text7 == "/d":
        await safe_send(bot, channel_id, f"<b>-┈━═.•°✅ Completed ✅°•.═━┈-</b>\n<blockquote><b>🎯Batch Name : {b_name}</b></blockquote>\n<blockquote>🔗 Total URLs: {len(links)} \n┃   ┠🔴 Total Failed URLs: {failed_count}\n┃   ┠🟢 Total Successful URLs: {success_count}\n┃   ┃   ┠🎥 Total Video URLs: {video_count}\n┃   ┃   ┠📄 Total PDF URLs: {pdf_count}\n┃   ┃   ┠📸 Total IMAGE URLs: {img_count}</blockquote>\n")
    else:
        await safe_send(bot, channel_id, f"<b>-┈━═.•°✅ Completed ✅°•.═━┈-</b>\n<blockquote><b>🎯Batch Name : {b_name}</b></blockquote>\n<blockquote>🔗 Total URLs: {len(links)} \n┃   ┠🔴 Total Failed URLs: {failed_count}\n┃   ┠🟢 Total Successful URLs: {success_count}\n┃   ┃   ┠🎥 Total Video URLs: {video_count}\n┃   ┃   ┠📄 Total PDF URLs: {pdf_count}\n┃   ┃   ┠📸 Total IMAGE URLs: {img_count}</blockquote>\n")
        await safe_send(bot, m.chat.id, f"<blockquote><b>✅ Your Task is completed, please check your Set Channel📱</b></blockquote>")


@bot.on_message(filters.text & filters.private)
async def text_handler(bot: Client, m: Message):
    if m.from_user.is_bot:
        return
    links = m.text
    path = None
    match = re.search(r'https?://\S+', links)
    if match:
        link = match.group(0)
    else:
        return

    editable = await m.reply_text(f"<pre><code>**🔹Processing your link...\n🔁Please wait...⏳**</code></pre>")
    await m.delete()

    await editable.edit(f"╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣ \n┣━━⪼ send `144`  for 144p\n┣━━⪼ send `240`  for 240p\n┣━━⪼ send `360`  for 360p\n┣━━⪼ send `480`  for 480p\n┣━━⪼ send `720`  for 720p\n┣━━⪼ send `1080` for 1080p\n╰━━⌈⚡[`{CREDIT}`]⚡⌋━━➣ ")
    input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"

    await editable.delete()
    raw_text4 = "working_token"
    thumb = "/d"
    count =0
    arg =1
    channel_id = m.chat.id
    try:
            Vxy = link.replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = Vxy

            name1 = links.replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)", text).group(1)

            if "acecwply" in url:
                # MAX SPEED
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'

            elif "https://cpvod.testbook.com/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                url = 'https://dragoapi.vercel.app/classplus?link=' + url
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp.com/drm/" in url:
                url = 'https://dragoapi.vercel.app/classplus?link=' + url
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "tencdn.classplusapp" in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{raw_text4}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']  

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{raw_text4}'}).json()['url']

            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url: 
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{raw_text4}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url   = response.json()['url']

            elif "childId" in url and "parentId" in url:
                url = f"https://anonymouspwplayer-907e62cf4891.herokuapp.com/pw?url={url}&token={raw_text4}"

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                vid_id =  url.split('/')[-2]
                url = fhttps://anonymouspwplayer-907e62cf4891.herokuapp.com/pw?url={url}&token={raw_text4}"

            if ".pdf*" in url:
                url = f"https://dragoapi.vercel.app/pdf/{url}"

            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

            if "youtu" in url:
                ytf = f"bv*[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[height<=?{raw_text2}]"
            elif "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                # MAX SPEED
                cmd = f'yt-dlp -o "{name}.mp4" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
            elif "webvideos.classplusapp." in url:
               # MAX SPEED
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url:
                # MAX SPEED
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}".mp4'
            else:
                # MAX SPEED
                cmd = f'yt-dlp -f "{ytf}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}" -o "{name}.mp4"'

            try:
                cc = f'🎞️𝐓𝐢𝐭𝐥𝐞 » `{name} [{res}].mp4`\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**CLICK HERE**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `{CREDIT}`'
                cc1 = f'📕𝐓𝐢𝐭𝐥𝐞 » `{name}`\n🔗𝐋𝐢𝐧𝐤 » <a href="{link}">__**CLICK HERE**__</a>\n\n🌟𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 » `{CREDIT}`'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif ".pdf" in url:
                    if "cwmediabkt99" in url:
                        max_retries = 15
                        retry_delay = 4
                        success = False
                        failure_msgs = []

                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)

                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)
                                    copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)

                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue

                        for msg in failure_msgs:
                            await msg.delete()

                        if not success:
                            await m.reply_text(f"Failed to download PDF after {max_retries} attempts.\n⚠️**Downloading Failed**⚠️\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}", disable_web_page_preview)

                    else:
                        try:
                            # MAX SPEED
                            cmd = f'yt-dlp -o "{name}.pdf" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            pass   

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        # MAX SPEED
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=cc1)
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        # MAX SPEED
                        cmd = f'yt-dlp -o "{name}.{ext}" --concurrent-fragments 16 --external-downloader aria2c --downloader-args "aria2c: -x 16 -s 16 -k 1M" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.{ext}', caption=cc1)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif 'encrypted.m' in url:    
                    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳**\n"                            f"🔗𝐋𝐢𝐧𝐤 » {url}\n"                            f"✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)  
                    filename = res_file  
                    await prog.delete(True)  
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    await asyncio.sleep(1)  
                    pass

                elif 'drmcdni' in url or 'drm/wv' in url:
                    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳**\n"                            f"🔗𝐋𝐢𝐧𝐤 » {url}\n"                            f"✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    await asyncio.sleep(1)
                    pass

                else:
                    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳**\n"                            f"🔗𝐋𝐢𝐧𝐤 » {url}\n"                            f"✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    time.sleep(1)

            except Exception as e:
                    await m.reply_text(f"⚠️𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n🔗𝐋𝐢𝐧𝐤 » `{link}`\n\n<blockquote><b><i>⚠️Failed Reason »**__\n{str(e)}</i></b></blockquote>")
                    pass

    except Exception as e:
        await m.reply_text(str(e))

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐁𝐨𝐭 𝐑𝐞𝐬𝐚𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    requests.post(url, data=data)

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    requests.post(url, json={"commands": []})
    commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "help", "description": "👨‍🏭 Help about the Bot"},
        {"command": "bhumi", "description": "📑 Upload .txt file"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YT .txt → .mp3 downloader"},
        {"command": "yt2m", "description": "🎵 YT link → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "resat", "description": "✅ Resat the Bot"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "logs", "description": "👁️ View Bot Activity"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation "},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"}
    ]
    requests.post(url, json={"commands": commands})

if __name__ == "__main__":
    reset_and_set_commands()
    notify_owner() 

bot.run()
