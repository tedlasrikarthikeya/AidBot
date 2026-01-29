import pyttsx3
import tempfile
import os
import re

# Initialize TTS engine once
engine = pyttsx3.init()

# Slightly slower, doctor-like speech
engine.setProperty("rate", 155)
engine.setProperty("volume", 1.0)


def set_language_voice(language="en"):
    """
    Tries to select a voice matching the requested language.
    Falls back safely if not found.
    """
    voices = engine.getProperty("voices")

    for voice in voices:
        voice_id = voice.id.lower()
        voice_name = voice.name.lower()

        if language == "en" and ("english" in voice_name or "en_" in voice_id):
            engine.setProperty("voice", voice.id)
            return

        if language == "hi" and ("hindi" in voice_name or "hi_" in voice_id):
            engine.setProperty("voice", voice.id)
            return

        if language == "es" and ("spanish" in voice_name or "es_" in voice_id):
            engine.setProperty("voice", voice.id)
            return

    # fallback: keep default voice
    return


def add_natural_pauses(text):
    """
    Adds pauses after medical sections and sentences
    """
    text = re.sub(r"\.\s+", ".\n", text)
    text = re.sub(r"(First Aid|Immediate Care|Warning Signs|Precautions)", r"\n\1:\n", text)
    return text


def speak_text(text, language="en"):
    if not text or len(text.strip()) < 5:
        return None

    # Select language voice if available
    set_language_voice(language)

    # Add pauses for natural narration
    text = add_natural_pauses(text)

    # Create temp audio file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio.close()

    engine.save_to_file(text, temp_audio.name)
    engine.runAndWait()

    return temp_audio.name
