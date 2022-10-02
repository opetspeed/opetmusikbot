import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import HNDLR, bot, call_py
from MusicUserbot.helpers.queues import QUEUE, add_to_queue, get_queue

AMBILFOTO = [
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
    "https://telegra.ph/file/613f681a511feb6d1b186.jpg",
]

IMAGE_THUMBNAIL = random.choice(AMBILFOTO)


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration = r["duration"]
        return [songname, url, duration]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
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


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration = r["duration"]
        return [songname, url, duration]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(filters.command(["play"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**✧ Memproses Request..**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
                duration = convert_seconds(replied.audio.duration)
            elif replied.voice:
                songname = "Voice Note"
                duration = convert_seconds(replied.voice.duration)
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/613f681a511feb6d1b186.jpg",
                    caption=f"""
**▶ ʟᴀɢᴜ ᴅɪ ᴀɴᴛʀɪᴀɴ ᴋᴇ** `{pos}`
🏷 **ᴊᴜᴅᴜʟ:** [{songname}]({link})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`
💡 **sᴛᴀᴛᴜs:** `Playing`
🎧 **ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
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
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/613f681a511feb6d1b186.jpg",
                    caption=f"""
**▶ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ʟᴀɢᴜ**
🏷 **ᴊᴜᴅᴜʟ:** [{songname}]({link})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`
💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`
🎧 **ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("Balas ke File Audio atau berikan sesuatu untuk Pencarian")
        else:
            await m.delete()
            huehue = await m.reply("**✧ Sedang Mencari Lagu... Mohon Bersabar**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`Tidak Menemukan Apapun untuk Kueri yang Diberikan`")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR âš ï¸** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**▶ ʟᴀɢᴜ ᴅɪ ᴀɴᴛʀɪᴀɴ ᴋᴇ** `{pos}`
🏷 **ᴊᴜᴅᴜʟ:** [{songname}]({url})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`
💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`
🎧 **ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
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
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**▶ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ʟᴀɢᴜ**
🏷️ **ᴊᴜᴅᴜʟ:** [{songname}]({url})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ** `{duration}`
💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`
🎧 **ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["videoplay", "vplay"], prefixes=f"{HNDLR}"))
async def videoplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**✧ Memproses Video....**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "`Hanya 720, 480, 360 Diizinkan` \n`Sekarang Streaming masuk 720p`"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video File"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/613f681a511feb6d1b186.jpg",
                    caption=f"""
**▶ ᴠɪᴅᴇᴏ ᴅɪ ᴀɴᴛʀɪᴀɴ ᴋᴇ {pos}
🏷️ ᴊᴜᴅᴜʟ: [{songname}]({link})
💡 sᴛᴀᴛᴜs: ᴘʟᴀʏɪɴɢ
🎧 ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ: {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/613f681a511feb6d1b186.jpg",
                    caption=f"""
**▶ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ᴠɪᴅᴇᴏ
🏷️ ᴊᴜᴅᴜʟ: [{songname}]({link})
💡 sᴛᴀᴛᴜs: ᴘʟᴀʏɪɴɢ
🎧 ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "**ʙᴀʟᴀs ᴋᴇ ꜰɪʟᴇ ᴀᴜᴅɪᴏ ᴀᴛᴀᴜ ʙᴇʀɪᴋᴀɴ sᴇsᴜᴀᴛᴜ ᴜɴᴛᴜᴋ ᴘᴇɴᴄᴀʀɪᴀɴ**"
            )
        else:
            await m.delete()
            huehue = await m.reply("**ðŸ”Ž ᴘᴇɴᴄᴀʀɪᴀɴ ʟᴀɢᴜ... ᴍᴏʜᴏɴ ʙᴇʀsᴀʙᴀʀ**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**ᴛɪᴅᴀᴋ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴀᴘᴀ ᴘᴜɴ ᴜɴᴛᴜᴋ ᴋᴜᴇʀɪ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ**"
                )
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR âš ï¸** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**▶ ᴠɪᴅᴇᴏ ᴅɪ ᴀɴᴛʀɪᴀɴ ᴋᴇ** `{pos}`
🏷️ **ᴊᴜᴅᴜʟ:** [{songname}]({url})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`
💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`
🎧 **ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**▶ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ᴠɪᴅᴇᴏ**
🏷️ **ᴊᴜᴅᴜʟ:** [{songname}]({url})
⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`
💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`
🎧 **ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ:** {m.from_user.mention}
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playfrom"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**𝙿𝙴𝙽𝙶𝙶𝚄𝙽𝙰𝙰𝙽:** \n\n`{HNDLR}playfrom [chat_id/username]` \n`{HNDLR}playfrom [chat_id/username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**✧ ᴍᴇɴɢᴀᴍʙɪʟ {limit} ʟᴀɢᴜ ᴀᴄᴀᴋ ᴅᴀʀɪ {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://telegra.ph/file/613f681a511feb6d1b186.jpg",
                        caption=f"""
**▶ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ʟᴀɢᴜ ᴅᴀʀɪ {chat}
🏷️ ᴊᴜᴅᴜʟ: [{songname}]({link})
💡 sᴛᴀᴛᴜs: ᴘʟᴀʏɪɴɢ
🎧 ᴀᴛᴀs ᴘᴇʀᴍɪɴᴛᴀᴀɴ: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"âž• ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ {lmt} ʟᴀɢᴜ ᴋᴇ ᴅᴀʟᴀᴍ ᴀɴᴛʀɪᴀɴ\nâ€¢ ᴋʟɪᴋ {HNDLR}ᴘʟᴀʏʟɪsᴛ ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴘᴜᴛᴀʀ**"
            )
        except Exception as e:
            await hmm.edit(f"**ERROR** \n`{e}`")


@Client.on_message(filters.command(["playlist", "queue"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**✧ 𝚂𝙴𝙺𝙰𝚁𝙰𝙽𝙶 𝙼𝙴𝙼𝚄𝚃𝙰𝚁:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**✧ 𝚂𝙴𝙺𝙰𝚁𝙰𝙽𝙶 𝙼𝙴𝙼𝚄𝚃𝙰𝚁:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**â¯ DAFTAR ANTRIAN:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**✧ ᴛɪᴅᴀᴋ ᴍᴇᴍᴜᴛᴀʀ ᴀᴘᴀᴘᴜɴ...**")
