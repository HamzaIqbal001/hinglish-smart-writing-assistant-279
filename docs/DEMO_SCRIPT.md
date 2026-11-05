# 🎙️ 2-Minute Screen-Recording Script
**Project**: Hinglish Smart Writing Assistant (CS3235 Mini Project #4)  
**Presenter**: Dipesh  
**Target Duration**: 120 seconds (2:00)

---

### [0:00 - 0:20] Introduction & Problem Setup
* **Screen**: Web browser opened at `http://localhost:7860`, showing the Hinglish Smart Writing Assistant Gradio UI with all boxes empty.
* **Action**: Move mouse smoothly over the header and pipeline description.
* **Spoken Script**:
  > *"Hello everyone. Welcome to the demonstration of the Hinglish Smart Writing Assistant, built for CS3235 Mini Project #4 in collaboration with AI4Bharat and BharatGen foundations.  
  > Across India, over 500 million bilingual users communicate in Hinglish—using the Roman alphabet to write Hindi phonetically. However, standard NLP tools struggle with irregular spellings, code-mixing, and informal slang. This project introduces a robust three-stage neural architecture that converts informal Hinglish into grammatically polished standard Hindi and high-quality English."*

---

### [0:20 - 0:50] Stage 1: Phonetic Transliteration (IndicXlit)
* **Screen**: Uncheck the *"Improve Phrasing"* and *"Translate to English"* checkboxes so only Stage 1 is active.
* **Action**: Type into the input box:
  `mujhe kal subah meeting ke liye jaana hai`  
  Click the **"🚀 Process Text"** button.
* **Result**:
  - Native Script: `मुझे कल सुबाह मीटिंग केई लिये जाना है`
* **Spoken Script**:
  > *"First, let's look at phonetic transliteration. Here, we disable improvement and translation to view raw script conversion. I type 'mujhe kal subah meeting ke liye jaana hai'.  
  > Powered by AI4Bharat's IndicXlit transformer engine, the system accurately maps phonetic Roman characters into Devanagari script in under 90 milliseconds. Notice how loanwords like 'meeting' are preserved, but typical phonetic typing introduces informal spelling artifacts like 'सुबाह' and 'केई लिये'."*

---

### [0:50 - 1:25] Stage 2 & 3: Phrasing Improvement & English Translation
* **Screen**: Turn both *"Improve Phrasing"* and *"Translate to English"* checkboxes back **ON**.
* **Action**: Click **"🚀 Process Text"** again.
* **Result**:
  - Native Script: `मुझे कल सुबाह मीटिंग केई लिये जाना है`
  - Improved Hindi: `मुझे कल सुबह बैठक के लिए जाना है।`
  - English Translation: `I have to go for the meeting tomorrow morning.`
* **Spoken Script**:
  > *"Now, let's activate the full generative pipeline. When we enable 'Improve Phrasing' and 'Translate to English' and process again, watch all three stages update simultaneously.  
  > In Stage 2, our language model rewrites the sentence: correcting the vowel lengthening in 'सुबाह' to standard 'सुबह', fixing postpositional syntax to 'के लिए', and elevating the English loanword 'मीटिंग' to formal Hindi 'बैठक'.  
  > In Stage 3, AI4Bharat's IndicTrans2 distilled 200M model translates the polished Hindi into fluent English: 'I have to go for the meeting tomorrow morning' in just 120 milliseconds."*

---

### [1:25 - 1:45] Code-Mixed & Colloquial Slang Example
* **Screen**: Click on Example 4 from the example tray below:  
  `tension mat lo sab jugaad ho jaayega`
* **Action**: Wait 1-2 seconds for automatic execution.
* **Result**:
  - Native Script: `टेंशन मत लो सब जुगाड़ हो जाएगा`
  - Improved Hindi: `चिंता मत कीजिए, सब प्रबंध हो जाएगा।`
  - English Translation: `Don't worry, everything will be managed.`
* **Spoken Script**:
  > *"Next, let's test colloquial slang and idiomatic expressions using the clickable examples. Clicking 'tension mat lo sab jugaad ho jaayega', the assistant transliterates the informal terms 'टेंशन' and 'जुगाड़', elevates them in clean Hindi to 'चिंता मत कीजिए, सब प्रबंध हो जाएगा', and translates to natural English: 'Don't worry, everything will be managed'."*

---

### [1:45 - 2:00] Evaluation Summary & Conclusion
* **Screen**: Open the evaluation chart screenshot (`docs/screenshots/05_eval_results.png`) or terminal showing `metrics.json`.
* **Action**: Highlight the metrics table.
* **Spoken Script**:
  > *"Our systematic benchmark across 40 test cases—including 30 sampled from the Aksharantar benchmark—achieves an end-to-end Devanagari Character Error Rate of just 5.1%, a transliteration accuracy of 50%, an English translation chrF score of 49.2 and BLEU of 29.0, and average processing latency under 1000 milliseconds for generative LLM improvement and ~100 milliseconds for translation on an RTX 4060 GPU.  
  > The code, automated evaluation scripts, and report are fully packaged and ready for reproduction. Thank you!"*
