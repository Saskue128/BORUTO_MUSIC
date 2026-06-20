import yaml
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config              # 🎯 Central Config Link Matrix
from strings.helpers import strings  # 🎯 Safe localization parser helper loading hook

@Client.on_message(filters.command("start"))
async def private_start_entry_node_handler(client: Client, msg: Message):
    bot_obj = await client.get_me()
    caption = strings["welcome_root"].format(mention=msg.from_user.mention, bot_name=bot_obj.first_name)
    
    # Single major help panel access trigger hook
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("HELP AND COMMAND", callback_data="cb_open_matrix_panel")]
    ])
    
    # 🎯 Ab ye direct aapke config.py se START_DM_IMG (ya START_LOG_GROUP_IMG) uthayega!
    # Agar alag DM image banayi hai toh config.START_DM_IMG kar dena yahan.
    await msg.reply_photo(photo=config.START_LOG_GROUP_IMG, caption=caption, reply_markup=buttons)


@Client.on_callback_query(filters.regex("^cb_open_matrix_panel$|^cb_back_to_matrix$"))
async def help_matrix_dashboard_router(client: Client, cb: CallbackQuery):
    # Dynamic 3-Column Matrix Buttons Grid Rows Layers Setup
    matrix_buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ADMIN", callback_data="help_mod_admin"),
            InlineKeyboardButton("AUTH", callback_data="help_mod_auth"),
            InlineKeyboardButton("BLACKLIST", callback_data="help_mod_blacklist")
        ],
        [
            InlineKeyboardButton("BROADCAST", callback_data="help_mod_broadcast"),
            InlineKeyboardButton("PING", callback_data="help_mod_ping"),
            InlineKeyboardButton("PLAY", callback_data="help_mod_play")
        ],
        [
            InlineKeyboardButton("SUDO", callback_data="help_mod_sudo"),
            InlineKeyboardButton("VIDEOCHATS", callback_data="help_mod_vchats"),
            InlineKeyboardButton("START", callback_data="help_mod_start")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="cb_close_panel_view")
        ]
    ])
    
    await cb.message.edit_caption(caption=strings["play_panel_desc"], reply_markup=matrix_buttons)


# 🚀 UNIVERSAL HANDLER: Saare sub-modules ka data ek sath automatic handle karega bina code toote!
@Client.on_callback_query(filters.regex("^help_mod_(admin|auth|blacklist|broadcast|ping|play|sudo|vchats|start)$"))
async def universal_help_modules_router(client: Client, cb: CallbackQuery):
    selected_module = cb.data.replace("help_mod_", "")
    yml_target_key = f"help_{selected_module}_desc"
    
    back_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("BACK", callback_data="cb_back_to_matrix")]
    ])
    
    if yml_target_key in strings:
        await cb.message.edit_caption(caption=strings[yml_target_key], reply_markup=back_btn)
    else:
        await cb.answer(f"❌ Sub-module string key '{yml_target_key}' missing inside en.yml!", show_alert=True)


@Client.on_callback_query(filters.regex("^cb_close_panel_view$"))
async def close_panel_execution_handler(client: Client, cb: CallbackQuery):
    await cb.message.delete()