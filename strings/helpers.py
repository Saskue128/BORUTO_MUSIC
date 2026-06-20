import os
import sys
import yaml

# en.yml ka absolute path configurations match karne ke liye
YML_FILE_PATH = os.path.join(os.path.dirname(__file__), "langs", "en.yml")

def load_localization_strings():
    """
    Safely loads the language yaml strings core block.
    Catches any structural syntax errors and dumps them directly to the terminal.
    """
    if not os.path.exists(YML_FILE_PATH):
        print(f"[-] CRITICAL DATABASE ERROR: Localization target file missing at '{YML_FILE_PATH}'!")
        sys.exit(1)
        
    try:
        with open(YML_FILE_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data:
                print("[-] WARNING: 'en.yml' file is completely empty or corrupted indices!")
                return {}
            print("[SUCCESS] Localization Engine loaded all language strings securely.")
            return data
            
    except yaml.YAMLError as syntax_error:
        print("\n" + "="*60)
        print("❌ CRITICAL SYNTAX ERROR DETECTED INSIDE strings/langs/en.yml")
        print(f"⚠️ DETAILS: {syntax_error}")
        print("="*60 + "\n")
        # System ko exit kar dega taaki galat text ke sath bot run na ho
        sys.exit(1)
    except Exception as general_error:
        print(f"[-] Unexpected Localization Pipeline Exception: {general_error}")
        sys.exit(1)

# Globally accessible variables pool dictionary array indices
strings = load_localization_strings()