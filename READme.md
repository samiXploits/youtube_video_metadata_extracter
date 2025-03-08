# YouTube Video Metadata Extractor

![YouTube Video Metadata Extractor](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

A powerful Python script that extracts metadata from YouTube videos using `yt_dlp`. This tool fetches details like title, uploader, views, likes, duration, resolution, and more. The extracted metadata can be saved in JSON, CSV, PDF, or HTML formats.

## Features
- 🔍 Extract YouTube video metadata (title, views, likes, uploader, etc.)
- 📂 Export data to JSON, CSV, PDF, or HTML formats
- 🚀 Multi-threading for faster processing of multiple video URLs
- 🎨 Beautiful CLI interface with colorized output
- 📝 Log system to track script activities

## Installation

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Basic Command
```bash
python video_search_engine.py "https://www.youtube.com/watch?v=example_id"
```

### Multiple Video URLs
```bash
python video_search_engine.py "https://youtu.be/video1" "https://youtu.be/video2"
```

### Output Folder
Specify an output folder for reports:
```bash
python video_search_engine.py "https://youtu.be/video1" --output my_reports
```

### Interactive Mode
Run the script without arguments to enter interactive mode and manually input video URLs.

## Available Report Formats
When the script completes execution, it prompts you to choose a report format:
- JSON (`.json`)
- CSV (`.csv`)
- PDF (`.pdf`)
- HTML (`.html`)
- All Formats (saves in all the above formats)

## Example Output
```
🎬 Title: My Sample Video
📢 Uploader: John Doe
👁️ Views: 1,200,000
👍 Likes: 45,000
📅 Upload Date: 2023-02-20
📂 Report saved as: report/video1.json
```

## Logging
Logs are stored in the `log/yt_metadata_extractor.log` file.

## Dependencies
- `yt_dlp`
- `tqdm`
- `colorama`
- `reportlab`
- `tabulate`
- `argparse`

## License
This project is licensed under the MIT License.

## Author
Created by Mr. Sami 🚀

