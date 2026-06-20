import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError, OperationFailure
import config

def initialize_mongodb_safely():
    """
    Safely establishes connection with MongoDB Atlas Cluster.
    Catches credential issues, wrong URIs, or network timeouts, 
    and prints a clean diagnostic error directly to the terminal.
    """
    if not config.MONGO_DB_URI:
        print("\n" + "="*60)
        print("❌ CRITICAL DATABASE ERROR: MONGO_DB_URI is missing inside .env file!")
        print("⚠️ FIX: Please add your MongoDB connection string in your environment.")
        print("="*60 + "\n")
        sys.exit(1)
        
    try:
        print("[INFO] Connecting to MongoDB Atlas Cluster Instance...")
        # Connection timeout ko 5000ms (5 seconds) par set kiya hai taaki lamba wait na karna pade
        client = AsyncIOMotorClient(config.MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        
        # Ek dummy command execute karke check karenge ki server sach me respond kar raha hai ya nahi
        # Kyunki motor asynchronous hai, isliye connection verify karne ke liye ye zaruri hai
        client.admin.command('ping')
        
        db_instance = client["BorutoMusicDB"]
        print("[SUCCESS] MongoDB Cloud Cluster Connection Protocols Fully Established.")
        return db_instance
        
    except ConfigurationError as config_err:
        print("\n" + "="*60)
        print("❌ CRITICAL MONGODB CONFIGURATION ERROR")
        print(f"⚠️ DETAILS: {config_err}")
        print("👉 HINT: Check if your MongoDB URI format is correct (e.g., username or password issues).")
        print("="*60 + "\n")
        sys.exit(1)
        
    except OperationFailure as auth_err:
        print("\n" + "="*60)
        print("❌ CRITICAL MONGODB AUTHENTICATION FAILED")
        print(f"⚠️ DETAILS: {auth_err}")
        print("👉 HINT: Your database username or password inside the URI is invalid.")
        print("="*60 + "\n")
        sys.exit(1)
        
    except Exception as network_err:
        print("\n" + "="*60)
        print("❌ CRITICAL DATABASE CONNECTION TIMEOUT / NETWORK ERROR")
        print(f"⚠️ DETAILS: {network_err}")
        print("👉 HINT: Check your VPS/Termux internet connection or Atlas IP Whitelist settings!")
        print("="*60 + "\n")
        sys.exit(1)

# Globally accessible database instance
db = initialize_mongodb_safely()