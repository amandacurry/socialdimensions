import csv
import requests
import pandas as pd
from langdetect import detect
from time import sleep

#API_KEY = 'AIzaSyBtgLmVigkEZ5XqTLwjgIz4fyUvEGFSKcc'#'AIzaSyAoI-AhItGmtsu_d9T3POCjEzj2k7vjHMw'# 'AIzaSyBjenBURlJbaJvME5JwjU3chM9HvLRwiCo'    # 'AIzaSyBtgLmVigkEZ5XqTLwjgIz4fyUvEGFSKcc' # Replace with your actual API key          
api_keys = ['AIzaSyBtgLmVigkEZ5XqTLwjgIz4fyUvEGFSKcc', 'AIzaSyAoI-AhItGmtsu_d9T3POCjEzj2k7vjHMw', 'AIzaSyBjenBURlJbaJvME5JwjU3chM9HvLRwiCo']
COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'
CATEGORY_MAP = {}  # We'll fill this once per session
API_KEY = api_keys[0]  # Start with the first API key

def is_english(text):
    try:
        return detect(text.strip()) == 'en'
    except:
        return False

def word_count(text):
    return len(text.strip().split())

def get_video_metadata(video_id):
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': API_KEY
    }
    resp = requests.get(VIDEO_URL, params=params)
    if resp.status_code != 200:
        print(f"⚠️ Metadata fetch failed for {video_id}")
        return None

    items = resp.json().get('items', [])
    if not items:
        return None

    snippet = items[0]['snippet']
    return {
        'video_title': snippet.get('title', ''),
        'category_id': snippet.get('categoryId', ''),
        'channel_name': snippet.get('channelTitle', '')
    }

def get_comment_reply_pairs(video_id, max_pairs=20):
    pairs = []
    next_page_token = None

    while len(pairs) < max_pairs:
        params = {
            'part': 'snippet,replies',
            'videoId': video_id,
            'maxResults': 100,
            'textFormat': 'plainText',
            'key': API_KEY
        }
        if next_page_token:
            params['pageToken'] = next_page_token

        resp = requests.get(COMMENT_URL, params=params)
        if resp.status_code != 200:
            print(f"❌ Comment fetch error for {video_id}: {resp.status_code}")
            error_message = resp.json().get('error', {}).get('message', 'Unknown error')
            print(f"Error message: {error_message}")
            break

        data = resp.json()
        for item in data.get('items', []):
            try:
                top = item['snippet']['topLevelComment']['snippet']
                top_text = top['textDisplay']
                top_date = top['publishedAt']

                if not (is_english(top_text) and word_count(top_text) > 10):
                    continue

                replies = item.get('replies', {}).get('comments', [])
                if not replies:
                    continue

                first_reply = replies[0]['snippet']
                reply_text = first_reply['textDisplay']
                reply_date = first_reply['publishedAt']

                if is_english(reply_text) and word_count(reply_text) > 10:
                    pairs.append({
                        'video_id': video_id,
                        'comment': top_text,
                        'reply': reply_text,
                        'comment_date': top_date,
                        'reply_date': reply_date
                    })

                if len(pairs) >= max_pairs:
                    break
            except Exception as e:
                continue

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return pairs

def enrich_with_video_data(pairs, metadata):
    for pair in pairs:
        pair.update({
            'video_title': metadata['video_title'],
            'category_id': metadata['category_id'],
            'channel_name': metadata['channel_name']
        })
    return pairs

def read_video_ids(file_path):
    df = pd.read_csv(file_path)
    return df.iloc[:, 0].dropna().unique().tolist()

def save_to_csv(all_data, output_path):
    df = pd.DataFrame(all_data)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved {len(df)} comment–reply pairs to {output_path}")

def main(input_csv, output_csv):
    video_ids = read_video_ids(input_csv)
    all_pairs = []
    i = 0
    API_KEY = api_keys[i]  # Use the first API key initially

    for vid in video_ids:
        print(f"\n🔍 Processing {vid}")
        meta = get_video_metadata(vid)
        if not meta:
            print("⚠️ Skipping video due to missing metadata")
            if i < len(api_keys) - 1:
                i += 1
                API_KEY = api_keys[i]
                print(f"🔑 Switching to API key {i + 1}")
                print("retying...")
                meta = get_video_metadata(vid)
                if not meta:
                    print("❌ Failed to fetch metadata after switching API keys, stopping.")
                    save_to_csv(all_pairs, output_csv)
                    continue
            else:
                print("❌ No more API keys available, stopping.") 
                break

        pairs = get_comment_reply_pairs(vid, max_pairs=100)
        if pairs:
            enriched = enrich_with_video_data(pairs, meta)
            all_pairs.extend(enriched)
        else:
            print("⚠️ No valid comment–reply pairs found")

        sleep(0.2)  # To be nice to the API

    save_to_csv(all_pairs, output_csv)

# Example usage
if __name__ == "__main__":
    main("prefix_video_ids_pt2.csv", "comment_reply_pairs_pt3.csv")
