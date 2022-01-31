# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import asyncio
import re

from config import BOT_USERNAME, GROUP_SUPPORT, IMG_1, IMG_2, UPDATES_CHANNEL
from driver.decorators import authorized_users_only
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:60] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["oynat", f"oynat@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def oynat(_, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🕊️", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="❤ ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply(" ⚡")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:60] + "..."
                else:
                    songname = replied.audio.file_name[:60] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"🎶 **parça sıraya eklendi **\n\n🍃 **adı:** [{songname}]({link})\n🥂 **Sohbet:** `{chat_id}`\n🕊️ **talep eden:** {m.from_user.mention()}\n👣 **At position »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"✅ **music akışı başlatıldı.**\n\n🎶 **isim:** [{songname}]({link})\n🕊️ **Sohbet:** `{chat_id}`\n🌿 **durum:** `Playing`\n👣 **Talep eden:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» reply to an **audio file** or **give something to search.**"
                )
            else:
                suhu = await m.reply("🔎 ")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **sonuç bulunamadı.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl sorunları algılandı")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"✅ **Parça sıraya eklendi **\n\n🍃**isim:** [{songname}]({url})\n🥂 **sohbet:** `{chat_id}`\n🕊**Talep eden:** {m.from_user.mention()}\n👣 **At position »** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"✅ **music akışı başladı.**\n\n👣 **isim:** [{songname}]({url})\n🕊️ **sohbet:** `{chat_id}`\n⚡ **durum:** `Playing`\n🎶 **Talep eden:** {m.from_user.mention()}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await m.reply_text(f"🚫 hata: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an **audio file** or **give something to search.**"
            )
        else:
            suhu = await m.reply("🔎 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **sonuç bulunamadı.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl sorunları algılandı")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"✅ **parça sıraya eklendi**\n\n🍃 **isim:** [{songname}]({url})\n🥂 **sohbet:** `{chat_id}`\n🕊 **Talep eden:** {m.from_user.mention()}\n👣 **At position »** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"⚡ **music akışı başladı.**\n\n🌿 **isim:** [{songname}]({url})\n🕊️ **sohbet:** `{chat_id}`\n⚛️ **durum:** `Playing`\n🎶 **Talep eden:** {m.from_user.mention()}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await m.reply_text(f"🚫 hata: `{ep}`")


# stream is used for live streaming only

@Client.on_message(command(["radio", f"radio@{BOT_USERNAME}"]) & other_filters)
async def radio(_, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⚛️", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="🕊️", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        link = m.text.split(None, 1)[1]
        suhu = await m.reply("♻️ **akım işleniyor...**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"✅ **parça sıraya eklendi **\n\n🕊️ **sohbet:** `{chat_id}`\n🎶 **Talep eden:** {m.from_user.mention()}\n👣 **At position »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            livelink,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                    await suhu.delete()
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"📡 **[Radio live]({link}) akış başladı.**\n\n🕊️ **sohbet:** `{chat_id}`\n⚡ **durum:** `Playing`\n🎶 **Talep eden:** {m.from_user.mention()}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await m.reply_text(f"🚫 hata: `{ep}`")


@Client.on_message(filters.command(["cplay", f"cplay@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def channel_play_list(client, m: Message):
with suppress(MessageIdInvalid, MessageNotModified):
k=await m.reply("Setting up for channel play..")
if " " in m.text:
you, me = m.text.split(" ", 1)
if me.startswith("-100"):
try:,
me=int(me)
except
await k.edit("Invalid chat id given")
await delete_messages([m, k])
return
try:
await client.get_chat_member(int(me), Config.USER_ID)
except (ValueError, PeerIdInvalid, ChannelInvalid):
LOGGER.error(f"Given channel is private and @{Config.BOT_USERNAME} is not an admin over there.", exc_info=True)
await k.edit(f"Given channel is private and @{Config.BOT_USERNAME} is not an admin over there. If channel is not private , please provide username of channel.") 
await delete_messages([m, k])
return
except UserNotParticipant:
LOGGER.error("Given channel is private and USER account is not a member of channel.") 
await k.edit(f"Given channel is private and @{Config.BOT_USERNAME} is not an admin over there. If channel is not private , please provide username of channel.") 
await delete_messages([m, k])
return
except Exception as e:
LOGGER.error(f"Errors occured while getting data abount channel - {e}", exc_info=True) 
await k.edit(f"Something went wrong- {e}") 
await delete_messages([m, k]) 
return 
await k.edit("Searching files from channel, this may take some time, depending on number of files in the channel.") 
st, msg = await c_play(me) 
if st == False: 
await m.edit(msg) 
else: 
await k.edit(f"Succesfully added {msg} files to playlist.") 
elif me.startswith("@"): 
me = me.replace("@", "")
 try
: chat=await client.get_chat(me)
 except Exception as e: 
LOGGER.error(f"Errors occured while fetching info about channel - {e}", exc_info=True) 
await k.edit(f"Errors occured while getting data about channel - {e}") await delete_messages([m, k]) 
return 
await k.edit("Searching files from channel, this may take some time, depending on number of files in the channel.") 
st, msg=await c_play(me) 
if st == False: 
await k.edit(msg) 
await delete_messages([m, k]) 
else: 
await k.edit(f"Succesfully Added {msg} files from {chat.title} to playlist") 
await delete_messages([m, k]) 
else: 
await k.edit("The given channel is invalid. For private channels it should start with -100 and for public channels it should start with @\nExamples - `/cplay @VCPlayerFiles or /cplay -100125369865\n\nFor private channel, both bot and the USER account should be members of channel.") 
await delete_messages([m, k]) 
else: 
await k.edit("You didn't gave me any channel. Give me a channel id or username from which i should play files . \nFor private channels it should start with -100 and for public channels it should start with @\nExamples - `/cplay @VCPlayerFiles or /cplay -100125369865\n\nFor private channel, both bot and the USER account should be members of channel.") 
await delete_messages([m, k]) 













