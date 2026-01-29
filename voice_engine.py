from gtts import gTTS
from langdetect import detect
import os
import time
from playsound import playsound

def speak_medical_response(text):
    if not text or len(text.strip()) < 5:
        return None

    # 🌍 Detect language automatically
    try:
        lang = detect(text)
    except:
        lang = "en"

    # 🎧 Supported languages mapping
    supported_langs = {
        "en": "en",
        "hi": "hi",
        "te": "te",
        "ta": "ta",
        "fr": "fr",
        "es": "es"
    }

    lang = supported_langs.get(lang, "en")

    # 🧩 Split text for pauses
    sections = text.split("\n")

    audio_files = []
    for i, section in enumerate(sections):
        if len(section.strip()) < 3:
            continue

        tts = gTTS(text=section, lang=lang, slow=False)
        filename = f"voice_part_{i}.mp3"
        tts.save(filename)
        audio_files.append(filename)

    # 🔊 Play with pauses
    for audio in audio_files:
        playsound(audio)
        time.sleep(0.8)  # pause between sections
        os.remove(audio)

    return "Voice played successfully"
