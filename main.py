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


def run_production(niche="wellness", goal="engagement", strategy="hormozi_unit", is_dry_run=True, override_script=None):
    """
    Runs a production cycle using the General Hendricks Universal OS.
    If override_script is provided, it skips the intelligence phase.
    """
    print(f"\n🚀 DEPLOYING MISSION: {niche.upper()} | GOAL: {goal.upper()}\n")
    sm = StateManager()

    # 1. Research (Intelligence)
    if override_script:
        print("[1/4] 🧠 Proceeding with approved intelligence...")
        script = override_script
    else:
        print(f"[1/4] 🧠 Running Viral Research ({strategy})...")
        sm.update_step("Viral Research", 10)
        researcher = ContentResearcher()
        script = researcher.generate_viral_script(niche, goal, strategy)
        
    if not script:
        print("❌ Intelligence failure.")
        return
    print(f"  Hook: {script['hook']}")

    # 2. Source (Production Support)
    print("\n[2/4] 🎥 Sourcing cinematic footage...")
    sm.update_step("Sourcing Assets", 35)
    sourcer = SourcingEngine()
    video_path = sourcer.fetch_vertical_video(script.get("mood_keywords", ["cinematic"]), niche)
    if not video_path:
        print("❌ Sourcing failed.")
        return

    # 3. Voice (Execution)
    print("\n[3/4] 🎙️ Generating narration...")
    sm.update_step("Voice Synthesis", 60)
    voicer = VoiceEngine()
    full_text = f"{script['hook']} {script['problem']} {script['insight']} {script['payoff']} {script['cta']}"
    audio_path = voicer.generate_narration(full_text, f"{niche}_{int(time.time())}")

    # 4. Assembly (Mission Ready)
    print("\n[4/4] 🎬 Assembling Premium Ad...")
    sm.update_step("Video Assembly", 85)
    producer = VideoGenerator()
    output_name = f"Hendricks_{niche}_{int(time.time())}.mp4"
    final_path = producer.create_reel(video_path, audio_path, script, output_name)
    
    if final_path:
        print(f"\n✅ MISSION COMPLETE: {final_path}")
        sm.update_step("Mission Successful", 100, latest_video=final_path)


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Royalle Source Universal Social Agent")
    parser.add_argument("--niche", type=str, default="wellness", help="Campaign niche")
    parser.add_argument("--goal", type=str, default="engagement", help="Campaign goal")
    parser.add_argument("--strategy", type=str, default="hormozi_unit", help="Viral strategy")
    parser.add_argument("--test", action="store_true", help="Run a test cycle")
    args = parser.parse_args()

    if args.test:
        run_production(args.niche, args.goal, args.strategy, is_dry_run=True)
    else:
        # Default to scheduler or specific production
        run_production(args.niche, args.goal, args.strategy)


if __name__ == "__main__":
    main()
