import asyncio

# Master memory buffers for queues status tracking
active_voice_chats = set() # Stores chat_id of chats having live operational VCs
queues = {}                # Chat-isolated playlists matrix arrays links data cache

async def get_queue_index(chat_id: int) -> int:
    if chat_id not in queues:
        queues[chat_id] = []
    return len(queues[chat_id]) + 1