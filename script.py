import os
import yt_dlp

def get_video_links_from_playlist(playlist_url):
    """
    Given a YouTube playlist URL, extract and return a list of full video URLs.
    """
    video_links = []
    ydl_opts = {
        'extract_flat': True,  # Only extract video URLs without downloading them
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        # Ensure that we have playlist entries
        if 'entries' in result:
            for entry in result['entries']:
                # entry['url'] may be just the video ID in flat mode; prepend the full URL if needed.
                video_id = entry.get('url')
                if not video_id.startswith("http"):
                    video_url = "https://www.youtube.com/watch?v=" + video_id
                else:
                    video_url = video_id
                video_links.append(video_url)
    return video_links

def download_video_as_mp3(video_url, output_folder="downloads"):
    """
    Downloads the audio from a YouTube video as an MP3 file.
    """
    # Create the output folder if it does not exist
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
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    # Ask for the playlist URL
    playlist_url = input("Enter the YouTube playlist URL: ")
    video_links = get_video_links_from_playlist(playlist_url)

    print("\nFound the following video links:")
    for idx, link in enumerate(video_links, start=1):
        print(f"{idx}: {link}")

    # Optionally download the videos as mp3 files
    download_choice = input("\nDo you want to download these videos as mp3? (yes/no): ").strip().lower()
    if download_choice in ('yes', 'y'):
        for link in video_links:
            print(f"\nDownloading {link} as mp3...")
            download_video_as_mp3(link)
        print("\nDownload complete.")
    else:
        print("\nDownload skipped.")