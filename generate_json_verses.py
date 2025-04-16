import json

# Total verses per chapter
chapter_verse_counts = {
    1: 47,  2: 72,  3: 43,  4: 42,  5: 29,  6: 47,
    7: 30,  8: 28,  9: 34, 10: 42, 11: 55, 12: 20,
    13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78
}

# Generate the proper Supersite-style links
audio_links = {}

for chapter in range(1, 19):
    sloka_map = {}
    for sloka in range(1, chapter_verse_counts[chapter] + 1):
        sloka_map[str(sloka)] = f"CHAP{chapter}/{chapter}-{sloka}.MP3"
    audio_links[str(chapter)] = sloka_map

# Save to JSON file
with open("gita_audio_links.json", "w", encoding="utf-8") as f:
    json.dump(audio_links, f, indent=2)

print("✅ gita_audio_links.json generated!")
