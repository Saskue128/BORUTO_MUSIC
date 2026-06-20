from .helpers import db

# Collections Definitions Mapping
auth_users_collection = db["auth_users"]

# ==========================================
# 🔐 DATABASE OPERATION: AUTHORIZATION MANAGEMENT
# ==========================================

async def add_auth_user_to_db(chat_id: int, user_id: int):
    """Saves a user ID mapped directly to a specific group chat context."""
    await auth_users_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"chat_id": chat_id, "user_id": user_id}},
        upsert=True
    )

async def remove_auth_user_from_db(chat_id: int, user_id: int):
    """Purges a user ID from the authorization stack of a specific group."""
    await auth_users_collection.delete_one({"chat_id": chat_id, "user_id": user_id})

async def is_user_authorized_in_chat(chat_id: int, user_id: int) -> bool:
    """Checks if a user has special authorized validation keys inside the current chat."""
    found = await auth_users_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    return True if found else False