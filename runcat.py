import pystray
from pystray import MenuItem as item
from PIL import Image
import psutil
import threading
import time
import sys
import os
import json

CONFIG_FILE = "config.json"

# GLOBAL INSTANCE HOLDER
app_instance = None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Fixed label function (MUST be global, not class method)
def speed_boost_label(icon, item):
    return f"{'✅ ' if app_instance and app_instance.boost_mode else ''}Speed Boost"

class RunCatTray:
    def __init__(self):
        global app_instance
        app_instance = self  # store reference globally for label function

        self.load_config()
        self.frames = self.load_theme_frames()
        self.index = 0
        self.icon = pystray.Icon("RunCat")
        self.running = True

        self.icon.icon = self.frames[0]
        self.icon.title = "RunCat CPU Monitor"

        self.icon.menu = pystray.Menu(
            item(lambda item: f"{'✅ ' if self.boost_mode else ''}Speed Boost", self.toggle_speed_boost),
            item("Toggle Theme", self.toggle_theme),
            item("Quit", self.quit_app)
        )


    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.theme = config.get("theme", "dark")
                self.boost_mode = config.get("boost_mode", False)
        else:
            self.theme = "dark"
            self.boost_mode = False

    def save_config(self):
        config = {
            "theme": self.theme,
            "boost_mode": self.boost_mode
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def load_theme_frames(self):
        frames = []
        i = 0
        while True:
            found = False
            for ext in [".ico", ".png"]:
                path = resource_path(f"cat/{self.theme}_cat_{i}{ext}")
                if os.path.exists(path):
                    frames.append(Image.open(path))
                    found = True
                    break
            if not found:
                break
            i += 1

        if not frames:
            print(f"❌ No frames found for theme '{self.theme}' in 'cat/' folder.")
            sys.exit(1)

        return frames

    def toggle_theme(self, icon, item):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.frames = self.load_theme_frames()
        self.index = 0
        self.save_config()
        print(f"🌗 Theme switched to: {self.theme}")

    def toggle_speed_boost(self, icon, item):
        self.boost_mode = not self.boost_mode
        self.save_config()
        print(f"⚡ Speed Boost {'enabled' if self.boost_mode else 'disabled'}")

    def run(self):
        threading.Thread(target=self.animate_icon, daemon=True).start()
        self.icon.run()

    def animate_icon(self):
        psutil.cpu_percent(interval=None)
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=None)
            except Exception as e:
                print(f"⚠️ CPU reading failed: {e}")
                cpu = 50

            speed = 0.015 if self.boost_mode else 0.015 + (0.1 - 0.015) * (1 - cpu / 100)

            self.index = (self.index + 1) % len(self.frames)
            self.icon.icon = self.frames[self.index]
            self.icon.title = f"CPU Usage: {cpu:.0f}%"
            time.sleep(speed)

    def quit_app(self, icon, item):
        self.running = False
        self.icon.stop()

if __name__ == "__main__":
    app = RunCatTray()
    app.run()
