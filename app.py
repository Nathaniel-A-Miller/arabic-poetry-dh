import streamlit as st
from collections import Counter
import re
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Empirical Arabic Vocabulary Explorer")

# 1. ACTUAL RAW STRINGS (Mirroring notebook data content)
raw_texts = {
    "Abu Nuwas": """دَعْ عَنْكَ لَوْمِي فَإِنَّ اللَّوْمَ إِغْرَاءُ وَدَاوِنِي بِالَّتِي كَانَتْ هِيَ الدَّاءُ صَفْرَاءُ لا تَنْزِلُ الأَحْزَانُ سَاحَتَهَا لَوْ مَسَّهَا حَجَرٌ مَسَّتْهُ سَرَّاءُ قَامَتْ بِأَبْرِيقِهَا وَاللَّيْلُ مُعْتَكِرٌ فَلَاحَ مِنْ وَجْهِهَا فِي الْبَيْتِ لَأْلَاءُ فَأَرْسَلَتْ مِنْ فَمِ الإِبْرِيقِ صَافِيَةً كَأَنَّمَا أَخْذُهَا بِالْعَيْنِ إِغْفَاءُ""",
    "Abu al-Atahiyah": """نَبْكِي عَلَى الدُّنْيَا وَمَا مِنْ مَعْشَرٍ جَمَعَتْهُمُ الدُّنْيَا فَلَمْ يَتَفَرَّقُوا أَيْنَ المُلُوكُ الَّتِي عَنْ حَظِّهَا غَفَلَتْ حَتَّى سَقَاهَا بِكَأْسِ المَوْتِ سَاقِيهَا تَبْكِي عِظَامِي حَذَارِ المَوْتِ فِي جَزَعٍ وَالْمَوْتُ نَازِلٌ بِالنَّفْسِ دَانِيهَا لِكُلِّ نَفْسٍ وَإِنْ عِاشَتْ عَلَى مَهَلٍ مِنَ المَنِيَّةِ يَوْمٌ لَيْسَ يُخْطِيهَا وَاللَّه يَعْلَمُ أَنَّ النَّفْسَ هَالِكَةٌ"""
}

# Standardized baseline stop words matching the notebook
AR_STOP_WORDS = {
    "من", "في", "على", "إلى", "عن", "مع", "هذا", "هذه", "التي", "الذي", 
    "ان", "أن", "لا", "ما", "يا", "و", "ف", "ب", "ل", "ثم", "أو", "كان", "كانت"
}

# 2. LIGATURE-SAFE ARABIC FONT CONFIGURATION
safe_config = {
    'delete_harakat': True,
    'support_ligatures': False
}
safe_reshaper = ArabicReshaper(configuration=safe_config)

def fix_arabic_text(text):
    return get_display(safe_reshaper.reshape(text))

# 3. THE REFACTORED CLEANING ENGINE
def build_frequency_distribution(raw_text, filter_stops):
    # Strip tatweel/kashida and harakat (diacritics)
    sanitized = re.sub(r'[\u064B-\u0652\u0640]', '', raw_text)
    
    # Tokenize: Explicitly extract Arabic script clusters (Matches Notebook Fix)
    words = re.findall(r'[\u0621-\u064A]+', sanitized)
    
    if filter_stops:
        # Exclude particles and single-letter orphan characters
        words = [w for w in words if w not in AR_STOP_WORDS and len(w) > 1]
        
    return Counter(words)

# 4. SIDEBAR CONTROL WIDGETS
st.sidebar.header("Analysis Parameters")
filter_stops = st.sidebar.checkbox("Apply Metaobject Filter: Exclude Stop Words", value=True)
top_n = st.sidebar.slider("Number of high-frequency words", min_value=3, max_value=10, value=5)
selected_poet = st.sidebar.selectbox("Select Poet Corpus", ["Abu Nuwas", "Abu al-Atahiyah"])

# Calculate frequencies on the fly
fd_counts = build_frequency_distribution(raw_texts[selected_poet], filter_stops)
top_items = fd_counts.most_common(top_n)

# 5. USER INTERFACE DISPLAY LAYER
if not top_items:
    st.warning("No structural text tokens found matching the current criteria configuration.")
else:
    words, counts = zip(*top_items)
    reshaped_labels = [fix_arabic_text(w) for w in words]

    st.subheader(f"Dynamic Unigram Frequency Distribution: {selected_poet}")
    
    # Display the raw data matrix directly to the reader
    st.dataframe([{"Token": w, "Absolute Count": c} for w, c in top_items], use_container_width=True)

    # Render Matplotlib Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(reshaped_labels, counts, color="maroon" if selected_poet == "Abu Nuwas" else "teal")
    
    # Apply ligature-safe labels to chart components
    ax.set_title(fix_arabic_text(f"Top Vocabulary Signature: {selected_poet}"), fontsize=14)
    ax.set_ylabel(fix_arabic_text("التكرار"), fontsize=12)
    
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    st.pyplot(fig)
