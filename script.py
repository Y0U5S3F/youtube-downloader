import os
import time
import yt_dlp

def get_video_links_from_playlist(playlist_url):
    """
    Extracts and returns a list of full video URLs from a YouTube playlist.
    """
    video_links = []
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,  # suppress extra output
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                for entry in result['entries']:
                    video_id = entry.get('url')
                    if not video_id.startswith("http"):
                        video_url = "https://www.youtube.com/watch?v=" + video_id
                    else:
                        video_url = video_id
                    video_links.append(video_url)
    except Exception as e:
        print(f"Error extracting playlist info: {e}")
    return video_links

def download_video_as_mp3(video_url, output_folder="downloads", wait_time=60):
    """
    Downloads a video as an MP3. If an error occurs (e.g., due to a temporary IP block),
    the script will wait for wait_time seconds before retrying. If the error indicates
    that the video is permanently unavailable (such as when the account is terminated),
    the video is skipped.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    attempts = 0
    while True:
        attempts += 1
        print(f"\nAttempt {attempts} for: {video_url}")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/115.0.0.0 Safari/537.36')
            },
            'quiet': False,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print(f"Successfully downloaded: {video_url}")
            break  # Download succeeded; exit the loop.
        except Exception as e:
            error_str = str(e)
            # Check if the error indicates the video is permanently unavailable.
            if "no longer available" in error_str or "Video unavailable" in error_str:
                print(f"Skipping video {video_url} because it is unavailable: {error_str}")
                break
            else:
                print(f"Error downloading {video_url}: {error_str}")
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)

if __name__ == "__main__":
    try:
        playlist_url = input("Enter the YouTube playlist URL: ").strip()
        video_links = get_video_links_from_playlist(playlist_url)
        
        if not video_links:
            print("No video links found. Exiting.")
        else:
            print("\nFound the following video links:")
            for idx, link in enumerate(video_links, start=1):
                print(f"{idx}: {link}")
            
            download_choice = input("\nDo you want to download these videos as MP3? (yes/no): ").strip().lower()
            if download_choice in ('yes', 'y'):
                for link in video_links:
                    print(f"\nDownloading {link} as MP3...")
                    download_video_as_mp3(link)
                print("\nDownload complete.")
            else:
                print("\nDownload skipped.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
