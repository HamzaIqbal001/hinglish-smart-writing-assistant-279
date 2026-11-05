"""
Build evaluation dataset for Hinglish Smart Writing Assistant.
Generates exactly 40 test cases:
- 30 transliteration word pairs sampled from Aksharantar Hindi test split (seed 42)
- 10 hand-crafted end-to-end sentences covering code-mixing, slang, ambiguous spellings, numbers, questions.
"""

import json
import random
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AKSHARANTAR_JSON = DATA_DIR / "aksharantar" / "hin_test.json"
OUTPUT_CSV = DATA_DIR / "testcases.csv"

E2E_CASES = [
    {
        "id": "e2e_01",
        "type": "end_to_end",
        "input": "mujhe kal subah meeting ke liye jaana hai",
        "ref_transliteration": "मुझे कल सुबह मीटिंग के लिए जाना है",
        "ref_improved": "मुझे कल सुबह बैठक के लिए जाना है।",
        "ref_translation": "I have to go for the meeting tomorrow morning.",
        "category": "code_mixed_meeting"
    },
    {
        "id": "e2e_02",
        "type": "end_to_end",
        "input": "project ki deadline agle hafte tak extend ho gayi hai",
        "ref_transliteration": "प्रोजेक्ट की डेडलाइन अगले हफ्ते तक एक्सटेंड हो गई है",
        "ref_improved": "परियोजना की अंतिम तिथि अगले सप्ताह तक बढ़ा दी गई है।",
        "ref_translation": "The project deadline has been extended until next week.",
        "category": "code_mixed_deadline"
    },
    {
        "id": "e2e_03",
        "type": "end_to_end",
        "input": "kya yahan free WiFi connection available hai?",
        "ref_transliteration": "क्या यहाँ फ्री वाईफाई कनेक्शन अवेलेबल है?",
        "ref_improved": "क्या यहाँ मुफ्त वाई-फाई कनेक्शन उपलब्ध है?",
        "ref_translation": "Is free WiFi connection available here?",
        "category": "code_mixed_wifi"
    },
    {
        "id": "e2e_04",
        "type": "end_to_end",
        "input": "kal main ghar par hi rahunga aur aaram karunga",
        "ref_transliteration": "कल मैं घर पर ही रहूंगा और आराम करूंगा",
        "ref_improved": "कल मैं घर पर ही रहकर विश्राम करूँगा।",
        "ref_translation": "Tomorrow I will stay at home and rest.",
        "category": "ambiguous_spelling_kal"
    },
    {
        "id": "e2e_05",
        "type": "end_to_end",
        "input": "main bahut der se aapka wait kar raha hoon",
        "ref_transliteration": "मैं बहुत देर से आपका वेट कर रहा हूँ",
        "ref_improved": "मैं काफी देर से आपकी प्रतीक्षा कर रहा हूँ।",
        "ref_translation": "I have been waiting for you for a long time.",
        "category": "ambiguous_spelling_hoon"
    },
    {
        "id": "e2e_06",
        "type": "end_to_end",
        "input": "bhai scene kya hai aaj shaam ka?",
        "ref_transliteration": "भाई सीन क्या है आज शाम का?",
        "ref_improved": "मित्र, आज शाम की क्या योजना है?",
        "ref_translation": "Brother, what is the plan for this evening?",
        "category": "casual_slang_scene"
    },
    {
        "id": "e2e_07",
        "type": "end_to_end",
        "input": "tension mat lo sab jugaad ho jaayega",
        "ref_transliteration": "टेंशन मत लो सब जुगाड़ हो जाएगा",
        "ref_improved": "चिंता मत कीजिए, सब प्रबंध हो जाएगा।",
        "ref_translation": "Don't worry, everything will be managed.",
        "category": "casual_slang_jugaad"
    },
    {
        "id": "e2e_08",
        "type": "end_to_end",
        "input": "is course ki fees 25000 rupaye hai aur 3 mahine chalega",
        "ref_transliteration": "इस कोर्स की फीस २५००० रुपये है और ३ महीने चलेगा",
        "ref_improved": "इस पाठ्यक्रम का शुल्क २५००० रुपये है और यह ३ महीने चलेगा।",
        "ref_translation": "The fee for this course is 25000 rupees and it will run for 3 months.",
        "category": "numbers_and_quantities"
    },
    {
        "id": "e2e_09",
        "type": "end_to_end",
        "input": "kya aap bata sakte hain ki agla metro kab aayega?",
        "ref_transliteration": "क्या आप बता सकते हैं कि अगला मेट्रो कब आएगा?",
        "ref_improved": "क्या आप बता सकते हैं कि अगली मेट्रो रेल कब आएगी?",
        "ref_translation": "Can you tell me when the next metro will arrive?",
        "category": "question_inquiry"
    },
    {
        "id": "e2e_10",
        "type": "end_to_end",
        "input": "ye assignment submit karne ka aakhri time kya hai?",
        "ref_transliteration": "ये असाइनमेंट सबमिट करने का आखिरी टाइम क्या है?",
        "ref_improved": "यह सत्रीय कार्य जमा करने का अंतिम समय क्या है?",
        "ref_translation": "What is the deadline to submit this assignment?",
        "category": "question_academic"
    }
]

def load_aksharantar_samples(json_path: Path, n: int = 30, seed: int = 42):
    records = []
    with open(json_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    random.seed(seed)
    sampled = random.sample(records, n)
    
    cases = []
    for idx, item in enumerate(sampled, start=1):
        cases.append({
            "id": f"aksh_{idx:02d}",
            "type": "transliteration",
            "input": item["english word"],
            "ref_transliteration": item["native word"],
            "ref_improved": "",
            "ref_translation": "",
            "category": "aksharantar_word"
        })
    return cases

def build_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    aksh_cases = load_aksharantar_samples(AKSHARANTAR_JSON, n=30, seed=42)
    all_cases = aksh_cases + E2E_CASES

    fieldnames = ["id", "type", "input", "ref_transliteration", "ref_improved", "ref_translation", "category"]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_cases)

    print(f"Successfully generated {len(all_cases)} test cases at {OUTPUT_CSV}")

if __name__ == "__main__":
    build_dataset()
