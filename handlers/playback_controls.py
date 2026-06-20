import asyncio
import yaml
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config
from utils.helpers import active_voice_chats, queues, get_queue_index
from utils.youtube import YouTube
from utils.thumbnail import generate_dynamic_thumbnail
from userbot.assistant import assistant_client # Assistant Userbot instance
from userbot.helpers import resolve_and_join_assistant

with open("strings/langs/en.yml", "r", encoding="utf-8") as f:
    strings = yaml.safe_load(f)

@Client.on_message(filters.command("play") & filters.group)
async def dynamic_play_stream_command_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    chat_name = msg.chat.title
    
    # 1. Check Voice Chat state flag cache link
    if chat_id not in active_voice_chats:
        await msg.reply_text(strings["vc_not_active"])
        return

    # Extract command arguments string query vector strings
    if len(msg.command) < 2:
        await msg.reply_text("<b>⚠️ Usage: /play [Song name or YouTube Link]</b>")
        return
        
    query_str = msg.text.split(None, 1)[1]
    
    # 2. Check Assistant Presence or Ban Interceptor System Core
    assistant_info = await assistant_client.get_me()
    join_success = await resolve_and_join_assistant(client, assistant_client, chat_id)
    
    if not join_success:
        # If assistant banned, delete the user /play message first
        try:
            await msg.delete()
        except Exception:
            pass
            
        alert_text = strings["assistant_banned_alert"].format(
            group_name=chat_name,
            assistant_id=assistant_info.id
        )
        await client.send_message(chat_id, alert_text)
        return

    # 3. Queue Logic Routing
    if chat_id in queues and len(queues[chat_id]) > 0:
        # Song already playing scenario -> Fetch tracking details to store inside playlist array
        find_msg = await msg.reply_text(strings["finding_track"])
        vidid, title, duration = await YouTube.search(query_str)
        await find_msg.delete()
        
        if not vidid:
            await msg.reply_text("<b>❌ Tracks matching query matrices not found on YouTube server links.</b>")
            return
            
        q_position = await get_queue_index(chat_id)
        queues[chat_id].append({"title": title, "vidid": vidid, "duration": duration})
        
        queue_msg = strings["queue_added_template"].format(
            q_num=q_position,
            title=title,
            duration=duration,
            mention=msg.from_user.mention
        )
        close_btn = InlineKeyboardMarkup([[InlineKeyboardButton("CLOSE PANEL", callback_data="cb_close_panel_view")]])
        await msg.reply_text(queue_msg, reply_markup=close_btn)
        return

    # 4. First Track Playing Node Logic Pipeline
    prep_msg = await msg.reply_text(strings["preparing_track"])
    
    # Perform Search via working multi-client yt-dlp API logic
    vidid, title, duration = await YouTube.search(query_str)
    if not vidid:
        await prep_msg.delete()
        await msg.reply_text("<b>❌ Tracks matching query matrices not found on YouTube server links.</b>")
        return
        
    # Extract Direct playing Stream URL
    status_code, stream_link_url = await YouTube.video(link=None, videoid=vidid)
    await prep_msg.delete() # Delete preparing track message instantly
    
    if status_code == 0:
        await msg.reply_text(f"<b>❌ Stream Generation Failure: {stream_link_url}</b>")
        return
        
    # Append to isolated active queue structure
    queues[chat_id] = [{"title": title, "vidid": vidid, "duration": duration}]
    
    # Get adaptive thumbnail link
    track_details, _ = await YouTube.track(link=None, videoid=vidid)
    thumb_display_url = await generate_dynamic_thumbnail(track_details.get("thumb"))
    
    # Trigger PyTgCalls system call stream pipeline logic here
    # from userbot.assistant import call_py -> call_py.join_group_call(...)
    
    now_playing_desc = f"<b>✨ ɴᴏᴡ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ sᴇsssɪᴏɴ :</b>\n\n<blockquote><b>🎵 ᴛɪᴛʟᴇ : {title}</b>\n<b>🕐 ᴅᴜʀᴀᴛɪᴏɴ : {duration}</b>\n<b>👤 ʀᴇǫᴜᴇsᴛᴇᴅ : {msg.from_user.mention}</b></blockquote>"
    await msg.reply_photo(photo=thumb_display_url, caption=now_playing_desc)