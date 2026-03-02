# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import re

@dataclass
class Book:
    """Represents a book from Zotero - only fields needed for processing"""
    zotero_key: str
    note_html: str  # Contains the excerpt with <!--post--> marker
    date_modified: datetime  # To find last modified items
    
    @classmethod
    def from_csv_row(cls, row: Dict[str, Any]) -> 'Book':
        """Create a Book instance from a CSV row dictionary"""
        return cls(
            zotero_key=row.get('Id', ''),
            note_html=row.get('Notes', ''),
            date_modified=datetime.strptime(
                row.get('Date Modified', ''), 
                '%Y-%m-%d %H:%M:%S'
            )
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
    # No caption fields - they come from the Jekyll project
    
    def to_csv_row(self) -> Dict[str, str]:
        """Convert to dictionary for CSV writing"""
        return {
            'Zotero key': self.zotero_key,
            'Publish time (day, date, time)': self.publish_datetime.strftime('%a, %-m-%-d-%Y, %I:%M %p'),
            'Video source': self.video_source,
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
            video_source=row.get('Video source', '')
        )