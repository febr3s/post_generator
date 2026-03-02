# test_data_loader.py
from data_loader import load_books, load_posts, get_posted_keys

print("=== Testing data_loader ===\n")

books = load_books()
print(f"Books with notes: {len(books)}")
if books:
    print(f"First 5 keys: {[b.zotero_key for b in books[:5]]}")
    print(f"First book date_modified: {books[0].date_modified}")
else:
    print("No books loaded.")

print("\n---")

posts = load_posts()
print(f"Existing posts: {len(posts)}")
if posts:
    print(f"First post key: {posts[0].zotero_key}")
    print(f"First post date: {posts[0].publish_datetime}")

print("\n---")

posted_keys = get_posted_keys()
print(f"Posted keys count: {len(posted_keys)}")
if posted_keys:
    print(f"Posted keys sample: {list(posted_keys)[:5]}")

print("\nTest complete.")