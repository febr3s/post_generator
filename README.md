# Social Media Post Generator from Zotero

This project automates the creation of social media posts (Instagram, Twitter) from a curated set of books in Zotero. It generates short video clips from book excerpts, schedules posts over a 91‑day period, and sends them via Telegram. The system is designed for a curator who selects 39 books each cycle, ensuring each excerpt fits the video constraints.

---

## Features

- Reads a Zotero CSV export and extracts relevant book data.
- Uses the **Abstract Note** as the source for the excerpt (plain text).
- Generates a video snippet from the excerpt using ImageMagick and ffmpeg.
- Automatically assigns posting dates (Mondays, Fridays, Saturdays at 11:00 AM) over a 91‑day window.
- Stores posts (key, date, video path, caption) in a local CSV.
- Provides a batch script to create all posts after curation.
- Sends scheduled posts via a Telegram bot (video + caption).
- Optional weekly status report.

---

## Prerequisites

- Python 3.8+
- ImageMagick (`convert`) and ffmpeg installed and in PATH.
- A Telegram bot token (from [@BotFather](https://t.me/botfather)) and your personal chat ID (from [@userinfobot](https://t.me/userinfobot)).

### Required Python packages

```bash
pip install requests python-dotenv
```

(No additional packages if you avoid `.env`.)

---

## Installation

1. Clone or download this repository.
2. Install dependencies.
3. Place your Zotero CSV export at the location defined in `config.py` (default: `../../morel-no-code-generator/assets/data/books_zotero.csv`).
4. Create a `.env` file (optional) with your Telegram credentials, or set them directly in `config.py`.

---

## Configuration

All settings are in `config.py`. Important variables:

| Variable | Description |
|----------|-------------|
| `ZOTERO_CSV_PATH` | Path to the Zotero export CSV. |
| `POSTS_DB_PATH`   | Path to the output CSV where posts are stored. |
| `OUTPUT_DIR`      | Directory where video folders will be created. |
| `START_DATE`      | First posting day (e.g., `datetime(2026, 3, 16)`). |
| `END_DATE`        | Automatically set to `START_DATE + 91 days`. |
| `POSTING_DAYS`    | Weekdays for posting: `[0,4,5]` = Monday, Friday, Saturday. |
| `POSTING_HOUR`    | Hour of day (24‑hour format). |
| `POSTING_MINUTE`  | Minute of day. |
| `VIDEO_SETTINGS`  | Parameters for video generation (font, colors, etc.). |
| `TELEGRAM_BOT_TOKEN` | Your bot token (string). Set to `None` to disable. |
| `TELEGRAM_CHAT_ID`   | Your personal or group chat ID (string or int). |

If you use a `.env` file, install `python-dotenv` and add at the top of `config.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Data Preparation

Your Zotero CSV export **must** include the following columns (exact names):

- `Key` – Zotero item key (used as unique identifier).
- `Abstract Note` – the excerpt text (plain, without HTML). The excerpt must be **281–349 characters** to produce exactly five video fragments. (Shorter text will cause video generation to fail.)
- `Date Modified` – used to sort books by recency.
- `Title`, `Author`, `Year`, `Publisher`, `Blurb` (true/false), `Edition`, `Library` – used for caption generation.  
  - `Blurb` should be `TRUE` or `FALSE`.
  - `Edition` should be an integer (1, 2, …).

Only books with a non‑empty `Abstract Note` are considered curated and eligible for posting.

---

## Workflow

### 1. Curate Books in Zotero
- Add an abstract (plain text) of the desired length (281–349 characters) to each book.
- Mark books you want to include in the next batch by having a non‑empty `Abstract Note`.

### 2. Export CSV from Zotero
- Export your library as a CSV file with all relevant fields. Place it at the path set in `config.py`.

### 3. Run Batch Generator
```bash
python batch_generator.py
```
This script:
- Loads all books with abstracts to the scheduler.
- Determines how many posting slots are still free.
- Selects up to 29 books (or fewer if fewer slots remain), sorted by most recent modification.
- For each book, generates a video, creates a caption, and saves the post to `posts.csv` with the next free date.

### 4. Set Up Cron Jobs

Two cron jobs are required: one for daily posting and one for weekly status updates.

**Daily Post** – Runs a few minutes after the scheduled posting time (e.g., 11:05 AM if you post at 11:00).  
Edit your crontab with `crontab -e` and add:

```cron
# Send scheduled post (adjust minute and hour to match POSTING_HOUR+5)
5 11 * * 1,4,5 cd /path/to/project && /usr/bin/python3 daily_post.py >> /path/to/project/logs/daily.log 2>&1

### 5. (Optional) Manual Testing
Use `simple_test.py` (provided in the repository) to test the whole pipeline on a single book:
```bash
python simple_test.py
```
This will pick the most recently modified book, generate its video, create a post, and display the results.

---

## Project Structure

```
post_generator/
├── config.py              # Configuration
├── models.py              # Book and Post dataclasses
├── data_loader.py         # CSV reading/writing
├── selector.py            # Filter and sort books
├── scheduler.py           # Generate posting dates
├── video_generator.py     # Call ImageMagick/ffmpeg to produce video
├── post_creator.py        # Orchestrate creation of one post
├── batch_generator.py     # Main script after curation
├── notifier.py            # Telegram messaging
├── daily_post.py          # Cron job to send today's post
├── weekly_status.py       # (Not yet implemented) status report
├── simple_test.py         # Integration test on one book
├── posts.csv              # Generated posts database
└── video_output/          # Subfolders with videos
```

---

## Testing

- `simple_test.py` verifies that a single book can be processed end‑to‑end.
- `simple_test_telegram.py` sends a test message using your telegram bot.
- Unit tests (optional) are in separate files (e.g., `test_data_loader.py`) but not required for normal operation.

---

## Troubleshooting

### Video generation fails
- Ensure the excerpt is **281–349 characters**. If shorter, the `fold` command will produce fewer than five lines, and the ffmpeg command will fail (missing images).
- Check that ImageMagick (`convert`) and ffmpeg are installed and in PATH.

### Telegram not sending
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are correct.
- The bot must be allowed to send messages to the chat (start a conversation with it first).
- If you use a group, add the bot to the group and get the group chat ID (negative number).

### Posts not found in `posts.csv`
- Ensure the CSV headers match exactly: `Zotero key`, `Publish time (day, date, time)`, `Video source`, `Caption`.
- The `Post.from_csv_row` method expects the same format.

### Date parsing errors
- The `publish_datetime` format is `%a, %-m-%-d-%Y, %I:%M %p` (e.g., `Mon, 3-16-2026, 11:00 am`). Do not modify this.

---

## License

[Your chosen license, e.g., MIT]

---

## Acknowledgements

Built with Python, ImageMagick, ffmpeg, DeepSeek and the Telegram Bot API.