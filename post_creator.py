# post_creator.py
import os
import random
from datetime import datetime
from typing import Optional, List

from models import Book, Post
from data_loader import load_posts, save_post
from scheduler import generate_schedule
from video_generator import generate_video


def get_next_free_date(existing_dates: set) -> Optional[datetime]:
    """Return the earliest unused posting date from the schedule."""
    for date in generate_schedule():
        if date not in existing_dates:
            return date
    return None


def generate_caption(book: Book) -> str:
    """
    Generate the post caption using the template and book fields.
    The template includes alternating expressions and conditional logic.
    """
    # List of possible verbs to alternate (randomly chosen here)
    verbos = [
        "reprodujo",
        "imprimió",
        "llevó a la imprenta",
        "tiró",
        "editó"
    ]
    verbo = random.choice(verbos)

    # Determine if there is a blurb (book.blurb is boolean)
    blurb_text = "de la que" if book.blurb else "donde"

    # Handle edition for "por primera vez"
    primera_vez = " por primera vez" if book.edition == 1 else ""

    # The excerpt (from abstract) – we assume it's already the right length
    excerpt = book.extract_excerpt()

    # Build the caption piece by piece
    # Note: The template uses "{{ book.Notes % picado en <!--post--> }}" for the excerpt.
    # We'll insert the excerpt directly.
    caption = f"En {book.year} {book.publisher} {verbo} _{book.title}_, de {book.author}, "
    caption += f"{blurb_text}{primera_vez} dijeron que: «{excerpt}». "

    if book.library:
        caption += f"Una copia se conserva en {book.library}. "

    caption += "Hoy está respaldada en el archivo público de BibAV.\n\n"
    caption += "¿Tienes alguna información que agregar o corregir sobre este título o esta copia? Déjala en comentarios.\n\n"
    caption += "Encuentra el link de descarga, portada y libros relacionados en BibAV (link en bio)"

    return caption


def create_post(book: Book) -> Optional[Post]:
    """
    Create a single post for the given book:
    - Find next free posting date
    - Generate video
    - Generate caption
    - Save to posts.csv
    Returns the Post object or None if no dates left.
    """
    # 1. Get used dates
    existing_posts = load_posts()
    used_dates = {p.publish_datetime for p in existing_posts}

    # 2. Next free date
    publish_date = get_next_free_date(used_dates)
    if publish_date is None:
        print(f"Error: No free posting dates left for {book.zotero_key}")
        return None

    # 3. Generate video
    try:
        video_path = generate_video(book.extract_excerpt(), book.zotero_key)
    except Exception as e:
        print(f"Video generation failed for {book.zotero_key}: {e}")
        return None

    # 4. Generate caption
    caption = generate_caption(book)

    # 5. Create and save post
    post = Post(
        zotero_key=book.zotero_key,
        publish_datetime=publish_date,
        video_source=video_path,
        caption=caption
    )
    save_post(post)
    print(f"✅ Created post for {book.zotero_key} on {publish_date.strftime('%Y-%m-%d %H:%M')}")

    return post