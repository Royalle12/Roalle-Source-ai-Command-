import schedule
import time
import random
import json
import os
from datetime import datetime
from config import POSTING_TIMES, TIMEZONE, BASE_DIR
from researcher import ContentResearcher
from sourcing_engine import SourcingEngine
from voice_engine import VoiceEngine
from video_generator import VideoGenerator
from multi_poster import MultiPoster
from analytics_tracker import AnalyticsTracker
from state_manager import StateManager

PERFORMANCE_LOG = os.path.join(BASE_DIR, "performance_log.json")


class SmartScheduler:
    """
    Cape Town timezone-aware scheduler that posts at optimal viral windows
    and self-adjusts based on analytics feedback.
    """
    def __init__(self):
        self.state = StateManager()
        self.analytics = AnalyticsTracker()
        self.posting_times = list(POSTING_TIMES)
        self.niche_rotation = ["wellness", "food", "wellness"]  # 3x morning burst

    def get_optimal_times(self):
        """
        Checks the analytics log for optimized posting times.
        Falls back to the defaults if no data exists yet.
        """
        try:
            log = self.analytics.load_log()
            optimal = log.get("optimal_times", [])
            if len(optimal) >= 3:
                self.posting_times = optimal[:3]
                print(f"[SCHEDULER] 🎯 Using optimized times: {self.posting_times}")
            else:
                print(f"[SCHEDULER] Using default times: {self.posting_times}")
        except Exception:
            print(f"[SCHEDULER] Using default times: {self.posting_times}")

    def schedule_daily_cycle(self):
        """
        Sets up the daily production cycle with 3 morning posts.
        """
        self.get_optimal_times()

        for i, post_time in enumerate(self.posting_times):
            niche = self.niche_rotation[i % len(self.niche_rotation)]
            schedule.every().day.at(post_time).do(self._produce_and_post, niche=niche, slot=i + 1)
            print(f"[SCHEDULER] ⏰ Slot {i+1}: {post_time} → {niche.upper()}")

        # Daily analytics refresh at 11 PM
        schedule.every().day.at("23:00").do(self._nightly_analytics)
        print("[SCHEDULER] 📊 Nightly analytics refresh at 23:00")

        # Re-optimize times at midnight
        schedule.every().day.at("00:01").do(self.get_optimal_times)
        print("[SCHEDULER] 🔄 Time re-optimization at 00:01")

    def _produce_and_post(self, niche, slot):
        """
        Full pipeline: Research → Source → Voice → Produce → Post
        """
        now = datetime.now()
        print(f"\n{'='*60}")
        print(f"[SCHEDULER] 🚀 SLOT {slot} FIRING — {niche.upper()} — {now.strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")

        self.state.update_step(f"Slot {slot}: Researching {niche}...", 10)

        try:
            # 1. Research
            researcher = ContentResearcher()
            script = researcher.generate_viral_script(niche)
            if not script:
                self.state.update_step(f"Slot {slot}: Script failed", 0)
                return
            self.state.update_step(f"Slot {slot}: Script ready", 25)

            # 2. Source footage
            sourcer = SourcingEngine()
            keywords = script.get("mood_keywords", ["aesthetic cinematic"])
            query = random.choice(keywords)
            video_path = sourcer.fetch_vertical_video(query)
            if not video_path:
                self.state.update_step(f"Slot {slot}: Sourcing failed", 0)
                return
            self.state.update_step(f"Slot {slot}: Footage sourced", 45)

            # 3. Voice narration
            voicer = VoiceEngine()
            narration = f"{script['hook']} {script['script_body']} {script['cta']}"
            audio_path = voicer.generate_narration(narration, f"{niche}_slot{slot}_{int(time.time())}")
            if not audio_path:
                self.state.update_step(f"Slot {slot}: Voice failed", 0)
                return
            self.state.update_step(f"Slot {slot}: Voice ready", 60)

            # 4. Produce video
            producer = VideoGenerator()
            output_name = f"Royalle_{niche}_s{slot}_{int(time.time())}.mp4"
            final_path = producer.create_reel(video_path, audio_path, script, output_name)
            if not final_path:
                self.state.update_step(f"Slot {slot}: Production failed", 0)
                return
            self.state.update_step(f"Slot {slot}: Video ready", 80)

            # 5. Post
            caption = f"{script['hook']}\n\n{script['script_body']}\n\n{script['cta']}\n\n#RoyalleSource #Wellness #Viral #Lifestyle"
            poster = MultiPoster()
            results = poster.post_everywhere(
                video_path=final_path,
                video_url=final_path,  # Replace with hosted URL in production
                caption=caption,
                title=script.get("title", "Royalle Source")
            )

            # 6. Log to analytics
            posted_at = datetime.now().isoformat()
            for platform, post_id in results.items():
                if post_id:
                    self.analytics.log_post(niche, platform, post_id, posted_at, final_path)

            self.state.update_step(f"Slot {slot} Complete! ✅", 100)
            print(f"\n[SCHEDULER] ✅ Slot {slot} complete: {output_name}\n")

        except Exception as e:
            self.state.update_step(f"Slot {slot} Error: {str(e)[:50]}", 0)
            print(f"[SCHEDULER] ❌ Slot {slot} error: {e}")

    def _nightly_analytics(self):
        """
        Runs the nightly analytics refresh and generates a daily report.
        """
        print("\n[SCHEDULER] 🌙 Running nightly analytics...")
        self.analytics.refresh_all_metrics()
        self.analytics.analyze_best_times()
        report = self.analytics.generate_daily_report()
        print(f"[SCHEDULER] 📊 Daily report saved.")

    def run(self):
        """
        Main loop. Keeps the scheduler alive.
        """
        self.schedule_daily_cycle()
        print(f"\n[SCHEDULER] 👑 ROYALLE SOURCE AGENT ARMED — Cape Town Time")
        print(f"[SCHEDULER] Waiting for scheduled slots...\n")

        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == "__main__":
    scheduler = SmartScheduler()
    scheduler.run()
