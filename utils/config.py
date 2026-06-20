import os

API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "abcdef1234567890abcdef1234567890")
BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://user:pass@cluster.mongodb.net/myDb")
STRING_SESSION = os.getenv("STRING_SESSION", "")  # Userbot runtime string context
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1001234567890"))

COOKIES_FILE = os.getenv("COOKIES_FILE", "cookies.txt")

# Strict RCE & Command Injection Security Boundaries
ALLOWED_DOMAINS = [
    "youtube.com",
    "www.youtube.com", 
    "m.youtube.com",
    "youtu.be",
    "music.youtube.com"
]

BLOCKED_CHARS = [";", "|", "$", "`", "&", ">", "<", "\n", "\r", "\t", "!", "(", ")", "{", "}", "[", "]"]

# Inside config.py, append this:

COUPLES_IMG = os.getenv("COUPLES_IMG", "https://graph.org/file/6c125bbda5fcd489bc8be.jpg")
# Inside config.py, append this:

PING_IMG = os.getenv("PING_IMG", "https://graph.org/file/6c125bbda5fcd489bc8be.jpg")