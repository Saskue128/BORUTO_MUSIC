import sys
from pyrogram import Client
from pytgcalls import PyTgCalls
import config

# STRING_SESSION Missing Verification Check Block
if not config.STRING_SESSION or not config.STRING_SESSION.strip():
    print("\n" + "="*60)
    print("[CRITICAL ERROR] Assistant STRING_SESSION missing inside config layer!")
    print("👉 FIX: Please add a valid Pyrogram/Telethon String Session inside your .env file.")
    print("="*60 + "\n")
    sys.exit(1)

print("[INFO] Initializing Assistant String Session Node...")

# 🚀 Initialize Autonomous Client Instance Matrix
assistant_client = Client(
    name="BorutoAssistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION
)

# 🎵 Pytgcalls VoIP Engine Core Binding Router
call_py = PyTgCalls(assistant_client)

print("[SUCCESS] Assistant Client Modules Armed Safely.")


# ==========================================
# ⚡ CORE USERBOT LIFECYCLE INITIALIZER LOGIC
# ==========================================
async def init_assistant(bot_instance: Client):
    """
    Starts the userbot assistant engine nodes and broadcasts 
    operational initialization status directly to the Log Group.
    """
    try:
        print("[INFO] Authorizing Userbot Assistant Client Instance...")
        await assistant_client.start()
        
        # 🎵 Starting PyTgCalls Subsystem Nodes Safely
        await call_py.start()
        
        assistant_identity = await assistant_client.get_me()
        print(f"[SUCCESS] Assistant authorized as: {assistant_identity.first_name}")
        
        # 🔔 AUTOMATED LOG GROUP BROADCAST OVERRIDE ON REBOOT
        log_payload = (
            f"<b>👤 ᴀssɪsᴛᴀɴᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ... ⚡</b>\n\n"
            f"👤 <b>ɴᴀᴍᴇ:</b> {assistant_identity.first_name}\n"
            f"🆔 <b>ᴜsᴇʀ ID:</b> <code>{assistant_identity.id}</code>\n"
            f"⚙️ <b>sᴛᴀᴛᴜs:</b> <code>Voice Chat Routing Nodes Connected Operational</code>"
        )
        
        if config.LOG_GROUP_ID != 0:
            await bot_instance.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=log_payload
            )
            print("[SUCCESS] Operational reboot alert dispatched to Log Group.")
            
    except Exception as e:
        print(f"\n" + "="*60)
        print(f"[FATAL USERBOT LIFECYCLE CRASH DETECTED]: {e}")
        print("👉 HINT: Session string expire ho gayi hai ya PyTgCalls ka alignment toota hai.")
        print("="*60 + "\n")
        sys.exit(1)