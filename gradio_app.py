import gradio as gr
from bot_brain import analyze_image, medical_reasoning
from user_voice import transcribe_with_whisper
from bot_voice import speak_text


def process_inputs(image, audio, text):
    user_text = text

    # 🎙️ Voice input handling
    if audio:
        user_text = transcribe_with_whisper(audio)

    # 🖼️ Image analysis
    image_caption = None
    if image:
        image_caption = analyze_image(image)

    # 🧠 Medical reasoning
    response = medical_reasoning(user_text, image_caption)

    # 🔊 Voice narration (multilingual + pauses handled inside speak_text)
    voice_path = speak_text(response)

    return response, voice_path


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Image(type="filepath", label="Upload Medical Image"),
        gr.Audio(type="filepath", label="Speak (Optional)"),
        gr.Textbox(
            label="Describe your issue",
            lines=4,
            placeholder="Example: I have a cut on my finger and it is bleeding"
        )
    ],
    outputs=[
        gr.Textbox(
            label="🩺 Doctor Response",
            lines=16,
            max_lines=30
        ),
        gr.Audio(
            label="🔊 Doctor Voice Response",
            autoplay=True
        )
    ],
    title="AidBot – Medical Assistant",
    description="Preliminary medical guidance with multilingual voice narration"
)

iface.launch()
