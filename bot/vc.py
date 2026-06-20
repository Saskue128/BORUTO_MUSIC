import yaml
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.types import UpdateGroupCall
from utils.helpers import active_voice_chats

with open("strings/langs/en.yml", "r", encoding="utf-8") as f:
    strings = yaml.safe_load(f)

@Client.on_raw_update()
async def raw_voice_chat_status_monitor(client: Client, update, users, chats):
    """
    Listens specifically to Raw UpdateGroupCall signals on the Telegram network.
    Safely captures live updates if VC changes status flags state.
    """
    if isinstance(update, UpdateGroupCall):
        chat_id = -int(update.chat_id) if update.chat_id > 0 else update.chat_id
        
        # Checking inner boolean flags properties of update structure parameters keys
        if update.call and not update.call.banned_rights:
            # VC Started Status Block Flow
            if chat_id not in active_voice_chats:
                active_voice_chats.add(chat_id)
                try:
                    await client.send_message(chat_id, strings["vc_started_desc"])
                except Exception:
                    pass
        else:
            # VC Ended Status Block Flow
            if chat_id in active_voice_chats:
                active_voice_chats.remove(chat_id)
                try:
                    await client.send_message(chat_id, strings["vc_ended_desc"])
                except Exception:
                    pass