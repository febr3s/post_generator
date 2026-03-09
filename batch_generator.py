#!/usr/bin/env python3
# batch_generator.py
"""
Main script to run after curating books.
Loads all eligible books, creates posts for each, and exits.
"""
from data_loader import load_books, get_posted_keys
from selector import select_books
from post_creator import create_post
from scheduler import count_posting_days
import sys

def main():
    print("=== Batch Post Generator ===\n")

    # 1. Load all books with abstracts
    books = load_books()
    print(f"Loaded {len(books)} books with abstracts")

    # 2. Get already posted keys
    posted_keys = get_posted_keys()
    print(f"Already posted: {len(posted_keys)} books")

    # 3. Count available posting slots
    total_slots = count_posting_days()
    existing_posts = len(posted_keys)
    available_slots = total_slots - existing_posts
    print(f"Posting slots: {total_slots} total, {available_slots} available")

    if available_slots <= 0:
        print("No available posting slots. Exiting.")
        return

    # 4. Select eligible books (up to available slots)
    #    The selector already returns max 29 by default, but we cap at available_slots
    limit = min(29, available_slots)
    selected = select_books(books, posted_keys, limit=limit)

    if not selected:
        print("No eligible books found.")
        return

    print(f"\nSelected {len(selected)} books to process")

    # 5. Process each book
    success_count = 0
    for i, book in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] Processing {book.zotero_key}...")
        try:
            post = create_post(book)
            if post:
                success_count += 1
            else:
                print(f"   Failed to create post for {book.zotero_key}")
        except Exception as e:
            print(f"   Error: {e}")

    # 6. Summary
    print(f"\n=== Complete ===")
    print(f"Successfully created: {success_count}/{len(selected)} posts")
    print(f"Remaining slots: {available_slots - success_count}")

if __name__ == "__main__":
    main()