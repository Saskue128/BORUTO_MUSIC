import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config

@Client.on_message(filters.command("reboot") & filters.user(config.OWNER_ID))
async def backend_server_reboot_handler(client: Client, msg: Message):
    reboot_alert = await msg.reply_text("<b>⚙️ Restructuring System Nodes... Killing Python Instance Event Loops.</b>")
    await asyncio.sleep(2)
    
    await reboot_alert.edit_text("<b>♻️ Active Framework Online! Hot Reload Successful.</b>")
    
    # Python script execution lifecycle restart trigger hook
    os.execl(sys.executable, sys.executable, *sys.argv)