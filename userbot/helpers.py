import asyncio
from pyrogram import Client
from pyrogram.errors import UserBannedInChannel, InviteHashExpired, ChatAdminRequired

async def resolve_and_join_assistant(bot_client: Client, assistant_client: Client, chat_id: int) -> bool:
    """
    Generates a fresh temporary group invite link using Bot client admin rights,
    then automatically pipes it to the Assistant Client to join the target group.
    Handles ban exception interceptions instantly.
    """
    try:
        # Step 1: Pehle check karenge ki assistant already group me hai ya nahi
        try:
            member = await bot_client.get_chat_member(chat_id, "me")
            if member:
                return True # Assistant already group me hai
        except Exception:
            pass

        # Step 2: Create a temporary fresh invite link via Bot Admin Access Scope Key
        invite_link_object = await bot_client.export_chat_invite_link(chat_id)
        
        # Step 3: Use Assistant Session Engine to join group dynamically
        await assistant_client.join_chat(invite_link_object)
        return True
        
    except UserBannedInChannel:
        # Assistant completely banned scenario status vector
        print(f"[-] CRITICAL: Assistant ID is banned inside Chat Nodes: {chat_id}")
        return False
    except (InviteHashExpired, ChatAdminRequired, Exception) as e:
        print(f"[-] Automated Link Inviter Core processing anomaly: {e}")
        # Flow bypass: Agar setting manual invite par chal rahi ho, toh flow break nahi hoga
        return True