import streamlit as st
from bidi.algorithm import get_display
import arabic_reshaper
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Classical Arabic Digital Metaobject Explorer")

st.markdown("""
### Chapter Interactive Lab: Khamriyyāt vs. Zuhdiyyāt
Adjust the metadata filters below to see how removing stop words changes the analytical outcome.
""")

# Mock data matrix representing the backend state
data = {
    "Abu Nuwas": {"خمر": 15, "كأس": 12, "الموت": 1, "الدنيا": 3, "من": 45, "في": 38},
    "Abu al-Atahiyah": {"خمر": 0, "كأس": 1, "الموت": 20, "الدنيا": 18, "من": 52, "في": 41}
}

# 1. UI Control Widgets
exclude_stop = st.checkbox("Apply Metaobject Filter: Exclude Stop Words ('من', 'في')", value=True)
poet_selection = st.multiselect("Select Authors to Compare:", ["Abu Nuwas", "Abu al-Atahiyah"], default=["Abu Nuwas", "Abu al-Atahiyah"])

# 2. Process Data dynamically based on widget selections
words_to_plot = ["خمر", "كأس", "الموت", "الدنيا"] if exclude_stop else ["خمر", "كأس", "الموت", "الدنيا", "من", "في"]
reshaped_labels = [get_display(arabic_reshaper.reshape(w)) for w in words_to_plot]

fig, ax = plt.subplots(figsize=(8, 4))
x = range(len(words_to_plot))

# 3. Dynamic Rendering Loop
if "Abu Nuwas" in poet_selection:
    counts = [data["Abu Nuwas"].get(w, 0) for w in words_to_plot]
    ax.bar([i - 0.2 for i in x], counts, width=0.4, label="Abu Nuwas", color="maroon")
if "Abu al-Atahiyah" in poet_selection:
    counts = [data["Abu al-Atahiyah"].get(w, 0) for w in words_to_plot]
    ax.bar([i + 0.2 for i in x], counts, width=0.4, label="Abu al-Atahiyah", color="teal")

ax.set_xticks(x)
ax.set_xticklabels(reshaped_labels, fontsize=12)
ax.set_ylabel("Frequencies")
ax.legend()

st.pyplot(fig)
