import json
import os
from config import BASE_DIR

class StateManager:
    def __init__(self):
        self.state_file = os.path.join(BASE_DIR, "state.json")
        self.default_state = {
            "last_step": "Idle",
            "current_niche": "wellness",
            "progress": 0,
            "latest_video": None,
            "queue": [],
            "history": []
        }
        if not os.path.exists(self.state_file):
            self.save_state(self.default_state)

    def load_state(self):
        try:
            with open(self.state_file, "r") as f:
                return json.load(f)
        except Exception:
            return self.default_state

    def save_state(self, state):
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)

    def update_step(self, step_name, progress=0, latest_video=None):
        state = self.load_state()
        state["last_step"] = step_name
        state["progress"] = progress
        if latest_video:
            state["latest_video"] = latest_video
            state["history"].append(latest_video)
        self.save_state(state)

if __name__ == "__main__":
    sm = StateManager()
    sm.update_step("Generating Wellness Script", 25)
    print("State updated successfully.")
