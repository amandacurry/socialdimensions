import httpx
import random
import string
import csv
from typing import List
from collections import defaultdict
import time

INNERTUBE_URL = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "X-Youtube-Client-Name": "1",
    "X-Youtube-Client-Version": "2.20201021.03.00"
}
MAX_RESULTS = 5

ID_CHARS = string.ascii_letters + string.digits + "-_"
ID_LAST_CHAR_OPTIONS = list("AEIMQUYcgkosw048")

def generate_random_ids(n: int = 32) -> List[str]:
    ids = []
    for _ in range(n):
        first_10 = ''.join(random.choices(ID_CHARS, k=10)).lower()
        last_char = random.choice(ID_LAST_CHAR_OPTIONS)
        ids.append(first_10 + last_char)
    return ids

def search_youtube_batch(query: str):
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20201021.03.00"
            }
        },
        "query": query
    }
    response = httpx.post(INNERTUBE_URL, headers=HEADERS, json=payload)
    print(payload)
    return response.json()

def extract_video_results(json_data):
    results = []
    try:
        sections = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        for section in sections:
            items = section.get('itemSectionRenderer', {}).get('contents', [])
            for item in items:
                if 'videoRenderer' in item:
                    video = item['videoRenderer']
                    video_id = video['videoId']
                    title = video['title']['runs'][0]['text']
                    description = video.get('detailedMetadataSnippets', [{}])[0].get('snippetText', {}).get('runs', [{}])[0].get('text', '')
                    results.append({
                        "video_id": video_id,
                        "title": title,
                        "description": description,
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })
    except Exception as e:
        print("Failed to parse results:", e)
    return results

def match_identifiers_to_results(identifiers: List[str], results: List[dict]):
    id_matches = defaultdict(list)
    for result in results:
        content = result['video_id'].lower()
        print(result)
        for ident in identifiers:
            print(f"Checking if {ident.lower()} matches {content}")
            if ident.lower() == content:
                id_matches[ident].append(result)
    return id_matches

YOUTUBE_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
def random_prefix(length=4):
    return ''.join(random.choices(YOUTUBE_ALPHABET, k=length))

def main():
    found_videos = []
    unmatched_ids = []

    seen_video_ids = set()

    while len(found_videos) < MAX_RESULTS:
        time.sleep(1) 
        ids = generate_random_ids(32)
        ids = [random_prefix()]
        #or_query = " OR ".join(ids)
        print(f"🔎 Searching batch: {ids}")
        try:
            response = search_youtube_batch(ids)
            results = extract_video_results(response)
            print(len(results))
            matches = match_identifiers_to_results(ids, results)

            for ident, vids in matches.items():
                for video in vids:
                    if video["video_id"] not in seen_video_ids and len(found_videos) < MAX_RESULTS:
                        found_videos.append({
                            "matched_id": ident,
                            "video_id": video["video_id"],
                            "title": video["title"],
                            "description": video["description"],
                            "url": video["url"]
                        })
                        seen_video_ids.add(video["video_id"])

            unmatched_ids.extend([i for i in ids if i not in matches])

        except Exception as e:
            print("Error during search:", e)
            unmatched_ids.extend(ids)  # assume whole batch failed

    with open("found_videos.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["matched_id", "video_id", "title", "description", "url"])
        writer.writeheader()
        for row in found_videos:
            writer.writerow(row)

    with open("unmatched_ids.txt", "w") as f:
        for uid in unmatched_ids:
            f.write(uid + "\n")

    print(f"\nFound {len(found_videos)} videos. Saved to found_videos.csv")
    print(f" {len(unmatched_ids)} unmatched IDs written to unmatched_ids.txt")

if __name__ == "__main__":
    main()
