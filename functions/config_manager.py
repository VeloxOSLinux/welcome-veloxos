import json
import os

# Pfad zur Config-Datei (Plattformübergreifend)
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".veloxos_welcome.json")

DEFAULT_CONFIG = {
    "language": "en",
    "autostart": True
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(lang, autostart):
    config = {
        "language": lang,
        "autostart": autostart
    }
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")