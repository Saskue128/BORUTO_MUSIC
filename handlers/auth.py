import yaml
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# MongoDB Database abstract functions simulation layer
from database.mongo import (
    add_auth_user_to_db, 
    remove_auth_user_from_db, 
    is_user_authorized_in_chat
)

with open("strings/langs/en.yml", "r", encoding="utf-8") as f:
    strings = yaml.safe_load(f)

async def verify_is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    """Helper method to check if execution user has admin authorization tags."""
    if user_id == config.OWNER_ID:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status.name in ["OWNER", "ADMINISTRATOR"]:
            return True
    except Exception:
        pass
    return False


# ==========================================
# 🔐 COMMAND: /auth (Reply-Only & Chat-Isolated)
# ==========================================
@Client.on_message(filters.command("auth") & filters.group)
async def chat_isolated_auth_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    executor_user_id = msg.from_user.id

    # 1. Verification Block: Strict Admin Check Engine Interception
    is_admin = await verify_is_admin(client, chat_id, executor_user_id)
    if not is_admin:
        await msg.reply_text(strings["auth_admin_only_alert"])
        return

    # 2. Verification Block: Strict Reply Validation Constraint Check
    if not msg.reply_to_message:
        await msg.reply_text(strings["auth_reply_missing_alert"])
        return

    target_user = msg.reply_to_message.from_user
    if target_user.is_bot:
        await msg.reply_text("❌ System identities matching vectors restriction: Cannot authorize service bots.")
        return

    # 3. Execution Pipeline: MongoDB Core Registration Layer Trigger
    already_authorized = await is_user_authorized_in_chat(chat_id, target_user.id)
    if already_authorized:
        await msg.reply_text(strings["auth_already_present"].format(target_mention=target_user.mention))
        return

    # Saves specifically mapped to current group chat context link indices
    await add_auth_user_to_db(chat_id, target_user.id)
    await msg.reply_text(strings["auth_success_desc"].format(target_mention=target_user.mention))


# ==========================================
# 🔓 COMMAND: /unauth (Reply-Only & Chat-Isolated)
# ==========================================
@Client.on_message(filters.command("unauth") & filters.group)
async def chat_isolated_unauth_handler(client: Client, msg: Message):
    chat_id = msg.chat.id
    executor_user_id = msg.from_user.id

    # 1. Verification Block: Strict Admin Check Engine Interception
    is_admin = await verify_is_admin(client, chat_id, executor_user_id)
    if not is_admin:
        await msg.reply_text(strings["auth_admin_only_alert"])
        return

    # 2. Verification Block: Strict Reply Validation Constraint Check
    if not msg.reply_to_message:
        await msg.reply_text(strings["auth_reply_missing_alert"])
        return

    target_user = msg.reply_to_message.from_user

    # 3. Execution Pipeline: MongoDB Data Removal Operation Purge
    is_authorized = await is_user_authorized_in_chat(chat_id, target_user.id)
    if not is_authorized:
        await msg.reply_text(strings["unauth_not_present"].format(target_mention=target_user.mention))
        return

    await remove_auth_user_from_db(chat_id, target_user.id)
    await msg.reply_text(strings["unauth_not_present"].format(target_mention=target_user.mention))