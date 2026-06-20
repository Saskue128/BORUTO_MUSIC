import asyncio
from pyrogram import Client
import config

# Loading integrity testing frameworks & verification checkers
from strings.helpers import strings
from database.helpers import db
from userbot.assistant import bot_client, init_assistant # Loading updated components

# Setup Main Core Bot Client Client Node
bot_client_instance = Client(
    name="BorutoMusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="handlers")
)

async def start_music_bot_system_stack():
    print("[SYSTEM] Powering up Core Bot Client Identity...")
    await bot_client_instance.start()
    
    # 🎯 Trigger Assistant Initializer Layer with Log Group Dispatch Pipeline
    print("[SYSTEM] Synchronizing Assistant Userbot Session Protocols...")
    await init_assistant(bot_client_instance)
    
    print("\n==============================================")
    print("🔥 BORUTO MUSIC STREAM BOT IS ONLINE OPERATIONAL!")
    print("==============================================\n")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    from main import bot_client_instance as client_hook
    # Dynamic plugin integrity scanner execution hook points directly running via start routine
    asyncio.run(start_music_bot_system_stack())