import yaml
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
import config

with open("strings/langs/en.yml", "r", encoding="utf-8") as f:
    strings = yaml.safe_load(f)

# ==========================================
# 📥 EVENT 1 & 3: BOT ADDED TO A NEW GROUP
# ==========================================
@Client.on_message(filters.new_chat_members)
async def bot_added_to_group_handler(client: Client, msg: Message):
    bot_obj = await client.get_me()
    
    # Check if the added member is our bot identity
    for user in msg.new_chat_members:
        if user.id == bot_obj.id:
            chat_id = msg.chat.id
            chat_title = msg.chat.title
            adder_user = msg.from_user
            
            # 1. Fetch Group stats & metadata parameters
            members_count = await client.get_chat_members_count(chat_id)
            
            # Check public or private group link rules index
            if msg.chat.username:
                chat_link = f"https://t.me/{msg.chat.username}"
            else:
                try:
                    chat_link = await client.export_chat_invite_link(chat_id)
                except Exception:
                    chat_link = "@PRIVATE"

            # 2. DISPATCH LOG TO LOG GROUP (All Bold Text Pattern)
            log_caption = strings["log_new_group_desc"].format(
                chat_title=chat_title,
                chat_id=chat_id,
                chat_link=chat_link,
                members_count=members_count
            )
            
            # Button link strictly pointing to Tg redirection user_id URI scheme format
            log_button = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"ADDED BY : {adder_user.first_name}", url=f"tg://openmessage?user_id={adder_user.id}")]
            ])
            
            await client.send_photo(
                chat_id=config.LOG_GROUP_ID,
                photo=config.START_LOG_GROUP_IMG,
                caption=log_caption,
                reply_markup=log_button
            )

            # 3. SEND WELCOME IMAGE IN THE PRESENT GROUP INLINE ROW WITH 2 BUTTONS
            group_caption = strings["group_welcome_desc"].format(mention=adder_user.mention)
            
            group_buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ADD ME", url=f"https://t.me/{bot_obj.username}?startgroup=true"),
                    InlineKeyboardButton("CLOSE", callback_data="cb_close_panel_view")
                ]
            ])
            
            await msg.reply_photo(
                photo=config.GROUP_WELCOME_IMG,
                caption=group_caption,
                reply_markup=group_buttons
            )
            return


# ==========================================
# 📤 EVENT 2: BOT KICKED/REMOVED FROM A GROUP
# ==========================================
@Client.on_chat_member_updated()
async def bot_removed_from_group_handler(client: Client, update: ChatMemberUpdated):
    bot_obj = await client.get_me()
    
    # Match trace context conditions to see if current state update targets the bot entity identity
    if update.old_chat_member and update.old_chat_member.user.id == bot_obj.id:
        # Check if the new state status turns to Left or Banned parameter markers keys
        if update.new_chat_member and update.new_chat_member.status.name in ["LEFT", "BANNED"]:
            
            chat_title = update.chat.title
            chat_id = update.chat.id
            
            # Fetch execution actor context who ran the removal operation command pipeline
            remover_admin = update.from_user
            admin_mention = remover_admin.mention if remover_admin else "Unknown Admin/System Identity"

            # Dispatch removal warning metrics summaries back to Owner Log channel
            remove_caption = strings["log_remove_group_desc"].format(
                chat_title=chat_title,
                chat_id=chat_id,
                admin_mention=admin_mention
            )
            
            await client.send_photo(
                chat_id=config.LOG_GROUP_ID,
                photo=config.LEAVE_LOG_GROUP_IMG,
                caption=remove_caption
            )