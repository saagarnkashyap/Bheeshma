import streamlit as st
import json
import difflib
import re
from gtts import gTTS
import requests
from io import BytesIO
import io


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
mode = st.sidebar.radio("Choose a View", ["📖 Explore Chapters", "🙏 Life Help", "🔍 Search Shlokas"])

# ======================= 📖 EXPLORE CHAPTERS =======================
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
            st.markdown(f"**{shloka['sanskrit_text']}**")

            # 🔊 Gita Supersite playback
            audio_url = f"https://www.gitasupersite.iitk.ac.in/static/audio/{shloka['chapter']}/{shloka['shloka_number']}.mp3"
            st.markdown("**🔊 Gita Supersite Recitation**")
            
            try:
                # Check if audio URL is accessible
                response = requests.head(audio_url)
                if response.status_code == 200:
                    st.audio(audio_url)
                else:
                    raise Exception("Supersite audio not available")

            except Exception:
                st.warning("⚠️ Official audio not available. Using fallback voice.")
                tts = gTTS(text=shloka['sanskrit_text'], lang='hi', slow=True)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes)

            st.markdown("**🔤 Transliteration**")
            st.markdown(f"*{shloka['transliteration']}*")

            st.markdown("**🧠 Meaning**")
            st.markdown(shloka["meaning"])

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

