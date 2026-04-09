"""
═══════════════════════════════════════════════════════════════
 ROYALLE SOURCE — UNIFIED LAUNCHER
 Starts both the Agent and the Dashboard simultaneously.
═══════════════════════════════════════════════════════════════
"""
import subprocess
import sys
import os
import time
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_URL = "http://localhost:8501"


def launch():
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║  👑 ROYALLE SOURCE — LAUNCHING COMMAND CENTER   ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

    # 1. Start the Agent scheduler in the background
    print("[1/2] 🤖 Starting AI Agent (scheduler)...")
    agent_proc = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "main.py"), "--mode", "schedule"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    print(f"      PID: {agent_proc.pid}")
    print("      ✅ Agent armed.\n")

    # 2. Launch the Streamlit dashboard
    print("[2/2] 🖥️  Starting Executive Dashboard...")
    print(f"      URL: {DASHBOARD_URL}")
    print()

    # Open browser after a short delay
    time.sleep(2)
    webbrowser.open(DASHBOARD_URL)

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run",
             os.path.join(BASE_DIR, "dashboard.py"),
             "--server.port", "8501",
             "--server.headless", "true",
             "--theme.base", "dark",
             "--theme.primaryColor", "#FFD700",
             "--theme.backgroundColor", "#0a0a0f",
             "--theme.secondaryBackgroundColor", "#111122",
             "--theme.textColor", "#e0e0e0"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👑 Shutting down Royalle Source...")
        agent_proc.terminate()
        print("   Agent stopped.")
        print("   Dashboard stopped.")
        print("   Goodbye, Boss! 😎\n")


if __name__ == "__main__":
    launch()
