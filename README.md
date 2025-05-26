<div align="center">

# Bheeshma – Bhagavad Gita Explorer

**A spiritual web companion that brings timeless Gita wisdom to life.**  
Built using Python, Streamlit, and modern UI/UX principles for immersive self-discovery.


![Screen Recording 2025-05-26 194934 (1)](https://github.com/user-attachments/assets/281a2d8e-b89f-4e30-9c77-dfe95aff41b9)



</div>

---

## Preview



---

## Features

**Verse-by-verse shloka explorer** with:
- Sanskrit (Devanagari)
- Transliteration
- Meaning, Interpretation, Life Application
- Audio playback (Gita Supersite + fallback TTS)

**Life Help** mode:
- Emotional problems → Gita verses mapped
- Eg: *anger*, *fear*, *loss*, *motivation*, *ego*...

**Text-to-speech** narration for English sections

**Dark mode divine UI**:
- Chakra animation 
- Floating nav bar 
- Custom fonts: Sanskrit Text, Diomag, Barter



---

## Project Structure

```bash
Bheeshma/
│
├── streamlit_app.py            # Main Streamlit App
├── bhagavad_gita_complete.json # Shloka + emotion data
├── audio_chunk_mapping.json    # Official Gita audio chunks
├── requirements.txt            # Dependencies
└── README.md                   # This file
