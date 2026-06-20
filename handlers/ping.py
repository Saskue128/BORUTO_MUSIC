import time
from pyrogram import Client, filters
from pyrogram.types import Message
import config # Config parameters loading hook

@Client.on_message(filters.command("ping"))
async def system_ping_latency_handler(client: Client, msg: Message):
    start_time = time.time()
    
    # Pehle system message send karke latency calculate karenge
    response_msg = await msg.reply_text("<b>⚡ Checking System Latency Core Vectors...</b>")
    
    end_time = time.time()
    ping_ms = round((end_time - start_time) * 1000, 2)
    
    # Text calculate hone ke baad initial temporary message ko delete karenge
    await response_msg.delete()
    
    caption = (
        f"<b>📊 ʙᴏʀᴜᴛᴏ ᴍᴜsɪᴄ ᴛᴇʟᴇᴍᴇᴛʀʏ :</b>\n\n"
        f"<blockquote>🚀 <b>ᴘɪɴɢ :</b> <code>{ping_ms} ms</code>\n"
        f"⚙️ <b>sᴛᴀᴛᴜs :</b> <code>Operational Stable</code></blockquote>"
    )
    
    # 🎯 Config se PING_IMG resource load karke photo send karega
    await msg.reply_photo(
        photo=config.PING_IMG,
        caption=caption
    )