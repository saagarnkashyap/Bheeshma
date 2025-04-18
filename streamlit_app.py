import streamlit as st
import json
import difflib
import re
from gtts import gTTS
import requests
from io import BytesIO
import io
import openai
import requests
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit page config FIRST
st.set_page_config(page_title="Bheeshma – Bhagavad Gita")

# --- Load data ---
@st.cache_data
def load_data():
    with open("bhagavad_gita_complete.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
data = load_data()
chapters = data["chapters"]
problem_map = data.get("problem_solutions_map", {})
import difflib  # Make sure this is at the top


# #------------------------------CSS------------------------------

# #------------------------------CSS------------------------------
# st.markdown("""
# <!-- ✅ Load Fonts -->
# <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari&family=Unbounded:wght@400;700&family=Inter&display=swap" rel="stylesheet">

# <style>
# /* 🌑 Global Dark Background */
# body {
#     background-color: #000000;
#     color: white;
#     font-family: 'Inter', sans-serif;
#     margin: 0;
#     padding: 0;
#     overflow-x: hidden;
# }

# div[data-testid="stAppViewContainer"] {
#     background-color: #000000 !important;
#     color: white !important;
#     font-family: 'Inter', sans-serif;
#     overflow-x: hidden;
#     padding-bottom: 80px;
# }

# /* ✨ Headings (Unbounded) */
# h1, h2, h3 {
#     font-family: 'Unbounded', cursive !important;
#     color: white !important;
#     text-shadow: 0 0 8px #ffffff55;
#     word-wrap: break-word;
# }

# /* 🕉️ Main Title */
# .title {
#     text-align: center;
#     font-size: clamp(2rem, 5vw, 3rem);
#     color: white;
#     margin: 1rem 0 1.5rem;
#     text-shadow: 0 0 10px #ffffff88;
#     font-family: 'Unbounded', cursive !important;
# }

# /* 📜 Shloka Sanskrit Style (Noto) */
# .shloka-sanskrit {
#     font-family: 'Noto Serif Devanagari', serif;
#     font-size: clamp(1.1rem, 3vw, 1.3rem);
#     color: #fffacd;
#     line-height: 1.8;
# }

# /* 🧱 Section Cards */
# .section {
#     padding: 1rem;
#     border-radius: 15px;
#     background: rgba(255, 255, 255, 0.05);
#     margin: 1rem auto;
#     box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
#     max-width: 900px;
# }

# /* 🔗 Link Styles */
# a {
#     color: #FFD700;
#     word-wrap: break-word;
# }
# a:hover {
#     text-shadow: 0 0 10px white;
#     color: #ffffff;
# }

# /* 🧭 Floating Chapter Navbar */
# #chapter-nav {
#     position:fixed;
#     top:0;
#     left:0;
#     width:100%;
#     overflow-x: auto;
#     white-space: nowrap;
#     padding: 10px;
#     background:#000;
#     border-bottom:1px solid white;
#     text-align:center;
#     font-size: 14px;
#     z-index: 9999;
# }

# #chapter-nav a {
#     display: inline-block;
#     margin: 0 10px;
#     font-weight: bold;
# }

# /* 🔄 Chakra Spinner */
# @keyframes spin {
#   from { transform: rotate(0deg); }
#   to { transform: rotate(360deg); }
# }

# .chakra-spinner {
#     position: fixed;
#     top: 10px;
#     right: 15px;
#     animation: spin 8s linear infinite;
#     width: 50px;
#     z-index: 999;
# }

# /* 🧱 Expanders */
# [data-testid="stExpander"] {
#     max-width: 100%;
#     margin-bottom: 1rem;
# }

# /* 🎧 Meditative Button */
# #chant-btn {
#     position: fixed;
#     bottom: 20px;
#     right: 20px;
#     max-width: 90vw;
#     font-size: 14px;
#     padding: 10px 18px;
#     border-radius: 30px;
#     z-index: 99999;
#     text-align: center;
# }

# /* 📱 Mobile Tweaks */
# @media (max-width: 600px) {
#   .title {
#     font-size: 2rem;
#     padding: 0 1rem;
#   }
#   .section {
#     padding: 1rem;
#     margin: 0.5rem;
#   }
#   #chant-btn {
#     font-size: 13px;
#     bottom: 15px;
#     right: 10px;
#     padding: 10px;
#   }
#   .chakra-spinner {
#     width: 40px;
#     top: 5px;
#     right: 10px;
#   }
#   .shloka-sanskrit {
#     font-size: 1.1rem;
#   }
# }
# </style>
# """, unsafe_allow_html=True)





st.markdown("""
<!-- ✅ Load Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari&family=Unbounded:wght@400;700&family=Inter&display=swap" rel="stylesheet">

<style>
/* 🌑 Global Dark Background */
body {
    background-color: #000000;
    color: white;
    font-family: 'Inter', sans-serif;
}

div[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
    color: white !important;
    font-family: 'Inter', sans-serif;
}

/* ✨ Titles (Unbounded Font) */
h1, h2, h3 {
    font-family: 'Unbounded', cursive !important;
    color: white !important;
    text-shadow: 0 0 8px #ffffff55;
}

/* 🕉️ Main Title */
.title {
    text-align: center;
    font-size: 3em;
    color: white;
    margin-bottom: 30px;
    text-shadow: 0 0 10px #ffffff88;
    font-family: 'Unbounded', cursive !important;
}

/* 📜 Shloka Sanskrit Style (Noto Serif Devanagari) */
.shloka-sanskrit {
    font-family: 'Noto Serif Devanagari', serif;
    font-size: 1.2em;
    color: #fffacd;
    line-height: 1.8;
}

/* 🧱 Section Cards */
.section {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.05);
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
}

/* 🔗 Link Styles */
a {
    color: #FFD700;
}
a:hover {
    text-shadow: 0 0 10px white;
    color: #ffffff;
}

/* 🧭 Floating Chapter Navbar */
#chapter-nav {
    position:fixed;
    top:0;
    left:0;
    width:100%;
    background:#000;
    padding:10px;
    text-align:center;
    z-index:9999;
    border-bottom:1px solid white;
}

/* 🔄 Chakra Spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)



# Keyword alias map for flexible emotional input
keyword_aliases = {
    "sad": "depression",
    "sadness": "depression",
    "depressed": "depression",
    "grief": "depression",
    "grieving": "depression",
    "guilt": "feeling_sinful",
    "guilty": "feeling_sinful",
    "sinful": "feeling_sinful",
    "shame": "feeling_sinful",
    "hopeless": "losing_hope",
    "worthless": "losing_hope",
    "despair": "losing_hope",
    "jealous": "dealing_with_envy",
    "jealousy": "dealing_with_envy",
    "envy": "dealing_with_envy",
    "fearful": "fear",
    "afraid": "fear",
    "anxious": "fear",
    "anxiety": "fear",
    "stress": "fear",
    "angry": "anger",
    "rage": "anger",
    "lazy": "laziness",
    "procrastination": "laziness",
    "bored": "demotivated",
    "unmotivated": "demotivated",
    "lustful": "lust",
    "tempted": "temptation",
    "temptation": "temptation",
    "ego": "pride",
    "prideful": "pride",
    "arrogant": "pride",
    "arrogance": "pride",
    "alone": "loneliness",
    "lonely": "loneliness",
    "isolation": "loneliness"
}

# --- Session state setup ---
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = 1
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

# --- App Mode Switch ---
mode = st.sidebar.radio("Choose a View", [
    "📖 Explore Chapters",
    "🙏 Life Help",
    "🤖 Chat with Bheeshma"  # 👈 Add this here
])




# st.markdown("""
# <audio id="bg-chant" loop style="display:none">
#   <source src="https://raw.githubusercontent.com/saagarnkashyap/Bheeshma/main/OM%20Chanting%20%40417%20Hz%20_%20Removes%20All%20Negative%20Blocks%20%5B8sYK7lm3UKg_00_24_11_00_24_33_part%5D.mp3" type="audio/mpeg">
# </audio>

# <div style="
#   position: fixed;
#   bottom: 25px;
#   right: 25px;
#   z-index: 9999;
#   display: flex;
#   align-items: center;
#   gap: 10px;
# ">
#   <button onclick="fadeToggleChant()" id="chantBtn" style="
#     background: radial-gradient(circle, #ffd700, #ff9900);
#     color: black;
#     padding: 12px 18px;
#     border-radius: 30px;
#     font-weight: bold;
#     border: none;
#     box-shadow: 0 0 15px gold;
#     cursor: pointer;
#     font-size: 14px;
#     animation: pulse 2s infinite;
#   ">🔊 Play Meditative Chant</button>

#   <input type="range" min="0" max="1" step="0.01" value="1" id="chantVolume" style="width: 100px;">
# </div>

# <script>
#   const chant = document.getElementById('bg-chant');
#   const chantBtn = document.getElementById('chantBtn');
#   const chantVolume = document.getElementById('chantVolume');
#   let isPlaying = false;
#   let fading = false;

#   // Volume Control
#   chantVolume.addEventListener('input', () => {
#     chant.volume = parseFloat(chantVolume.value);
#   });

#   function fadeToggleChant() {
#     if (fading) return;
#     fading = true;

#     let volume = chant.volume;
#     const step = 0.05;

#     if (isPlaying) {
#       const fadeOut = setInterval(() => {
#         volume -= step;
#         chant.volume = Math.max(0, volume);
#         if (volume <= 0) {
#           chant.pause();
#           isPlaying = false;
#           chantBtn.innerText = "🧘 Play Meditative Chant";
#           clearInterval(fadeOut);
#           fading = false;
#         }
#       }, 80);
#     } else {
#       chant.volume = 0;
#       chant.play().then(() => {
#         const fadeIn = setInterval(() => {
#           volume += step;
#           chant.volume = Math.min(1, volume);
#           if (volume >= 1) {
#             isPlaying = true;
#             chantBtn.innerText = "⏸️ Pause Meditative Chant";
#             clearInterval(fadeIn);
#             fading = false;
#           }
#         }, 80);
#       }).catch(e => console.log("Playback failed:", e));
#     }
#   }

#   // Auto start after interaction
#   const tryAutoPlay = () => {
#     if (!isPlaying) {
#       chant.volume = 0;
#       chant.play().then(() => {
#         let v = 0;
#         const fadeIn = setInterval(() => {
#           v += 0.05;
#           chant.volume = Math.min(1, v);
#           if (v >= 1) {
#             isPlaying = true;
#             chantBtn.innerText = "⏸️ Pause Meditative Chant";
#             clearInterval(fadeIn);
#           }
#         }, 80);
#       }).catch(e => console.log("Autoplay blocked:", e));
#     }
#     document.removeEventListener('click', tryAutoPlay);
#     document.removeEventListener('touchstart', tryAutoPlay);
#   };

#   document.addEventListener('click', tryAutoPlay);
#   document.addEventListener('touchstart', tryAutoPlay);
# </script>

# <style>
# @keyframes pulse {
#   0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
#   70% { box-shadow: 0 0 0 20px rgba(255, 215, 0, 0); }
#   100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
# }
# </style>
# """, unsafe_allow_html=True)



#----------------------------original markdown for autoplay chanting--------------------------
st.markdown("""
<audio id="bg-chant" autoplay loop muted style="display:none">
  <source src="https://raw.githubusercontent.com/saagarnkashyap/Bheeshma/main/OM%20Chanting%20%40417%20Hz%20_%20Removes%20All%20Negative%20Blocks%20%5B8sYK7lm3UKg_00_24_11_00_24_33_part%5D.mp3" type="audio/mpeg">
</audio>

<button onclick="fadeToggleChant()" id="chant-btn" style="
  position: fixed;
  bottom: 25px;
  right: 25px;
  background: radial-gradient(circle, #ffd700, #ff9900);
  color: black;
  padding: 12px 22px;
  border-radius: 30px;
  font-weight: bold;
  border: none;
  box-shadow: 0 0 15px gold;
  z-index: 9999;
  cursor: pointer;
  font-size: 14px;
  animation: pulse 2s infinite;
">🔊 Pause Meditative Chant</button>

<script>
  const chant = document.getElementById('bg-chant');
  const btn = document.getElementById('chant-btn');
  let fading = false;
  let isPlaying = false;

  // Ensure playback starts after interaction
  window.addEventListener('DOMContentLoaded', () => {
    chant.muted = true;
    chant.volume = 0;
    chant.play().then(() => {
      fadeVolume(chant, 1, 1000);
      chant.muted = false;
      isPlaying = true;
    }).catch((e) => {
      console.log("Playback blocked until interaction:", e);
    });
  });

  function fadeVolume(audio, target, duration) {
    const stepTime = 50;
    const steps = duration / stepTime;
    const step = (target - audio.volume) / steps;
    let count = 0;

    const fade = setInterval(() => {
      audio.volume = Math.min(1, Math.max(0, audio.volume + step));
      count++;
      if (count >= steps) clearInterval(fade);
    }, stepTime);
  }

  function fadeToggleChant() {
    if (fading) return;
    fading = true;

    if (isPlaying) {
      fadeVolume(chant, 0, 800);
      setTimeout(() => {
        chant.pause();
        btn.innerText = "🔊 Play Meditative Chant";
        isPlaying = false;
        fading = false;
      }, 800);
    } else {
      chant.volume = 0;
      chant.play().then(() => {
        fadeVolume(chant, 1, 800);
        btn.innerText = "🔊 Pause Meditative Chant";
        isPlaying = true;
        fading = false;
      }).catch(() => {
        alert("🎧 Please interact with the page first (click anywhere)");
        fading = false;
      });
    }
  }
</script>

<style>
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
  70% { box-shadow: 0 0 0 20px rgba(255, 215, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
}
</style>
""", unsafe_allow_html=True)




# ======================= 📖 EXPLORE CHAPTERS =======================
def load_audio_map():
    with open("gita_audio_links.json", "r", encoding="utf-8") as f:
        return json.load(f)

AUDIO_LINKS = load_audio_map()
if mode == "📖 Explore Chapters":
    st.title("Bheeshma - Your Bhagavad Gita Companion")

    # --- Chapter Buttons ---
    st.markdown("### 🕉️ Select a Chapter")
    chapter_cols = st.columns(9)
    for i in range(1, 19):
        col = chapter_cols[(i - 1) % 9]
        if col.button(f"{i}"):
            st.session_state.selected_chapter = i
            st.session_state.selected_section = None

    chapter = next(c for c in chapters if c["number"] == st.session_state.selected_chapter)
    st.markdown(f"## {chapter['number']}. {chapter['name']}")

    # --- Bullet Subsection Nav ---
    st.markdown("### 🔍 Explore Section")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("• 📚 Philosophical Aspects"):
            st.session_state.selected_section = "philosophical_aspects"

    with col2:
        if st.button("• 💠 Life Problems Addressed"):
            st.session_state.selected_section = "life_problems_addressed"

    with col3:
        if st.button("• 🧘‍♂️ Yoga Type"):
            st.session_state.selected_section = "yoga_type"

    # --- Conditional Section Display ---
    if st.session_state.selected_section == "philosophical_aspects":
        st.markdown("#### 📚 Philosophical Aspects")
        for p in chapter["philosophical_aspects"]:
            st.markdown(f"- {p}")

    elif st.session_state.selected_section == "life_problems_addressed":
        st.markdown("#### 💠 Life Problems Addressed")
        for lp in chapter["life_problems_addressed"]:
            st.markdown(f"- {lp}")

    elif st.session_state.selected_section == "yoga_type":
        st.markdown("#### 🧘‍♂️ Yoga Type")
        st.info(chapter["yoga_type"])

    # --- Summary + Shlokas ---
    st.markdown("#### 🧘 Chapter Summary")
    st.markdown(chapter["summary"])

    for shloka in chapter["shlokas"]:
        with st.expander(f"Shloka {shloka['shloka_number']}"):
            st.markdown("**📖 Sanskrit**")
            st.markdown(f"<div class='shloka-sanskrit'>{shloka['sanskrit_text']}</div>", unsafe_allow_html=True)

            st.markdown("**🔤 Transliteration**")
            st.markdown(f"*{shloka['transliteration']}*")

            st.markdown("**🔊 Audio Recitation**")

                # Construct URL: CHAP<chapter>/<sloka>-<sloka>.MP3
            chapter_str = str(shloka["chapter"])
            sloka_str = str(shloka["shloka_number"])
            path = AUDIO_LINKS.get(chapter_str, {}).get(sloka_str)

            if path:
                audio_url = f"https://www.gitasupersite.iitk.ac.in/sites/default/files/audio/{path}"
                try:
                    r = requests.head(audio_url, timeout=5)
                    if r.status_code == 200:
                        st.audio(audio_url)
                    else:
                        raise Exception("Audio not available")
                except:
                    st.warning("⚠️ Official audio not available. Using fallback voice.")
                    try:
                        tts = gTTS(text=shloka["sanskrit_text"], lang="hi", slow=True)
                        audio_bytes = BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        st.audio(audio_bytes)
                    except Exception as e:
                        st.error(f"❌ Fallback audio failed: {e}")
            else:
                st.warning("⚠️ Audio path not found in map.")          
                
                # tts = gTTS(text=shloka['sanskrit_text'], lang='hi', slow=True)
                # audio_bytes = BytesIO()
                # tts.write_to_fp(audio_bytes)
                # audio_bytes.seek(0)
                # st.audio(audio_bytes)



            st.markdown("**🧠 Meaning**")
            st.markdown(shloka["meaning"])
            #---------this doesnt work... fix it later---------
            # st.markdown("**🔊 Listen to Meaning**")
            # def combine_and_speak(meaning, interpretation, application, lang="en"):
            #     full_text = (
            #             "Meaning: " + meaning + ". "
            #         )
            #     tts = gTTS(text=full_text, lang=lang, slow=False)
            #     audio_bytes = BytesIO()
            #     tts.write_to_fp(audio_bytes)
            #     audio_bytes.seek(0)
            #     return audio_bytes

            # tts_audio = combine_and_speak(
            #     shloka["meaning"],
            #     shloka["interpretation"],
            #     shloka["life_application"]
            #     )
            # st.audio(tts_audio, format="audio/mp3")

            st.markdown("**💬 Interpretation**")
            st.markdown(shloka["interpretation"])

            st.markdown("**🌱 Life Application**")
            st.markdown(shloka["life_application"])
            

    


# ======================= 🙏 LIFE HELP =======================


elif mode == "🙏 Life Help":
    st.title("🙏 Life Help from the Bhagavad Gita")
    st.markdown("Describe your challenge or emotion (e.g. `anger`, `guilt`, `sadness`, `loneliness`)")

    user_input = st.text_input("What are you feeling?", "").strip().lower()

    matched_key = None

    if user_input:
        # Step 1: check direct match
        if user_input in problem_map:
            matched_key = user_input

        # Step 2: check alias match
        elif user_input in keyword_aliases:
            matched_key = keyword_aliases[user_input]

        # Step 3: fuzzy match fallback
        else:
            all_keys = [key.replace("_", " ").lower() for key in problem_map.keys()]
            match = difflib.get_close_matches(user_input, all_keys, n=1, cutoff=0.5)
            if match:
                matched_key = next((key for key in problem_map if match[0] in key.replace("_", " ").lower()), None)

        # --- Show matched verse content ---
        if matched_key:
            problem = problem_map[matched_key]
            st.success(f"🧠 {problem['description']}")
            st.markdown("#### 🔗 Relevant Shlokas")

            for ref in problem["references"]:
                ch_num, sh_num = ref["chapter"], ref["shloka"]
                chapter = next((c for c in chapters if c["number"] == ch_num), None)
                if chapter:
                    shloka = next((s for s in chapter["shlokas"] if s["shloka_number"] == sh_num), None)
                    if shloka:
                        with st.expander(f"Chapter {ch_num}, Shloka {sh_num}"):
                            st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
                            st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
                            st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
                            st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
                            st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
        else:
            st.warning("🙏 Sorry, I couldn't find a matching emotion. Try keywords like `fear`, `guilt`, `jealousy`, `loneliness`, or `lust`.")


# ======================= 🤖 CHATBOT MODE =======================

# elif mode == "🤖 Chat with Bheeshma":
#     import openai
#     import os
#     from dotenv import load_dotenv

#     # Load environment variable
#     load_dotenv()
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     st.title("🧠 Chat with Bheeshma")
#     st.markdown("Ask about life, karma, fear, duty, or spiritual questions. Bheeshma will reply using the wisdom of the Bhagavad Gita.")

#     # Initialize message history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # User input field
#     if user_input := st.chat_input("What’s troubling you today, warrior?"):
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         with st.chat_message("assistant"):
#             with st.spinner("Consulting the Gita..."):
#                 try:
#                     client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#                     response = client.chat.completions.create(
#                         model="gpt-3.5-turbo",
#                         messages=[
#                             {"role": "system", "content": 
#                             "You are Bheeshma, a wise and spiritual guide from the Mahabharata. "
#                             "You respond using the teachings of the Bhagavad Gita. "
#                             "Cite shlokas with verse numbers when relevant. Speak with calm clarity, like a guru."},
#                             *st.session_state.messages
#                         ]
#                     )
#                     reply = response.choices[0].message.content
#                     st.markdown(reply)
#                     st.session_state.messages.append({"role": "assistant", "content": reply})
#                 except Exception as e:
#                     st.error(f"Failed to get response: {e}")



# ======================= 🔍 SEARCH SHLOKAS =======================
elif mode == "🔍 Search Shlokas":
    st.title("🔍 Search Shlokas")
    search_query = st.text_input("Search by keyword or type '2:47' to find a specific verse.")

    if search_query:
        if ":" in search_query:
            # Format: chapter:verse (e.g. 2:47)
            try:
                ch, sh = map(int, search_query.split(":"))
                chapter = next((c for c in chapters if c["number"] == ch), None)
                if chapter:
                    shloka = next((s for s in chapter["shlokas"] if s["shloka_number"] == sh), None)
                    if shloka:
                        st.markdown(f"### Chapter {ch}, Shloka {sh}")
                        st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
                        st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
                        st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
                        st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
                        st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
                    else:
                        st.error("Shloka not found.")
                else:
                    st.error("Chapter not found.")
            except ValueError:
                st.error("Invalid format. Use `chapter:verse`, e.g. `2:47`")
        else:
            st.markdown("### 🔎 Search Results")
            results = []
            for c in chapters:
                for s in c["shlokas"]:
                    if search_query.lower() in s["sanskrit_text"].lower() \
                    or search_query.lower() in s["transliteration"].lower() \
                    or search_query.lower() in s["meaning"].lower() \
                    or search_query.lower() in s["interpretation"].lower() \
                    or search_query.lower() in s["life_application"].lower():
                        results.append((c["number"], s))
            if results:
                for ch_num, shloka in results:
                    with st.expander(f"Chapter {ch_num}, Shloka {shloka['shloka_number']}"):
                        st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
                        st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
                        st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
                        st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
                        st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
            else:
                st.info("No results found.")

st.markdown(
    """
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <div style="text-align: center; font-size: 0.9rem; color: gray;">
        Made with 🕉️ by <strong>Saagar N Kashyap</strong>
    </div>
    """,
    unsafe_allow_html=True
)



#---------------------------------------------------------------------------------------------------------old code is here 592


# import streamlit as st
# import json
# import difflib
# import re
# from gtts import gTTS
# import requests
# from io import BytesIO
# import io
# import openai
# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Set Streamlit page config FIRST
# st.set_page_config(page_title="Bheeshma – Bhagavad Gita")

# # --- Load data ---
# @st.cache_data
# def load_data():
#     with open("bhagavad_gita_complete.json", "r", encoding="utf-8") as f:
#         return json.load(f)
    
# data = load_data()
# chapters = data["chapters"]
# problem_map = data.get("problem_solutions_map", {})
# import difflib  # Make sure this is at the top


# #------------------------------CSS------------------------------
# st.markdown("""
# <!-- ✅ Load Fonts -->
# <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari&family=Unbounded:wght@400;700&family=Inter&display=swap" rel="stylesheet">

# <style>
# /* 🌑 Global Dark Background */
# body {
#     background-color: #000000;
#     color: white;
#     font-family: 'Inter', sans-serif;
# }

# div[data-testid="stAppViewContainer"] {
#     background-color: #000000 !important;
#     color: white !important;
#     font-family: 'Inter', sans-serif;
# }

# /* ✨ Titles (Unbounded Font) */
# h1, h2, h3 {
#     font-family: 'Unbounded', cursive !important;
#     color: white !important;
#     text-shadow: 0 0 8px #ffffff55;
# }

# /* 🕉️ Main Title */
# .title {
#     text-align: center;
#     font-size: 3em;
#     color: white;
#     margin-bottom: 30px;
#     text-shadow: 0 0 10px #ffffff88;
#     font-family: 'Unbounded', cursive !important;
# }

# /* 📜 Shloka Sanskrit Style (Noto Serif Devanagari) */
# .shloka-sanskrit {
#     font-family: 'Noto Serif Devanagari', serif;
#     font-size: 1.2em;
#     color: #fffacd;
#     line-height: 1.8;
# }

# /* 🧱 Section Cards */
# .section {
#     padding: 20px;
#     border-radius: 15px;
#     background: rgba(255, 255, 255, 0.05);
#     margin-bottom: 20px;
#     box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
# }

# /* 🔗 Link Styles */
# a {
#     color: #FFD700;
# }
# a:hover {
#     text-shadow: 0 0 10px white;
#     color: #ffffff;
# }

# /* 🧭 Floating Chapter Navbar */
# #chapter-nav {
#     position:fixed;
#     top:0;
#     left:0;
#     width:100%;
#     background:#000;
#     padding:10px;
#     text-align:center;
#     z-index:9999;
#     border-bottom:1px solid white;
# }

# /* 🔄 Chakra Spinner */
# @keyframes spin {
#   from { transform: rotate(0deg); }
#   to { transform: rotate(360deg); }
# }
# </style>
# """, unsafe_allow_html=True)


# # Keyword alias map for flexible emotional input
# keyword_aliases = {
#     "sad": "depression",
#     "sadness": "depression",
#     "depressed": "depression",
#     "grief": "depression",
#     "grieving": "depression",
#     "guilt": "feeling_sinful",
#     "guilty": "feeling_sinful",
#     "sinful": "feeling_sinful",
#     "shame": "feeling_sinful",
#     "hopeless": "losing_hope",
#     "worthless": "losing_hope",
#     "despair": "losing_hope",
#     "jealous": "dealing_with_envy",
#     "jealousy": "dealing_with_envy",
#     "envy": "dealing_with_envy",
#     "fearful": "fear",
#     "afraid": "fear",
#     "anxious": "fear",
#     "anxiety": "fear",
#     "stress": "fear",
#     "angry": "anger",
#     "rage": "anger",
#     "lazy": "laziness",
#     "procrastination": "laziness",
#     "bored": "demotivated",
#     "unmotivated": "demotivated",
#     "lustful": "lust",
#     "tempted": "temptation",
#     "temptation": "temptation",
#     "ego": "pride",
#     "prideful": "pride",
#     "arrogant": "pride",
#     "arrogance": "pride",
#     "alone": "loneliness",
#     "lonely": "loneliness",
#     "isolation": "loneliness"
# }

# # --- Session state setup ---
# if "selected_chapter" not in st.session_state:
#     st.session_state.selected_chapter = 1
# if "selected_section" not in st.session_state:
#     st.session_state.selected_section = None

# # --- App Mode Switch ---
# mode = st.sidebar.radio("Choose a View", [
#     "📖 Explore Chapters",
#     "🙏 Life Help",
#     "🤖 Chat with Bheeshma"  # 👈 Add this here
# ])
# st.markdown("""
# <audio id="bg-chant" autoplay loop style="display:none">
#   <source src="https://raw.githubusercontent.com/saagarnkashyap/Bheeshma/main/OM%20Chanting%20%40417%20Hz%20_%20Removes%20All%20Negative%20Blocks%20%5B8sYK7lm3UKg_00_24_11_00_24_33_part%5D.mp3" type="audio/mpeg">
# </audio>

# <button onclick="fadeToggleChant()" style="
#   position: fixed;
#   bottom: 25px;
#   right: 25px;
#   background: radial-gradient(circle, #ffd700, #ff9900);
#   color: black;
#   padding: 12px 22px;
#   border-radius: 30px;
#   font-weight: bold;
#   border: none;
#   box-shadow: 0 0 15px gold;
#   z-index: 9999;
#   cursor: pointer;
#   font-size: 14px;
#   animation: pulse 2s infinite;
# ">🔊 Play Meditative Chant</button>

# <script>
#   const chant = document.getElementById('bg-chant');
#   let fading = false;
#   let isPlaying = true;

#   function fadeToggleChant() {
#     if (fading) return;
#     fading = true;

#     let volume = chant.volume;
#     let step = 0.05;

#     const fade = setInterval(() => {
#       if (isPlaying) {
#         volume -= step;
#         if (volume <= 0) {
#           chant.pause();
#           isPlaying = false;
#           clearInterval(fade);
#           fading = false;
#         }
#       } else {
#         if (chant.paused) chant.play();
#         volume += step;
#         if (volume >= 1) {
#           isPlaying = true;
#           clearInterval(fade);
#           fading = false;
#         }
#       }
#       chant.volume = Math.max(0, Math.min(1, volume));
#     }, 80);
#   }
# </script>

# <style>
# @keyframes pulse {
#   0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
#   70% { box-shadow: 0 0 0 20px rgba(255, 215, 0, 0); }
#   100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
# }
# </style>
# """, unsafe_allow_html=True)


# # ======================= 📖 EXPLORE CHAPTERS =======================
# def load_audio_map():
#     with open("gita_audio_links.json", "r", encoding="utf-8") as f:
#         return json.load(f)

# AUDIO_LINKS = load_audio_map()
# if mode == "📖 Explore Chapters":
#     st.title("Bheeshma - Your Bhagavad Gita Companion")

#     # --- Chapter Buttons ---
#     st.markdown("### 🕉️ Select a Chapter")
#     chapter_cols = st.columns(9)
#     for i in range(1, 19):
#         col = chapter_cols[(i - 1) % 9]
#         if col.button(f"{i}"):
#             st.session_state.selected_chapter = i
#             st.session_state.selected_section = None

#     chapter = next(c for c in chapters if c["number"] == st.session_state.selected_chapter)
#     st.markdown(f"## {chapter['number']}. {chapter['name']}")

#     # --- Bullet Subsection Nav ---
#     st.markdown("### 🔍 Explore Section")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button("• 📚 Philosophical Aspects"):
#             st.session_state.selected_section = "philosophical_aspects"

#     with col2:
#         if st.button("• 💠 Life Problems Addressed"):
#             st.session_state.selected_section = "life_problems_addressed"

#     with col3:
#         if st.button("• 🧘‍♂️ Yoga Type"):
#             st.session_state.selected_section = "yoga_type"

#     # --- Conditional Section Display ---
#     if st.session_state.selected_section == "philosophical_aspects":
#         st.markdown("#### 📚 Philosophical Aspects")
#         for p in chapter["philosophical_aspects"]:
#             st.markdown(f"- {p}")

#     elif st.session_state.selected_section == "life_problems_addressed":
#         st.markdown("#### 💠 Life Problems Addressed")
#         for lp in chapter["life_problems_addressed"]:
#             st.markdown(f"- {lp}")

#     elif st.session_state.selected_section == "yoga_type":
#         st.markdown("#### 🧘‍♂️ Yoga Type")
#         st.info(chapter["yoga_type"])

#     # --- Summary + Shlokas ---
#     st.markdown("#### 🧘 Chapter Summary")
#     st.markdown(chapter["summary"])

#     for shloka in chapter["shlokas"]:
#         with st.expander(f"Shloka {shloka['shloka_number']}"):
#             st.markdown("**📖 Sanskrit**")
#             st.markdown(f"<div class='shloka-sanskrit'>{shloka['sanskrit_text']}</div>", unsafe_allow_html=True)

#             st.markdown("**🔤 Transliteration**")
#             st.markdown(f"*{shloka['transliteration']}*")

#             st.markdown("**🔊 Audio Recitation**")

#                 # Construct URL: CHAP<chapter>/<sloka>-<sloka>.MP3
#             chapter_str = str(shloka["chapter"])
#             sloka_str = str(shloka["shloka_number"])
#             path = AUDIO_LINKS.get(chapter_str, {}).get(sloka_str)

#             if path:
#                 audio_url = f"https://www.gitasupersite.iitk.ac.in/sites/default/files/audio/{path}"
#                 try:
#                     r = requests.head(audio_url, timeout=5)
#                     if r.status_code == 200:
#                         st.audio(audio_url)
#                     else:
#                         raise Exception("Audio not available")
#                 except:
#                     st.warning("⚠️ Official audio not available. Using fallback voice.")
#                     try:
#                         tts = gTTS(text=shloka["sanskrit_text"], lang="hi", slow=True)
#                         audio_bytes = BytesIO()
#                         tts.write_to_fp(audio_bytes)
#                         audio_bytes.seek(0)
#                         st.audio(audio_bytes)
#                     except Exception as e:
#                         st.error(f"❌ Fallback audio failed: {e}")
#             else:
#                 st.warning("⚠️ Audio path not found in map.")          
                
#                 # tts = gTTS(text=shloka['sanskrit_text'], lang='hi', slow=True)
#                 # audio_bytes = BytesIO()
#                 # tts.write_to_fp(audio_bytes)
#                 # audio_bytes.seek(0)
#                 # st.audio(audio_bytes)



#             st.markdown("**🧠 Meaning**")
#             st.markdown(shloka["meaning"])
#             #---------this doesnt work... fix it later---------
#             # st.markdown("**🔊 Listen to Meaning**")
#             # def combine_and_speak(meaning, interpretation, application, lang="en"):
#             #     full_text = (
#             #             "Meaning: " + meaning + ". "
#             #         )
#             #     tts = gTTS(text=full_text, lang=lang, slow=False)
#             #     audio_bytes = BytesIO()
#             #     tts.write_to_fp(audio_bytes)
#             #     audio_bytes.seek(0)
#             #     return audio_bytes

#             # tts_audio = combine_and_speak(
#             #     shloka["meaning"],
#             #     shloka["interpretation"],
#             #     shloka["life_application"]
#             #     )
#             # st.audio(tts_audio, format="audio/mp3")

#             st.markdown("**💬 Interpretation**")
#             st.markdown(shloka["interpretation"])

#             st.markdown("**🌱 Life Application**")
#             st.markdown(shloka["life_application"])
            

    


# # ======================= 🙏 LIFE HELP =======================


# elif mode == "🙏 Life Help":
#     st.title("🙏 Life Help from the Bhagavad Gita")
#     st.markdown("Describe your challenge or emotion (e.g. `anger`, `guilt`, `sadness`, `loneliness`)")

#     user_input = st.text_input("What are you feeling?", "").strip().lower()

#     matched_key = None

#     if user_input:
#         # Step 1: check direct match
#         if user_input in problem_map:
#             matched_key = user_input

#         # Step 2: check alias match
#         elif user_input in keyword_aliases:
#             matched_key = keyword_aliases[user_input]

#         # Step 3: fuzzy match fallback
#         else:
#             all_keys = [key.replace("_", " ").lower() for key in problem_map.keys()]
#             match = difflib.get_close_matches(user_input, all_keys, n=1, cutoff=0.5)
#             if match:
#                 matched_key = next((key for key in problem_map if match[0] in key.replace("_", " ").lower()), None)

#         # --- Show matched verse content ---
#         if matched_key:
#             problem = problem_map[matched_key]
#             st.success(f"🧠 {problem['description']}")
#             st.markdown("#### 🔗 Relevant Shlokas")

#             for ref in problem["references"]:
#                 ch_num, sh_num = ref["chapter"], ref["shloka"]
#                 chapter = next((c for c in chapters if c["number"] == ch_num), None)
#                 if chapter:
#                     shloka = next((s for s in chapter["shlokas"] if s["shloka_number"] == sh_num), None)
#                     if shloka:
#                         with st.expander(f"Chapter {ch_num}, Shloka {sh_num}"):
#                             st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
#                             st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
#                             st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
#                             st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
#                             st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
#         else:
#             st.warning("🙏 Sorry, I couldn't find a matching emotion. Try keywords like `fear`, `guilt`, `jealousy`, `loneliness`, or `lust`.")


# # ======================= 🤖 CHATBOT MODE =======================

# # elif mode == "🤖 Chat with Bheeshma":
# #     import openai
# #     import os
# #     from dotenv import load_dotenv

# #     # Load environment variable
# #     load_dotenv()
# #     openai.api_key = os.getenv("OPENAI_API_KEY")

# #     st.title("🧠 Chat with Bheeshma")
# #     st.markdown("Ask about life, karma, fear, duty, or spiritual questions. Bheeshma will reply using the wisdom of the Bhagavad Gita.")

# #     # Initialize message history
# #     if "messages" not in st.session_state:
# #         st.session_state.messages = []

# #     # Display chat history
# #     for msg in st.session_state.messages:
# #         with st.chat_message(msg["role"]):
# #             st.markdown(msg["content"])

# #     # User input field
# #     if user_input := st.chat_input("What’s troubling you today, warrior?"):
# #         st.session_state.messages.append({"role": "user", "content": user_input})
# #         with st.chat_message("user"):
# #             st.markdown(user_input)

# #         with st.chat_message("assistant"):
# #             with st.spinner("Consulting the Gita..."):
# #                 try:
# #                     client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# #                     response = client.chat.completions.create(
# #                         model="gpt-3.5-turbo",
# #                         messages=[
# #                             {"role": "system", "content": 
# #                             "You are Bheeshma, a wise and spiritual guide from the Mahabharata. "
# #                             "You respond using the teachings of the Bhagavad Gita. "
# #                             "Cite shlokas with verse numbers when relevant. Speak with calm clarity, like a guru."},
# #                             *st.session_state.messages
# #                         ]
# #                     )
# #                     reply = response.choices[0].message.content
# #                     st.markdown(reply)
# #                     st.session_state.messages.append({"role": "assistant", "content": reply})
# #                 except Exception as e:
# #                     st.error(f"Failed to get response: {e}")



# # ======================= 🔍 SEARCH SHLOKAS =======================
# elif mode == "🔍 Search Shlokas":
#     st.title("🔍 Search Shlokas")
#     search_query = st.text_input("Search by keyword or type '2:47' to find a specific verse.")

#     if search_query:
#         if ":" in search_query:
#             # Format: chapter:verse (e.g. 2:47)
#             try:
#                 ch, sh = map(int, search_query.split(":"))
#                 chapter = next((c for c in chapters if c["number"] == ch), None)
#                 if chapter:
#                     shloka = next((s for s in chapter["shlokas"] if s["shloka_number"] == sh), None)
#                     if shloka:
#                         st.markdown(f"### Chapter {ch}, Shloka {sh}")
#                         st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
#                         st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
#                         st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
#                         st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
#                         st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
#                     else:
#                         st.error("Shloka not found.")
#                 else:
#                     st.error("Chapter not found.")
#             except ValueError:
#                 st.error("Invalid format. Use `chapter:verse`, e.g. `2:47`")
#         else:
#             st.markdown("### 🔎 Search Results")
#             results = []
#             for c in chapters:
#                 for s in c["shlokas"]:
#                     if search_query.lower() in s["sanskrit_text"].lower() \
#                     or search_query.lower() in s["transliteration"].lower() \
#                     or search_query.lower() in s["meaning"].lower() \
#                     or search_query.lower() in s["interpretation"].lower() \
#                     or search_query.lower() in s["life_application"].lower():
#                         results.append((c["number"], s))
#             if results:
#                 for ch_num, shloka in results:
#                     with st.expander(f"Chapter {ch_num}, Shloka {shloka['shloka_number']}"):
#                         st.markdown(f"**📖 Sanskrit**\n\n{shloka['sanskrit_text']}")
#                         st.markdown(f"**🔤 Transliteration**\n\n*{shloka['transliteration']}*")
#                         st.markdown(f"**🧠 Meaning**\n\n{shloka['meaning']}")
#                         st.markdown(f"**💬 Interpretation**\n\n{shloka['interpretation']}")
#                         st.markdown(f"**🌱 Life Application**\n\n{shloka['life_application']}")
#             else:
#                 st.info("No results found.")

# st.markdown(
#     """
#     <hr style="margin-top: 2rem; margin-bottom: 1rem;">
#     <div style="text-align: center; font-size: 0.9rem; color: gray;">
#         Made with 🕉️ by <strong>Saagar N Kashyap</strong>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

