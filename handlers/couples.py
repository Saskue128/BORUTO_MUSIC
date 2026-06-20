import random
import yaml
from pyrogram import Client, filters
from pyrogram.types import Message
import config # Config import hona zaroori hai

with open("strings/langs/en.yml", "r", encoding="utf-8") as f:
    strings = yaml.safe_load(f)

@Client.on_message(filters.command("couples") & filters.group)
async def isolated_couples_game_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    chat_title = msg.chat.title
    
    pool = []
    async for member in client.get_chat_members(chat_id, limit=100):
        if not member.user.is_bot and not member.user.is_deleted:
            pool.append(member.user)
            
    if len(pool) < 2:
        pool = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                pool.append(member.user)

    if len(pool) < 2:
        await msg.reply_text("<b>❌ Error: Pairs calculate karne ke liye group me log available nahi hain!</b>")
        return
        
    p_a = random.choice(pool)
    p_b = random.choice(pool)
    
    if len(pool) > 1:
        while p_a.id == p_b.id:
            p_b = random.choice(pool)
        
    caption = strings["couples_template"].format(
        chat_title=chat_title,
        partner_a=p_a.mention,
        partner_b=p_b.mention
    )
    
    # 🎯 Ab ye direct config.py se COUPLES_IMG wala unique link uthayega
    await msg.reply_photo(
        photo=config.COUPLES_IMG,
        caption=caption
    )