# test_post_creator.py
from data_loader import load_books, load_posts
from selector import select_books
from post_creator import create_post
import os
from config import OUTPUT_DIR

print("=== Testing post_creator with real CSV data ===\n")

# Load books
books = load_books()
print(f"Loaded {len(books)} books with abstracts")

# Get one eligible book (most recent, treat all as eligible for test)
selected = select_books(books, set(), limit=1)

if not selected:
    print("No books available")
    exit()

book = selected[0]
print(f"Selected book: {book.zotero_key}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Year: {book.year}")
print(f"Publisher: {book.publisher}")
print(f"Blurb: {book.blurb}")
print(f"Edition: {book.edition}")
print(f"Library: {book.library}")
print(f"Abstract excerpt length: {len(book.extract_excerpt())} characters")

# Create post
print(f"\nCreating post...")
try:
    post = create_post(book)
    if post:
        print(f"✅ Post created successfully!")
        print(f"   Zotero key: {post.zotero_key}")
        print(f"   Publish datetime: {post.publish_datetime}")
        print(f"   Video source: {post.video_source}")
        print(f"   Caption preview: {post.caption[:150]}...")

        # Verify video files
        book_folder = os.path.join(OUTPUT_DIR, book.zotero_key)
        video_path = os.path.join(book_folder, "output.mp4")
        if os.path.exists(video_path):
            print(f"   ✅ Video file exists: {video_path}")
        else:
            print(f"   ❌ Video file missing: {video_path}")

        # Verify post was saved to CSV
        all_posts = load_posts()
        matching = [p for p in all_posts if p.zotero_key == book.zotero_key]
        if matching:
            saved_post = matching[-1]
            print(f"   ✅ Post found in posts.csv")
            print(f"      Caption in CSV: {saved_post.caption[:100]}...")
        else:
            print(f"   ❌ Post not found in posts.csv")
    else:
        print(f"❌ create_post returned None (no free dates or error)")
except Exception as e:
    print(f"❌ Exception: {e}")

print("\nTest complete.")