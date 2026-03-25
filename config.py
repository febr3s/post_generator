# config.py
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

# Paths - adjust these as needed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZOTERO_CSV_PATH = os.path.join(BASE_DIR, '../../BibAV/assets/data/books_zotero.csv')  # Path to the Zotero export CSV
POSTS_DB_PATH = os.path.join(BASE_DIR, 'posts.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'video_output')  # Will create subfolders by Zotero key

# Date range for posting schedule (91 days)
START_DATE = datetime(2026, 3, 25)  # First Monday of the cycle (year, month, day)
END_DATE = START_DATE + timedelta(days=91)

# Posting schedule
POSTING_DAYS = [0, 2, 5]  # Monday=0, Wednesday=2, Saturday=5
POSTING_HOUR = 11
POSTING_MINUTE = 0

# Video generation settings
VIDEO_SETTINGS = {
    'image_size': '1080x1080',
    'background_color': '#C6C8C4',
    'text_color': '#2a3425',
    'font': 'AvantGarde-Book',
    'font_size': 115,
    'line_width': 70,  # characters per line for fold
    'fragment_duration': 3,  # seconds per fragment
    'transition_duration': 1,  # seconds for fade
    'fps': 30
}

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Set to None to disable notifications
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def validate_config():
    """Check if required directories exist and create them if needed"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if Zotero CSV exists
    if not os.path.exists(ZOTERO_CSV_PATH):
        print(f"Warning: Zotero CSV not found at {ZOTERO_CSV_PATH}")
    
    # Check if posts DB exists
    if not os.path.exists(POSTS_DB_PATH):
        print(f"Info: Posts database will be created at {POSTS_DB_PATH}")
    
    # Check if Jekyll posts folder exists
    if not os.path.exists(JEKYLL_POSTS_PATH):
        print(f"Warning: Jekyll posts folder not found at {JEKYLL_POSTS_PATH}")