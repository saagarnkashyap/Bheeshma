import os
import json
from gtts import gTTS

# Load the Bhagavad Gita JSON file
with open(r"E:\Personal\projects\Bheeshma\bhagavad_gita_complete.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Output folder
os.makedirs("audio", exist_ok=True)

chapters = data["chapters"]

for chapter in chapters:
    for shloka in chapter["shlokas"]:
        chapter_num = chapter["number"]
        shloka_num = shloka["shloka_number"]
        text = shloka["sanskrit_text"]

        filename = f"audio/{chapter_num}_{shloka_num}.mp3"
        
        if not os.path.exists(filename):  # Avoid overwriting if already exists
            print(f"Generating {filename}")
            tts = gTTS(text=text, lang='hi')  # Hindi TTS for Sanskrit script
            tts.save(filename)
        else:
            print(f"Skipping {filename} (already exists)")
