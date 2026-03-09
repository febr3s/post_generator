# data_loader.py
import csv
import os
from typing import List, Set
from models import Book, Post
from config import ZOTERO_CSV_PATH, POSTS_DB_PATH

def load_books() -> List[Book]:
    """Load all books from Zotero CSV that have notes."""
    books = []
    try:
        with open(ZOTERO_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Abstract Note'):  # only books with notes
                    books.append(Book.from_csv_row(row))
    except FileNotFoundError:
        print(f"Error: Zotero CSV not found at {ZOTERO_CSV_PATH}")
    return books

def load_posts() -> List[Post]:
    """Load all existing posts from posts.csv."""
    posts = []
    if not os.path.exists(POSTS_DB_PATH):
        return posts
    with open(POSTS_DB_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append(Post.from_csv_row(row))
    return posts

def save_post(post: Post) -> None:
    """Append a single post to posts.csv."""
    file_exists = os.path.exists(POSTS_DB_PATH)
    with open(POSTS_DB_PATH, 'a', encoding='utf-8', newline='') as f:
        row = post.to_csv_row()
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def get_posted_keys() -> Set[str]:
    """Return set of Zotero keys that have already been posted."""
    return {p.zotero_key for p in load_posts()}