import requests
import os
import random
from config import PEXELS_API_KEY, ASSETS_DIR

class SourcingEngine:
    """
    Universal Sourcing Engine for General Hendricks.
    Finds cinematic vertical footage for ANY niche.
    """
    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key}

    def fetch_vertical_video(self, keywords, niche="wellness"):
        """
        Searches Pexels for high-quality vertical 9:16 videos.
        Args:
            keywords: List of mood keywords from researcher.
            niche: The broad category to ensure relevance.
        """
        if self.api_key == "YOUR_PEXELS_API_KEY":
            print("Warning: PEXELS_API_KEY not set. Sourcing will fail.")
            return None

        # Combine niche with keywords for better results
        query = f"{niche} {random.choice(keywords)}"
        print(f"Sourcing intelligence for: {query}")

        params = {
            "query": query,
            "orientation": "portrait",
            "per_page": 5,
            "min_width": 720
        }

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = data.get("videos", [])
            if not videos:
                # Fallback to broader search
                print(f"Refining search for: {niche}...")
                params["query"] = niche
                response = requests.get(self.base_url, headers=self.headers, params=params)
                data = response.json()
                videos = data.get("videos", [])

            if not videos:
                return None

            video_data = random.choice(videos[:3])
            video_files = video_data.get("video_files", [])
            
            # Find HD link
            best_link = next((f.get("link") for f in video_files if f.get("width") >= 720), None)
            if not best_link and video_files:
                best_link = video_files[0].get("link")

            if best_link:
                video_id = video_data.get("id")
                save_path = os.path.join(ASSETS_DIR, f"video_{video_id}.mp4")
                
                v_res = requests.get(best_link, stream=True)
                with open(save_path, "wb") as f:
                    for chunk in v_res.iter_content(chunk_size=1024):
                        f.write(chunk)
                
                return save_path

        except Exception as e:
            print(f"Error fetching video: {e}")
            return None

if __name__ == "__main__":
    engine = SourcingEngine()
    print(engine.fetch_vertical_video(["Cinematic Luxury"], "Crypto Trading"))
