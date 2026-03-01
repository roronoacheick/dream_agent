import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image

load_dotenv()

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"

def generate_image(dream_text: str, model_id: str = DEFAULT_MODEL) -> Image.Image:
    
    dream_text = dream_text.strip()
    if not dream_text:
        raise ValueError("La description ne peut pas être vide.")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("Token HF_TOKEN manquant dans .env")

    # Utiliser l'API Hugging Face Inference
    client = InferenceClient(token=token)
    image = client.text_to_image(dream_text, model=model_id)
    
    return image


if __name__ == "__main__":
    image = generate_image("un coucher de soleil magnifique sur la montagne")
    image.save("generated_image.png")
    print("Image générée avec succès!")