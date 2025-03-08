import yt_dlp
import threading
import csv
import json
import os
import logging
from tqdm import tqdm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from colorama import init, Fore
from tabulate import tabulate
import argparse

# Initialize colorama
init(autoreset=True)

# 🔥 Beautiful ASCII Banner
BANNER = f"""
{Fore.CYAN}
 ██████  ██    ██ ███████ ██████   ██████  
 ██   ██ ██    ██ ██      ██   ██ ██    ██ 
 ██████  ██    ██ █████   ██████  ██    ██ 
 ██      ██    ██ ██      ██   ██ ██    ██ 
 ██       ██████  ███████ ██   ██  ██████  
   {Fore.YELLOW}YouTube Video Metadata Extractor - Created by Mr. Sami {Fore.RESET}
"""

# Set up logging
log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(Fore.GREEN + f"📁 Created log folder: {log_folder}")

log_file = os.path.join(log_folder, "yt_metadata_extractor.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file,
    filemode="w",  # Overwrite the log file each time
)
logger = logging.getLogger(__name__)

# Log script start
logger.info("Script started")
print(Fore.GREEN + f"📝 Logs will be saved to: {log_file}")

def print_banner():
    print(BANNER)

def fetch_video_details(video_url, results, progress_bar):
    try:
        logger.info(f"Fetching details for: {video_url}")
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_details = {
                'Title': info_dict.get('title', 'N/A'),
                'Uploader': info_dict.get('uploader', 'N/A'),
                'Channel URL': info_dict.get('uploader_url', 'N/A'),
                'Upload Date': info_dict.get('upload_date', 'N/A'),
                'Views': f"{info_dict.get('view_count', 0):,}",
                'Likes': f"{info_dict.get('like_count', 0):,}",
                'Dislikes': f"{info_dict.get('dislike_count', 'N/A'):,}" if info_dict.get('dislike_count') else 'N/A',
                'Duration': f"{round(info_dict.get('duration', 0) / 60, 2)} min",
                'Resolution': info_dict.get('format', 'N/A'),
                'FPS': info_dict.get('fps', 'N/A'),
                'Age Restriction': "Yes" if info_dict.get('age_limit', 0) > 0 else "No",
                'Thumbnail': info_dict.get('thumbnail', 'N/A'),
                'Video URL': info_dict.get('webpage_url', 'N/A'),
                'Tags': ', '.join(info_dict.get('tags', [])) if info_dict.get('tags') else 'No Tags',
                'Categories': ', '.join(info_dict.get('categories', [])) if info_dict.get('categories') else 'No Categories',
                'Description': info_dict.get('description', 'No Description')[:300] + "...",
                'Language': info_dict.get('language', 'N/A'),
                'Subtitles': 'Yes' if info_dict.get('subtitles') else 'No',
                'Formats': [f"{f['format']} ({f['ext']})" for f in info_dict.get('formats', [])],
            }
            results.append(video_details)
            logger.info(f"Successfully fetched details for: {video_url}")
    except Exception as e:
        logger.error(f"Error fetching details for {video_url}: {e}")
    finally:
        progress_bar.update(1)

def process_videos(video_urls):
    results = []
    threads = []
    progress_bar = tqdm(total=len(video_urls), desc="Extracting Metadata", unit="video")

    for url in video_urls:
        thread = threading.Thread(target=fetch_video_details, args=(url, results, progress_bar))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    progress_bar.close()
    print(Fore.GREEN + "\n✅ Metadata Extraction Completed!\n")
    logger.info("Metadata extraction completed")
    return results

def display_video_details(video_details):
    table_data = [[Fore.YELLOW + key + Fore.RESET, Fore.GREEN + str(value) + Fore.RESET] for key, value in video_details.items()]
    print(tabulate(table_data, headers=[Fore.MAGENTA + "Field", Fore.MAGENTA + "Value"], tablefmt="fancy_grid"))

def save_to_json(results, video_id, output_folder):
    filename = os.path.join(output_folder, f"{video_id}.json")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)
    print(Fore.GREEN + f"📂 JSON report saved as '{filename}'")
    logger.info(f"JSON report saved: {filename}")

def save_to_csv(results, video_id, output_folder):
    filename = os.path.join(output_folder, f"{video_id}.csv")
    with open(filename, "w", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(Fore.GREEN + f"📂 CSV report saved as '{filename}'")
    logger.info(f"CSV report saved: {filename}")

def save_to_pdf(results, video_id, output_folder):
    filename = os.path.join(output_folder, f"{video_id}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 40, "YouTube Video Metadata Report")

    y_position = height - 80
    c.setFont("Helvetica", 12)

    for video in results:
        c.drawString(50, y_position, "-" * 80)  # Separator
        y_position -= 20
        for key, value in video.items():
            lines = simpleSplit(f"{key}: {value}", "Helvetica", 12, 500)
            for line in lines:
                c.drawString(50, y_position, line)
                y_position -= 20
                if y_position < 50:
                    c.showPage()
                    y_position = height - 40
                    c.setFont("Helvetica", 12)

    c.save()
    print(Fore.GREEN + f"📂 PDF report saved as '{filename}'")
    logger.info(f"PDF report saved: {filename}")

def save_to_html(results, video_id, output_folder):
    filename = os.path.join(output_folder, f"{video_id}.html")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Video Metadata Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .video-details {{ margin-bottom: 20px; }}
            .video-details h2 {{ color: #555; }}
            .video-details img {{ max-width: 100%; height: auto; }}
            .video-details table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            .video-details th, .video-details td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            .video-details th {{ background-color: #f4f4f4; }}
            .collapsible {{ cursor: pointer; }}
            .content {{ display: none; padding: 10px; background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>YouTube Video Metadata Report</h1>
    """
    
    for video in results:
        html_content += f"""
        <div class="video-details">
            <h2>{video['Title']}</h2>
            <img src="{video['Thumbnail']}" alt="Thumbnail">
            <table>
                <thead>
                    <tr>
                        <th>Field</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
        """
        for key, value in video.items():
            if key == "Thumbnail":
                continue
            html_content += f"""
                    <tr>
                        <td><strong>{key}</strong></td>
                        <td>{value}</td>
                    </tr>
            """
        html_content += """
                </tbody>
            </table>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(Fore.GREEN + f"📂 HTML report saved as '{filename}'")
    logger.info(f"HTML report saved: {filename}")

def main():
    print_banner()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="YouTube Video Metadata Extractor")
    parser.add_argument("urls", nargs="*", help="YouTube video URLs (space-separated)")
    parser.add_argument("--output", default="report", help="Output folder for reports")
    args = parser.parse_args()

    # Create output folder if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        logger.info(f"Created output folder: {args.output}")

    # Get video URLs
    if args.urls:
        video_urls = args.urls
    else:
        choice = input(Fore.YELLOW + "1️⃣ Single Video\n2️⃣ Bulk Video Input (Comma Separated)\nChoose option (1/2): ")
        if choice == "1":
            video_url = input(Fore.GREEN + "📄 Enter Video URL: ")
            video_urls = [video_url]
        elif choice == "2":
            video_urls = input(Fore.GREEN + "📄 Enter Video URLs (comma separated): ").split(',')
            video_urls = [url.strip() for url in video_urls]
        else:
            print(Fore.RED + "❌ Invalid option! Exiting...")
            logger.error("Invalid option selected")
            return

    # Process videos
    results = process_videos(video_urls)

    # Display all results
    for video in results:
        display_video_details(video)

    # Save to report
    print(Fore.YELLOW + "\n📜 Choose report format:")
    print("1️⃣ JSON")
    print("2️⃣ CSV")
    print("3️⃣ PDF")
    print("4️⃣ HTML")
    print("5️⃣ All Formats")
    
    report_choice = input(Fore.GREEN + "Enter option (1/2/3/4/5): ")

    for video in results:
        video_id = video['Video URL'].split('=')[-1]  # Extract video ID from URL
        if report_choice == "1":
            save_to_json([video], video_id, args.output)
        elif report_choice == "2":
            save_to_csv([video], video_id, args.output)
        elif report_choice == "3":
            save_to_pdf([video], video_id, args.output)
        elif report_choice == "4":
            save_to_html([video], video_id, args.output)
        elif report_choice == "5":
            save_to_json([video], video_id, args.output)
            save_to_csv([video], video_id, args.output)
            save_to_pdf([video], video_id, args.output)
            save_to_html([video], video_id, args.output)
        else:
            print(Fore.RED + "❌ Invalid choice, no report generated.")
            logger.warning("Invalid report format selected")

if __name__ == "__main__":
    main()