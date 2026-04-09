import requests
import json
import os
import time
from config import (
    META_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID, FACEBOOK_PAGE_ID,
    YOUTUBE_CLIENT_SECRET_FILE, BASE_DIR
)
from state_manager import StateManager


class MultiPoster:
    """
    Unified connector for posting Reels/Shorts to Instagram, Facebook, and YouTube.
    """
    def __init__(self, profile=None):
        self.state = StateManager()
        self.graph_url = "https://graph.facebook.com/v19.0"
        self.set_profile(profile)

    def set_profile(self, profile):
        """
        Dynamically switches API credentials to a specific social media profile.
        """
        if profile:
            self.meta_token = profile.get("meta_token", META_ACCESS_TOKEN)
            self.ig_id = profile.get("ig_id", INSTAGRAM_ACCOUNT_ID)
            self.fb_id = profile.get("fb_id", FACEBOOK_PAGE_ID)
            self.yt_secret = profile.get("youtube_secret", YOUTUBE_CLIENT_SECRET_FILE)
        else:
            self.meta_token = META_ACCESS_TOKEN
            self.ig_id = INSTAGRAM_ACCOUNT_ID
            self.fb_id = FACEBOOK_PAGE_ID
            self.yt_secret = YOUTUBE_CLIENT_SECRET_FILE

    # ═══════════════════════════════════════════════════
    #  INSTAGRAM REELS (via Meta Graph API)
    # ═══════════════════════════════════════════════════
    def post_instagram_reel(self, video_url, caption):
        """
        Posts a Reel to Instagram using the Meta Graph API.
        Requires the video to be hosted at a public URL.
        For local files, you must first upload to a hosting service.
        """
        if self.meta_token == "YOUR_META_ACCESS_TOKEN":
            print("[IG] ⚠ META_ACCESS_TOKEN not configured. Skipping Instagram.")
            return None

        try:
            # Step 1: Create a media container
            container_url = f"{self.graph_url}/{self.ig_id}/media"
            payload = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "access_token": self.meta_token
            }
            res = requests.post(container_url, data=payload)
            res.raise_for_status()
            container_id = res.json().get("id")

            if not container_id:
                print(f"[IG] ❌ Failed to create container: {res.json()}")
                return None

            # Step 2: Wait for processing (Meta processes async)
            print("[IG] ⏳ Waiting for Instagram to process the Reel...")
            for _ in range(30):  # Poll for up to 5 minutes
                status_url = f"{self.graph_url}/{container_id}?fields=status_code&access_token={self.meta_token}"
                status_res = requests.get(status_url).json()
                if status_res.get("status_code") == "FINISHED":
                    break
                time.sleep(10)

            # Step 3: Publish
            publish_url = f"{self.graph_url}/{self.ig_id}/media_publish"
            pub_payload = {
                "creation_id": container_id,
                "access_token": self.meta_token
            }
            pub_res = requests.post(publish_url, data=pub_payload)
            pub_res.raise_for_status()
            media_id = pub_res.json().get("id")
            print(f"[IG] ✅ Reel published! Media ID: {media_id}")
            return media_id

        except Exception as e:
            print(f"[IG] ❌ Error posting Reel: {e}")
            return None

    # ═══════════════════════════════════════════════════
    #  FACEBOOK REELS (via Meta Graph API)
    # ═══════════════════════════════════════════════════
    def post_facebook_reel(self, video_url, description):
        """
        Posts a Reel to a Facebook Page using the Graph API.
        """
        if self.meta_token == "YOUR_META_ACCESS_TOKEN":
            print("[FB] ⚠ META_ACCESS_TOKEN not configured. Skipping Facebook.")
            return None

        try:
            # Step 1: Initialize upload
            init_url = f"{self.graph_url}/{self.fb_id}/video_reels"
            init_payload = {
                "upload_phase": "start",
                "access_token": self.meta_token
            }
            init_res = requests.post(init_url, data=init_payload)
            init_res.raise_for_status()
            video_id = init_res.json().get("video_id")

            if not video_id:
                print(f"[FB] ❌ Failed to initialize upload: {init_res.json()}")
                return None

            # Step 2: Upload video binary
            upload_url = f"{self.graph_url}/{self.fb_id}/video_reels"
            upload_payload = {
                "upload_phase": "transfer",
                "video_id": video_id,
                "video_file_url": video_url,
                "access_token": self.meta_token
            }
            upload_res = requests.post(upload_url, data=upload_payload)
            upload_res.raise_for_status()

            # Step 3: Publish
            finish_url = f"{self.graph_url}/{self.fb_id}/video_reels"
            finish_payload = {
                "upload_phase": "finish",
                "video_id": video_id,
                "description": description,
                "access_token": self.meta_token
            }
            finish_res = requests.post(finish_url, data=finish_payload)
            finish_res.raise_for_status()
            print(f"[FB] ✅ Reel published! Video ID: {video_id}")
            return video_id

        except Exception as e:
            print(f"[FB] ❌ Error posting Reel: {e}")
            return None

    # ═══════════════════════════════════════════════════
    #  YOUTUBE SHORTS (via YouTube Data API v3)
    # ═══════════════════════════════════════════════════
    def post_youtube_short(self, video_path, title, description, tags=None):
        """
        Uploads a YouTube Short using the YouTube Data API.
        Requires OAuth2 credentials (client_secret.json).
        """
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            print("[YT] ⚠ google-api-python-client or google-auth-oauthlib not installed.")
            print("[YT]   Run: pip install google-api-python-client google-auth-oauthlib")
            return None

        secret_path = os.path.join(BASE_DIR, self.yt_secret)
        if not os.path.exists(secret_path):
            print(f"[YT] ⚠ YouTube client_secret.json not found at: {secret_path}")
            print("[YT]   Download it from Google Cloud Console > APIs > Credentials.")
            return None

        try:
            scopes = ["https://www.googleapis.com/auth/youtube.upload"]
            flow = InstalledAppFlow.from_client_secrets_file(secret_path, scopes)
            credentials = flow.run_local_server(port=0)
            youtube = build("youtube", "v3", credentials=credentials)

            body = {
                "snippet": {
                    "title": title,
                    "description": description + "\n#Shorts",
                    "tags": tags or ["wellness", "lifestyle", "royallesource"],
                    "categoryId": "22"  # People & Blogs
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }

            media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = request.execute()
            vid = response.get("id")
            print(f"[YT] ✅ Short uploaded! Video ID: {vid}")
            print(f"[YT]    URL: https://youtube.com/shorts/{vid}")
            return vid

        except Exception as e:
            print(f"[YT] ❌ Error uploading Short: {e}")
            return None

    # ═══════════════════════════════════════════════════
    #  UNIFIED POSTER
    # ═══════════════════════════════════════════════════
    def post_everywhere(self, video_path, video_url, caption, title=None):
        """
        Posts the same content to all 3 platforms.
        video_path: local file path (for YouTube)
        video_url:  public URL (for Instagram/Facebook)
        """
        results = {}
        self.state.update_step("Uploading to Instagram...", 85)
        results["instagram"] = self.post_instagram_reel(video_url, caption)

        self.state.update_step("Uploading to Facebook...", 90)
        results["facebook"] = self.post_facebook_reel(video_url, caption)

        self.state.update_step("Uploading to YouTube...", 95)
        results["youtube"] = self.post_youtube_short(
            video_path,
            title or caption[:70],
            caption,
            tags=["royallesource", "wellness", "viral", "shorts"]
        )

        self.state.update_step("All Uploads Complete!", 100)
        return results


if __name__ == "__main__":
    poster = MultiPoster()
    print("MultiPoster initialized. Configure your API tokens in .env to start posting.")
