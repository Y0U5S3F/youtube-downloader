import os
import yt_dlp

def get_video_links_from_playlist(playlist_url):
    """
    Extracts and returns a list of full video URLs from a YouTube playlist.
    """
    video_links = []
    ydl_opts = {
        'extract_flat': True,  # Only extract video URLs without downloading them
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            for entry in result['entries']:
                # If the URL is only a video ID, prepend the full URL
                video_id = entry.get('url')
                if not video_id.startswith("http"):
                    video_url = "https://www.youtube.com/watch?v=" + video_id
                else:
                    video_url = video_id
                video_links.append(video_url)
    return video_links

def download_video_as_mp3(video_url, output_folder="downloads"):
    """
    Downloads the audio from a YouTube video and converts it to MP3.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Using a custom User-Agent to help bypass potential 403 errors
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        },
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    
    # Extract video links from the playlist
    video_links = get_video_links_from_playlist(playlist_url)
    print("\nFound the following video links:")
    for idx, link in enumerate(video_links, start=1):
        print(f"{idx}: {link}")

    # Ask if the user wants to download the videos as MP3
    download_choice = input("\nDo you want to download these videos as mp3? (yes/no): ").strip().lower()
    if download_choice in ('yes', 'y'):
        for link in video_links:
            print(f"\nDownloading {link} as mp3...")
            download_video_as_mp3(link)
        print("\nDownload complete.")
    else:
        print("\nDownload skipped.")
