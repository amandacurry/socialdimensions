import random
import requests
from langdetect import detect
import re
import csv
import time


INNERTUBE_URL = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "X-Youtube-Client-Name": "1",
    "X-Youtube-Client-Version": "2.20201021.03.00"
}

YOUTUBE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789_'
API_KEY = 'AIzaSyBjenBURlJbaJvME5JwjU3chM9HvLRwiCo'
API_KEY = 'AIzaSyAoI-AhItGmtsu_d9T3POCjEzj2k7vjHMw'
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

def clean_title(title):
    # Removes hashtags (words starting with #), including multi-word ones
    return re.sub(r'#\w+', '', title).strip()

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False  # fallback if text is too short or ambiguous
    
def random_prefix(length=4):
    return ''.join(random.choices(YOUTUBE_ALPHABET, k=length))

def search_prefix(prefix, max_results=50):
    query = f'"watch?v={prefix}"'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return 'error'

    items = response.json().get('items', [])
    results = []
    for item in items:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        description = item['snippet']['description']
        
        if video_id.lower().startswith(f"{prefix}-") and is_english(description):
            print(video_title)
            results.append(video_id)
    return results


def save_video_ids_to_csv(video_ids, filename="video_ids.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow(["video_id"])  # header
        for vid in video_ids:
            writer.writerow([vid])
    print(f"✅ Saved {len(video_ids)} video IDs to {filename}")

def main():
    found_videos = []
    unmatched_ids = []

    seen_video_ids = set()

    while len(found_videos) < 5000:  # Adjust the limit as needed
        prefix = random_prefix(4)
        print(f"🔎 Searching with prefix: {prefix}")
        try:
            results = search_prefix(prefix)
            if results == 'error':
                print("Error occurred during search, skipping this prefix.")
                save_video_ids_to_csv(found_videos)
                break
            print(f"Found {len(results)} videos with prefix '{prefix}'")

            for video_id in results:
                found_videos.append(video_id)
                print(len(found_videos))
                seen_video_ids.add(video_id)

        except Exception as e:
            save_video_ids_to_csv(found_videos)
            print("Error during search:", e)

    print("Found videos:")
    for video in found_videos:
        print(video)
    save_video_ids_to_csv(found_videos)
    time.sleep(0.2)

if __name__ == "__main__":
    main()
