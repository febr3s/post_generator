#!/usr/bin/env python3
# batch_generator.py
"""
Main script to run after curation.
Loads all eligible books, creates posts for up to the available posting slots,
and saves them to the schedule.
"""

from data_loader import load_books, get_posted_keys, load_posts
from selector import select_books
from post_creator import create_post
from scheduler import count_posting_days
import sys

def main():
    print("=== Batch Post Generator ===\n")

    # 1. Load books (only those with abstracts)
    books = load_books()
    print(f"Loaded {len(books)} books with abstracts")

    # 2. Get already posted keys
    posted_keys = get_posted_keys()
    print(f"Already posted: {len(posted_keys)} books")

    # 3. Count total posting slots and available slots
    total_slots = count_posting_days()
    available_slots = total_slots - len(posted_keys)
    print(f"Posting slots: {total_slots} total, {available_slots} available")

    if available_slots <= 0:
        print("No available posting slots. Exiting.")
        return

    # 4. Select books to process (max 29, but not more than available slots)
    limit = min(29, available_slots)
    selected_books = select_books(books, posted_keys, limit=limit)

    if not selected_books:
        print("No eligible books found.")
        return

    print(f"\nSelected {len(selected_books)} books to process (max {limit})")

    # 5. Process each book
    success_count = 0
    for i, book in enumerate(selected_books, 1):
        print(f"\n[{i}/{len(selected_books)}] Processing {book.zotero_key}...")
        print(f"   Title: {book.title}")
        print(f"   Author: {book.author}")
        print(f"   Year: {book.year}")
        print(f"   Publisher: {book.publisher}")
        print(f"   Blurb: {book.blurb}")
        print(f"   Edition: {book.edition}")
        print(f"   Library: {book.library}")
        print(f"   Excerpt length: {len(book.extract_excerpt())} characters")

        try:
            post = create_post(book)
            if post:
                success_count += 1
                print(f"   ✅ Post created for {post.publish_datetime.strftime('%Y-%m-%d %H:%M')}")
            else:
                print(f"   ❌ create_post returned None (no free dates or error)")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

    # 6. Summary
    print(f"\n=== Complete ===")
    print(f"Successfully created: {success_count}/{len(selected_books)} posts")
    print(f"Remaining slots after this run: {available_slots - success_count}")

if __name__ == "__main__":
    main()