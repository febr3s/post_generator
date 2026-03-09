# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import re

@dataclass
class Book:
    """Represents a book from Zotero - only fields needed for processing"""
    zotero_key: str
    note_html: str 
    date_modified: datetime  # To find last modified items
    title: str
    author: str
    year: Optional[str]          # Some books may not have year
    publisher: Optional[str]
    blurb: bool                   # TRUE/FALSE in CSV
    edition: Optional[int]        # may be empty
    library: Optional[str]

    @classmethod

    def from_csv_row(cls, row: Dict[str, Any]) -> 'Book':
        # Helper to convert CSV string to boolean
        def to_bool(val: str) -> bool:
            return str(val).strip().upper() in ('TRUE', '1', 'YES')

        # Helper to convert to int if possible
        def to_int(val: str) -> Optional[int]:
            try:
                return int(val) if val else None
            except (ValueError, TypeError):
                return None
                
        return cls(
            zotero_key=row.get('Key', ''),
            note_html=row.get('Abstract Note', ''),
            date_modified=datetime.strptime(
                row.get('Date Modified', ''), 
                '%Y-%m-%d %H:%M:%S'
            ),
            # Add the missing fields:
            title=row.get('Title', ''),
            author=row.get('Author', ''),
            year=row.get('Publication Year', ''),
            publisher=row.get('Publisher', ''),
            blurb=to_bool(row.get('Blurb', '')),
            edition=to_int(row.get('Edition', '')),
            library=row.get('Library', '')
        )
        
    
    def extract_excerpt(self) -> str:
        """
        Extract the text from the note up to the <!--post--> mark.
        Strips HTML tags.
        """
        if not self.note_html:
            return ""
        
        # Find the post marker
        post_marker = '<!--post-->'
        marker_pos = self.note_html.find(post_marker)
        
        if marker_pos != -1:
            # Take everything before the marker
            excerpt_html = self.note_html[:marker_pos]
        else:
            # If no marker, take the whole note
            excerpt_html = self.note_html
        
        # Strip HTML tags (simple version - for production consider using BeautifulSoup)
        excerpt_text = re.sub(r'<[^>]+>', '', excerpt_html)
        # Clean up whitespace
        excerpt_text = re.sub(r'\s+', ' ', excerpt_text).strip()
        
        # Truncate to 350 characters from beginning (as per spec)
        if len(excerpt_text) > 350:
            excerpt_text = excerpt_text[:350]
        
        return excerpt_text

@dataclass
class Post:
    """Represents a generated social media post"""
    zotero_key: str
    publish_datetime: datetime  # When to post
    video_source: str  # Path to video file (relative)
    caption: str                    # NEW: the full caption text
        
    def to_csv_row(self) -> Dict[str, str]:
        """Convert to dictionary for CSV writing"""
        return {
            'Zotero key': self.zotero_key,
            'Publish time (day, date, time)': self.publish_datetime.strftime('%a, %-m-%-d-%Y, %I:%M %p'),
            'Video source': self.video_source,
            'Caption': self.caption,    # NEW column
            # Note: Captions will be read from markdown files when needed for posting
        }
    
    @classmethod
    def from_csv_row(cls, row: Dict[str, Any]) -> 'Post':
        """Create a Post instance from a CSV row dictionary"""
        # Parse date - format: "Mon, 3-16-2026, 11:00 am"
        date_str = row.get('Publish time (day, date, time)', '')
        # Remove day of week and clean up
        date_part = re.sub(r'^[A-Za-z]+, ', '', date_str)
        publish_datetime = datetime.strptime(date_part, '%m-%d-%Y, %I:%M %p')
        
        return cls(
            zotero_key=row.get('Zotero key', ''),
            publish_datetime=publish_datetime,
            video_source=row.get('Video source', ''),
            caption=row.get('Caption', '')
        )