import requests
import os
import random
from config import PEXELS_API_KEY, ASSETS_DIR

class SourcingEngine:
    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key}

    def fetch_vertical_video(self, query, min_duration=10, max_duration=60):
        """
        Searches Pexels for high-quality vertical 9:16 videos based on a mood query.
        """
        if self.api_key == "YOUR_PEXELS_API_KEY":
            print("Warning: PEXELS_API_KEY not set. Sourcing will fail.")
            return None

        params = {
            "query": query,
            "orientation": "portrait", # Ensures 9:16 vertical
            "per_page": 5,
            "min_width": 720
        }

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = data.get("videos", [])
            if not videos:
                print(f"No videos found for query: {query}")
                return None

            # Pick a random video from the top results for variety
            video_data = random.choice(videos)
            
            # Find the best quality HD link
            video_files = video_data.get("video_files", [])
            best_link = None
            for f in video_files:
                if f.get("width") == 720 or f.get("width") == 1080:
                    best_link = f.get("link")
                    break
            
            if not best_link and video_files:
                best_link = video_files[0].get("link")

            if best_link:
                video_id = video_data.get("id")
                save_path = os.path.join(ASSETS_DIR, f"video_{video_id}.mp4")
                
                # Download the video
                print(f"Downloading video: {best_link}...")
                v_res = requests.get(best_link, stream=True)
                with open(save_path, "wb") as f:
                    for chunk in v_res.iter_content(chunk_size=1024):
                        f.write(chunk)
                
                return save_path

        except Exception as e:
            print(f"Error fetching video from Pexels: {e}")
            return None

if __name__ == "__main__":
    # Test sourcing
    engine = SourcingEngine()
    print("Testing Moody Wellness Search...")
    path = engine.fetch_vertical_video("Moody Wellness Aesthetic")
    if path:
        print(f"Success! Video saved to: {path}")
