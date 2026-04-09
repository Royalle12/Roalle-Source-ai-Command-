"""
═══════════════════════════════════════════════════════════════
 ROYALLE SOURCE — AI SOCIAL AGENT
 Main Entry Point
 
 This script orchestrates the entire Royalle Source system:
   1. Starts the Smart Scheduler (3x morning burst)
   2. Launches the Executive Dashboard
   3. Manages the production pipeline
═══════════════════════════════════════════════════════════════
"""
import sys
import os
import time
import random
import argparse

# Ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import POSTING_TIMES, TIMEZONE
from researcher import ContentResearcher
from sourcing_engine import SourcingEngine
from voice_engine import VoiceEngine
from video_generator import VideoGenerator
from multi_poster import MultiPoster
from analytics_tracker import AnalyticsTracker
from state_manager import StateManager
from scheduler import SmartScheduler


BANNER = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   👑  R O Y A L L E   S O U R C E                       ║
║                                                          ║
║   AI Social Agent v1.0                                   ║
║   Cape Town, South Africa (SAST)                         ║
║                                                          ║
║   Niches: Health/Wellness + Lifestyle/Food               ║
║   Platforms: Instagram | Facebook | YouTube              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def run_single(niche="wellness"):
    """
    Runs a single production cycle for testing.
    Generates one Reel without posting.
    """
    print(f"\n🎬 Running single {niche} production (DRY RUN)...\n")
    sm = StateManager()

    # 1. Research
    print("[1/4] 📝 Generating script...")
    sm.update_step("Generating Script", 10)
    researcher = ContentResearcher()
    script = researcher.generate_viral_script(niche)
    if not script:
        print("❌ Script generation failed. Check your GEMINI_API_KEY.")
        return
    print(f"  Title: {script.get('title', 'N/A')}")
    print(f"  Hook: {script.get('hook', 'N/A')}")

    # 2. Source footage
    print("\n[2/4] 🎥 Sourcing vertical footage...")
    sm.update_step("Sourcing Footage", 30)
    sourcer = SourcingEngine()
    keywords = script.get("mood_keywords", ["aesthetic cinematic"])
    query = random.choice(keywords)
    print(f"  Search query: {query}")
    video_path = sourcer.fetch_vertical_video(query)
    if not video_path:
        print("❌ Video sourcing failed. Check your PEXELS_API_KEY.")
        return
    print(f"  Saved to: {video_path}")

    # 3. Voice narration
    print("\n[3/4] 🎙️ Generating narration...")
    sm.update_step("Generating Voice", 55)
    voicer = VoiceEngine()
    narration = f"{script['hook']} {script['script_body']} {script['cta']}"
    audio_path = voicer.generate_narration(narration, f"test_{niche}_{int(time.time())}")
    if not audio_path:
        print("❌ Voice generation failed.")
        return
    print(f"  Saved to: {audio_path}")

    # 4. Produce video
    print("\n[4/4] 🎬 Assembling Reel...")
    sm.update_step("Assembling Video", 75)
    producer = VideoGenerator()
    output_name = f"Royalle_{niche}_TEST_{int(time.time())}.mp4"
    final_path = producer.create_reel(video_path, audio_path, script, output_name)
    if not final_path:
        print("❌ Video production failed.")
        return

    sm.update_step("Test Complete!", 100, latest_video=final_path)
    print(f"\n{'='*50}")
    print(f"✅ SUCCESS! Pilot Reel saved to:")
    print(f"   {final_path}")
    print(f"{'='*50}")
    print(f"\nOpen the dashboard to preview it!")


def run_scheduler():
    """
    Starts the full automated scheduler.
    """
    scheduler = SmartScheduler()
    scheduler.run()


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Royalle Source AI Social Agent")
    parser.add_argument("--mode", choices=["test", "schedule", "wellness", "food"],
                       default="schedule",
                       help="Run mode: 'test' for dry run, 'schedule' for full automation")
    args = parser.parse_args()

    if args.mode == "test":
        run_single("wellness")
    elif args.mode == "wellness":
        run_single("wellness")
    elif args.mode == "food":
        run_single("food")
    elif args.mode == "schedule":
        run_scheduler()


if __name__ == "__main__":
    main()
