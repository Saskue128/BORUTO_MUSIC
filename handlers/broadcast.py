import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config
from database.mongo import db # Optional Mongo tracking schema link

@Client.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def global_gcast_broadcaster_node(client: Client, msg: Message):
    if not msg.reply_to_message:
        await msg.reply_text("<b>⚠️ Error: Reply to a message or media packet vector to broadcast!</b>")
        return
        
    status_update_msg = await msg.reply_text("<b>⚡ Deploying global packets across chat nodes arrays...</b>")
    
    # Static fallback array if collection lookup index isn't operational yet
    target_chats_list = []
    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type.name in ["GROUP", "SUPERGROUP"]:
                target_chats_list.append(dialog.chat.id)
    except Exception as e:
        print(f"[-] Dialog fetch intercept exception: {e}")

    success_count = 0
    failure_count = 0
    
    for c_id in target_chats_list:
        try:
            await msg.reply_to_message.copy(chat_id=c_id)
            success_count += 1
            await asyncio.sleep(0.3) # Floodwait escape bypass protection lock
        except Exception:
            failure_count += 1
            
    await status_update_msg.edit_text(
        f"<b>📊 BROADCAST DISPATCH COMPLETED:</b>\n\n"
        f"✅ <b>sᴜᴄᴄᴇss :</b> <code>{success_count} chats</code>\n"
        f"❌ <b>ꜰᴀɪʟᴇᴅ :</b> <code>{failure_count} chats</code>"
    )