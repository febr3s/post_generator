#!/usr/bin/env python3
# daily_post.py
"""
Cron job script to send today's scheduled post via Telegram.
Runs daily (e.g., at 11:05) to check if there's a post scheduled for today at 11:00.
If found, sends the video with caption.
"""

import os
from datetime import datetime
from data_loader import load_posts
from notifier import send_video
from config import OUTPUT_DIR

def get_todays_post():
    """
    Return the first post scheduled for today (ignoring time).
    Returns None if none found.
    """
    today = datetime.now().date()
    all_posts = load_posts()
    for post in all_posts:
        if post.publish_datetime.date() == today:
            return post
    return None

def main():
    print(f"Daily post check at {datetime.now()}")

    post = get_todays_post()
    if not post:
        print("No post scheduled for today.")
        return

    print(f"Found post for today: {post.zotero_key} at {post.publish_datetime}")

    # Construct absolute video path
    video_abs_path = os.path.join(OUTPUT_DIR, post.video_source)
    if not os.path.exists(video_abs_path):
        print(f"ERROR: Video file not found: {video_abs_path}")
        return

    # Send to Telegram
    success = send_video(video_abs_path, caption=post.caption)
    if success:
        print("✅ Post sent successfully.")
    else:
        print("❌ Failed to send post.")

if __name__ == "__main__":
    main()