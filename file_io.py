# file_io.py
# Save and load high score and level data

import json

def load_game_data(filename="score.json"):
    """Load high score and max level from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        # 如果文件不存在或损坏，就创建一个默认字典
        return {"high_score": 0, "max_level": 1}

def save_game_data(data, filename="score.json"):
    """Save high score and max level to JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving game data:", e)