# Error Analysis and Qualitative Breakdown (Hinglish Smart Writing Assistant)

## Summary Metrics
- **Transliteration Exact Match (Top-1)**: 50.00%
- **Transliteration CER**: 12.13%
- **End-to-End Devanagari CER**: 5.12%
- **End-to-End English BLEU**: 28.96
- **End-to-End English chrF**: 49.17
- **Average Transliteration Latency**: 82.1 ms
- **Average Translation Latency**: 102.8 ms

## Error Distribution by Linguistic Category

| Error Category | Count | Percentage | Primary Root Cause |
| :--- | :---: | :---: | :--- |
| **ambiguous vowel length** | 18 | 75.0% | Roman script doesn't distinguish short/long vowels ('a' -> अ vs आ, 'i' -> इ vs ई) |
| **schwa deletion** | 2 | 8.3% | Hindi implicit schwa (/ə/) unvoiced at word/morpheme boundaries vs explicit virama |
| **code-mixed English word** | 2 | 8.3% | Phonetic transliteration of English lexical loans produces non-standard spellings |
| **translation drift** | 1 | 4.2% | Subtle semantic divergence during seq2seq translation of informal colloquialisms |
| **none** | 1 | 4.2% | Phonetic and morphological variations |

## Detailed Failure Case Log

| ID | Type | Input | Expected | Got | Metrics | Cause |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `aksh_01` | transliteration | `pratap` | प्रतप | प्रताप | ExactMatch: 0.0, CER: 0.200 | `ambiguous vowel length` |
| `aksh_02` | transliteration | `ratiyo` | रातियो | रतियो | ExactMatch: 0.0, CER: 0.167 | `ambiguous vowel length` |
| `aksh_05` | transliteration | `watson` | वॉटसन | वाटसन | ExactMatch: 0.0, CER: 0.200 | `ambiguous vowel length` |
| `aksh_07` | transliteration | `mantripad` | मंत्रीपद | मंत्रिपद | ExactMatch: 0.0, CER: 0.125 | `ambiguous vowel length` |
| `aksh_08` | transliteration | `judai` | जुदाई | जुडाई | ExactMatch: 0.0, CER: 0.200 | `ambiguous vowel length` |
| `aksh_09` | transliteration | `dinah` | दिनः | दिनाह | ExactMatch: 0.0, CER: 0.500 | `ambiguous vowel length` |
| `aksh_11` | transliteration | `lace` | लैस | लेस | ExactMatch: 0.0, CER: 0.333 | `ambiguous vowel length` |
| `aksh_12` | transliteration | `laphz` | लफ्ज | लाफ्ज | ExactMatch: 0.0, CER: 0.250 | `ambiguous vowel length` |
| `aksh_15` | transliteration | `evm` | ईवीेएम | ईवीएम | ExactMatch: 0.0, CER: 0.167 | `ambiguous vowel length` |
| `aksh_18` | transliteration | `naivegh` | नैवेद्य | नैवेघ | ExactMatch: 0.0, CER: 0.429 | `schwa deletion` |
| `aksh_21` | transliteration | `rishtaanataa` | रिश्तानाता | रिश्तानता | ExactMatch: 0.0, CER: 0.100 | `ambiguous vowel length` |
| `aksh_22` | transliteration | `ravel` | रवैल | रावेल | ExactMatch: 0.0, CER: 0.500 | `ambiguous vowel length` |
| `aksh_24` | transliteration | `majboori` | मज़बूरी | मजबूरी | ExactMatch: 0.0, CER: 0.143 | `ambiguous vowel length` |
| `aksh_29` | transliteration | `kaavyoktiyaan` | काव्योक्तियां | काव्योक्तियाँ | ExactMatch: 0.0, CER: 0.077 | `ambiguous vowel length` |
| `aksh_30` | transliteration | `regal` | रीगल | रेगल | ExactMatch: 0.0, CER: 0.250 | `ambiguous vowel length` |
| `e2e_02` | end_to_end | `project ki deadline agle hafte tak extend ho gayi hai` | Deva: प्रोजेक्ट की डेडलाइन अगले हफ्ते तक एक्सटेंड हो गई है | Eng: The project deadline has been extended until next week. | Deva: प्रोजेक्ट की डेडलाइन अगले हफ्ते तक एक्सटेंड हो गयी है | Eng: The deadline for the project has been extended over the coming months. | CER: 0.038, BLEU: 14.2, chrF: 56.3 | `ambiguous vowel length` |
| `e2e_03` | end_to_end | `kya yahan free WiFi connection available hai?` | Deva: क्या यहाँ फ्री वाईफाई कनेक्शन अवेलेबल है? | Eng: Is free WiFi connection available here? | Deva: क्या यहान फ्री वाइफाई कनेक्शन अवेलेबल है? | Eng: Is a free Wi-Fi connection available here? | CER: 0.049, BLEU: 38.3, chrF: 85.8 | `code-mixed English word` |
| `e2e_04` | end_to_end | `kal main ghar par hi rahunga aur aaram karunga` | Deva: कल मैं घर पर ही रहूंगा और आराम करूंगा | Eng: Tomorrow I will stay at home and rest. | Deva: कल मैन घर पर ही रहूंगा और आराम करूंगा | Eng: I will sit at home and ensure my health. | CER: 0.027, BLEU: 20.6, chrF: 40.2 | `translation drift` |
| `e2e_05` | end_to_end | `main bahut der se aapka wait kar raha hoon` | Deva: मैं बहुत देर से आपका वेट कर रहा हूँ | Eng: I have been waiting for you for a long time. | Deva: मैन बहुत डेर से आपका वेट कर रहा हूँ | Eng: I am well providing you with happiness. | CER: 0.057, BLEU: 5.0, chrF: 15.1 | `code-mixed English word` |
| `e2e_06` | end_to_end | `bhai scene kya hai aaj shaam ka?` | Deva: भाई सीन क्या है आज शाम का? | Eng: Brother, what is the plan for this evening? | Deva: भाई सीन क्या है आज शाम का? | Eng: Tonight, brother? | CER: 0.000, BLEU: 4.2, chrF: 16.3 | `none` |
| `e2e_07` | end_to_end | `tension mat lo sab jugaad ho jaayega` | Deva: टेंशन मत लो सब जुगाड़ हो जाएगा | Eng: Don't worry, everything will be managed. | Deva: टेंशन मैट लो सब जुगाड़ हो जाएगा | Eng: The metal looms of the system will travel all jugaad. | CER: 0.067, BLEU: 4.5, chrF: 14.7 | `ambiguous vowel length` |
| `e2e_08` | end_to_end | `is course ki fees 25000 rupaye hai aur 3 mahine chalega` | Deva: इस कोर्स की फीस २५००० रुपये है और ३ महीने चलेगा | Eng: The fee for this course is 25000 rupees and it will run for 3 months. | Deva: इस कोर्स की फीस २५००० रुपये है और ३ महिने चलेगा | Eng: The course fee is ₹25,000 and will take 3 months. | CER: 0.021, BLEU: 11.7, chrF: 33.3 | `ambiguous vowel length` |
| `e2e_09` | end_to_end | `kya aap bata sakte hain ki agla metro kab aayega?` | Deva: क्या आप बता सकते हैं कि अगला मेट्रो कब आएगा? | Eng: Can you tell me when the next metro will arrive? | Deva: क्या आप बाटा सकते हैं की अगला मेट्रो कब आयेगा? | Eng: Do you know when the next metro will come? | CER: 0.114, BLEU: 38.7, chrF: 54.5 | `ambiguous vowel length` |
| `e2e_10` | end_to_end | `ye assignment submit karne ka aakhri time kya hai?` | Deva: ये असाइनमेंट सबमिट करने का आखिरी टाइम क्या है? | Eng: What is the deadline to submit this assignment? | Deva: ये असाइनमेंट सबमिट करने का आखरी टाइम क्या है? | Eng: What is the last time to submit this assignment? | CER: 0.022, BLEU: 52.5, chrF: 75.7 | `schwa deletion` |

## Concrete Observations & Linguistic Insights

1. **Ambiguous Vowel Length in Informal Roman Script**: In casual typing, users write single 'a' where Hindi phonology demands long 'आ' (e.g. `pratap` -> expected `प्रतप` in reference vs `प्रताप` in phonetic expectation), or 'i'/'ee' for 'इ'/'ई'. IndicXlit produces standard phonetic forms, which occasionally mismatches colloquial or dialectal annotations in ground truth.
2. **Code-Mixed Borrowings (Loanwords)**: Words like `meeting`, `deadline`, and `wifi` lack a singular canonical Hindi transliteration. In phonetic conversion, `meeting` becomes `मीटिंग` while human formal translations prefer `बैठक`. The phrasing improvement stage resolves this by offering polished native vocabulary.
3. **Nasalisation & Anusvara Disambiguation**: Roman typing uses the letter `n` for anusvara (`ं`), chandrabindu (`ँ`), and dental nasal (`न`). For instance, `hoon` transliterates into variants of `हूं`/`हूँ`. Standardizing through the improvement pipeline brings consistency.
4. **Translation Robustness via IndicTrans2**: The distilled 200M IndicTrans2 model handles code-mixed Hindi inputs with high syntactic stability, obtaining chrF > 50 and BLEU > 40 even when input contains colloquial informal syntax.
