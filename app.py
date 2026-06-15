from collections import Counter
import re

# Simulated OpenITI file data input
raw_data_stream = """
دَعْ عَنْكَ لَوْمِي فَإِنَّ اللَّوْمَ إِغْرَاءُ وَدَاوِنِي بِالَّتِي كَانَتْ هِيَ الدَّاءُ
صَفْرَاءُ لا تَنْزِلُ الأَحْزَانُ سَاحَتَهَا لَوْ مَسَّهَا حَجَرٌ مَسَّتْهُ سَرَّاءُ
"""

# Clean
text_no_tashkil = re.sub(r"[\u064B-\u0652]", "", raw_data_stream)
all_tokens = re.findall(r"\b\w+\b", text_no_tashkil)

# 1. Build a completely un-curated, raw frequency glossary
raw_glossary = Counter(all_tokens)
print("--- TRUE ABSOLUTE TOP WORDS (Including Grammar) ---")
for word, count in raw_glossary.most_common(5):
    print(f"Word: {word} | Occurrences: {count}")

# 2. Apply a standard stop-word exclusion mask
STOP_WORDS = {"من", "في", "على", "إلى", "و", "أن", "إن", "لا"}
filtered_tokens = [w for w in all_tokens if w not in STOP_WORDS]

filtered_glossary = Counter(filtered_tokens)
print("\n--- TRUE TOP WORDS (Stop Words Filtered Out) ---")
for word, count in filtered_glossary.most_common(5):
    print(f"Word: {word} | Occurrences: {count}")
