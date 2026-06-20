from pyrogram import Client, filters
from pyrogram.types import Message
from main import queues, tagging_tasks

@Client.on_message(filters.command("reset") & filters.group)
async def group_memory_variables_reset_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    user = await client.get_chat_member(chat_id, msg.from_user.id)
    if user.status.name not in ["OWNER", "ADMINISTRATOR"]:
        return
        
    # Flush local cache layers matrices securely
    if chat_id in queues:
        queues[chat_id] = []
    if chat_id in tagging_tasks:
        tagging_tasks[chat_id] = False
        
    await msg.reply_text("<b>🗑️ All local cache buffers, tagall queues, and playlist matrices have been purged successfully!</b>")