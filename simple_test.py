# test_video_generator_with_real_data.py
from data_loader import load_books
from selector import select_books
from video_generator import generate_video
import os
from config import OUTPUT_DIR

print("=== Testing video_generator with real CSV data ===\n")

# Load books
books = load_books()
print(f"Loaded {len(books)} books with notes")

# Get one book (first eligible)
posted_keys = set()  # empty for testing
selected = select_books(books, posted_keys, limit=1)

if not selected:
    print("No books available")
    exit()

book = selected[0]
print(f"Selected book: {book.zotero_key}")
print(f"Date modified: {book.date_modified}")

# Extract excerpt
excerpt = book.extract_excerpt()
print(f"Excerpt length: {len(excerpt)} characters")
print(f"Excerpt preview: {excerpt[:100]}...")

# Generate video
print(f"\nGenerating video...")
try:
    video_path = generate_video(excerpt, book.zotero_key)
    print(f"✓ Video generated at: {video_path}")
    
    # Check files
    book_folder = os.path.join(OUTPUT_DIR, book.zotero_key)
    for i in range(1, 6):
        img = os.path.join(book_folder, f"fragment_{i}.png")
        if os.path.exists(img):
            print(f"  ✓ fragment_{i}.png exists ({os.path.getsize(img)} bytes)")
        else:
            print(f"  ✗ fragment_{i}.png missing")
    
    video = os.path.join(book_folder, "output.mp4")
    if os.path.exists(video):
        print(f"  ✓ output.mp4 exists ({os.path.getsize(video)} bytes)")
    else:
        print(f"  ✗ output.mp4 missing")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("\nTest complete.")