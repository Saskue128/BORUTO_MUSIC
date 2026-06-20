import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Access global matrix loops markers mapping from parent instances runtime system hooks
from main import tagging_tasks

@Client.on_message(filters.command("tagall") & filters.group)
async def isolated_tagall_module_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    user = await client.get_chat_member(chat_id, msg.from_user.id)
    if user.status.name not in ["OWNER", "ADMINISTRATOR"]:
        return

    tag_text = msg.text.split(None, 1)[1] if len(msg.command) > 1 else "Attention Members!"
    tagging_tasks[chat_id] = True
    batch = []
    
    async for member in client.get_chat_members(chat_id):
        if not tagging_tasks.get(chat_id):
            break
        if member.user.is_bot or member.user.is_deleted:
            continue
            
        batch.append(member.user.mention)
        if len(batch) == 5:
            await client.send_message(chat_id, f"{', '.join(batch)}\n\n📢 {tag_text}")
            batch = []
            await asyncio.sleep(2.5)

    if tagging_tasks.get(chat_id) and batch:
        await client.send_message(chat_id, f"{', '.join(batch)}\n\n📢 {tag_text}")
    tagging_tasks[chat_id] = False