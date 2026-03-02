# selector.py
from typing import List, Set
from models import Book

def select_books(books: List[Book], posted_keys: Set[str], limit: int = 29) -> List[Book]:
    """
    Return the most recently modified books that:
    - have a note (assumed already filtered in books list)
    - are not in posted_keys
    
    Args:
        books: list of Book objects (should already have notes)
        posted_keys: set of Zotero keys already used
        limit: maximum number to return (default 29)
    
    Returns:
        List of Book objects sorted by date_modified descending, limited to limit.
    """
    # Filter out already posted books
    eligible = [book for book in books if book.zotero_key not in posted_keys]
    
    # Sort by date_modified descending (newest first)
    eligible.sort(key=lambda b: b.date_modified, reverse=True)
    
    # Limit the result
    selected = eligible[:limit]
    
    if len(selected) < limit:
        print(f"Warning: Only {len(selected)} eligible books found (requested {limit})")
    
    return selected