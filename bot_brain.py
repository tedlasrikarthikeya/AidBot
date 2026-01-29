from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    AutoTokenizer,
    AutoModelForCausalLM
)
from PIL import Image
import torch

# ---------- IMAGE MODEL ----------
image_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
image_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
image_model.eval()

# ---------- TEXT MODEL ----------
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct"
)
llm = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    device_map="cpu"
)

# ---------- IMAGE ANALYSIS ----------
def analyze_image(image):
    if image is None:
        return None

    if isinstance(image, str):
        image = Image.open(image).convert("RGB")
    else:
        image = Image.fromarray(image).convert("RGB")

    inputs = image_processor(image, return_tensors="pt")

    with torch.no_grad():
        out = image_model.generate(**inputs, max_new_tokens=40)

    caption = image_processor.decode(out[0], skip_special_tokens=True)

    # filter bad captions
    if not caption or len(caption.split()) < 4 or "ac ac" in caption.lower():
        return None

    return caption


# ---------- MEDICAL REASONING ----------
def medical_reasoning(user_text, image_caption=None):
    context = f"Patient complaint: {user_text}. "
    if image_caption:
        context += f"Visual observation: {image_caption}. "

    system_prompt = (
    "You are an experienced medical doctor giving preliminary advice. "
    "First identify the likely type of problem such as injury, skin, dental, or internal. "
    "Explain what might be happening in simple terms. "
    "Give immediate first aid or home care steps. "
    "Mention warning signs that require medical attention. "
    "End with preventive measures and a calm closing sentence. "
    "Do not mention prompts or AI. Do not give a definite diagnosis."
    )


    prompt = f"""{system_prompt}
    Patient details: 
    {context}
    Respond strictly in this format:

    1. Initial Assessment
    2. Immediate First Aid
    3. Home Care Steps
    4. Warning Signs (when to see a doctor)
    5. Preventive Measures
    6. Reassurance

    Response:
    """

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm.generate(
        **inputs,
        max_new_tokens=420,
        temperature=0.6,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("Response:")[-1].strip()
