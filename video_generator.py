# video_generator.py
import os
import subprocess
from config import OUTPUT_DIR

def generate_video(excerpt: str, zotero_key: str) -> str:
    """
    Generate video using the exact commands from the spec.

    Args:
        excerpt: text to convert (must produce at least 5 lines when folded)
        zotero_key: Zotero ID for folder naming

    Returns:
        relative path to output.mp4 (e.g., 'N9IPZBJU/output.mp4')

    Raises:
        subprocess.CalledProcessError if a command fails.
    """
    # Create book folder
    book_folder = os.path.join(OUTPUT_DIR, zotero_key)
    os.makedirs(book_folder, exist_ok=True)

    # Escape double quotes inside excerpt to avoid breaking the shell command
    excerpt_escaped = excerpt.replace('"', '\\"')

    # 1. Generate images (exactly as in spec)
    cmd_images = (
        f'echo "{excerpt_escaped}" | fold -sw70 | while read line; do '
        'n=$((n+1)); '
        'convert -size 1080x1080 -background "#C6C8C4" -fill "#2a3425" '
        '-font "AvantGarde-Book" -weight Black -pointsize 115 -gravity west '
        '-size 980x1080 caption:"$(echo "$line" | tr \'[:lower:]\' \'[:upper:]\')" '
        '-gravity center -extent 1080x1080 "fragment_$n.png"; '
        'echo "Generated fragment_$n.png"; done'
    )
    subprocess.run(cmd_images, shell=True, cwd=book_folder, check=True)

    # 2. Generate video (exactly as in spec)
    cmd_video = (
        'ffmpeg -loop 1 -t 3 -i fragment_1.png '
        '-loop 1 -t 3 -i fragment_2.png '
        '-loop 1 -t 3 -i fragment_3.png '
        '-loop 1 -t 3 -i fragment_4.png '
        '-loop 1 -t 3 -i fragment_5.png '
        '-filter_complex '
        '"[0][1]xfade=transition=fade:duration=1:offset=2[ab];'
        '[ab][2]xfade=transition=fade:duration=1:offset=4[abc];'
        '[abc][3]xfade=transition=fade:duration=1:offset=6[abcd];'
        '[abcd][4]xfade=transition=fade:duration=1:offset=8" '
        '-c:v libx264 -r 30 -pix_fmt yuv420p output.mp4'
    )
    subprocess.run(cmd_video, shell=True, cwd=book_folder, check=True)

    # Return relative path
    return os.path.join(zotero_key, 'output.mp4')