# notifier.py
import requests
import os
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def is_enabled() -> bool:
    """Return True if Telegram notifications are configured."""
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

def send_message(text: str) -> bool:
    """
    Send a plain text message to the configured Telegram chat.
    Returns True if successful, False otherwise.
    """
    if not is_enabled():
        print("Telegram not configured – skipping message.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }

    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram send_message failed: {e}")
        return False

def send_video(video_path: str, caption: str = "") -> bool:
    """
    Send a video file to the configured Telegram chat.
    video_path should be an absolute path to an existing video file.
    Returns True if successful, False otherwise.
    """
    if not is_enabled():
        print("Telegram not configured – skipping video.")
        return False

    if not os.path.isfile(video_path):
        print(f"Video file not found: {video_path}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
    try:
        with open(video_path, 'rb') as f:
            files = {'video': f}
            r = requests.post(url, data=data, files=files, timeout=30)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram send_video failed: {e}")
        return False

def send_status(text: str) -> bool:
    """
    Alias for send_message, used for weekly status updates.
    """
    return send_message(text)