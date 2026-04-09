import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API KEYS ---
# Get these from https://aistudio.google.com/
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# Get these from https://www.pexels.com/api/
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY")

# Get these from https://elevenlabs.io/ (Optional: for high-quality voice cloning)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID", "YOUR_CLONED_VOICE_ID")

# --- SOCIAL MEDIA KEYS (Meta/YouTube) ---
# Meta Graph API (Instagram/Facebook)
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "YOUR_INSTAGRAM_ACCOUNT_ID")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "YOUR_FACEBOOK_PAGE_ID")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "YOUR_META_ACCESS_TOKEN")

# YouTube Data API
YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")

# --- PROFILE SYSTEM (Multi-Account) ---
PROFILES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles.json")

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as f:
            return json.load(f)
    # Default fallback
    return {
        "Royal Main": {
            "ig_id": INSTAGRAM_ACCOUNT_ID,
            "fb_id": FACEBOOK_PAGE_ID,
            "meta_token": META_ACCESS_TOKEN,
            "youtube_secret": YOUTUBE_CLIENT_SECRET_FILE,
            "niche": "wellness",
            "active": True
        }
    }

PROFILES = load_profiles()

# --- CONFIGURATION ---
TIMEZONE = "Africa/Johannesburg" # Cape Town / South Africa
POSTING_TIMES = ["07:00", "08:30", "10:00"] # Viral Morning Windows

# --- DIRECTORIES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
POSTS_DIR = os.path.join(BASE_DIR, "posts")

for d in [ASSETS_DIR, POSTS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)
