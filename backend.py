from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def generate_image(prompt: str) -> Image.Image:
    # Charger le pipeline Stable Diffusion

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        use_auth_token=HF_TOKEN,
        torch_dtype=torch.float16
    )
    
    # Utiliser GPU si disponible
    pipe = pipe.to("cuda") if torch.cuda.is_available() else pipe.to("cpu")
    
    # Générer l'image
    image = pipe(prompt).images[0]
    
    return image


# Exemple d'utilisation
if __name__ == "__main__":
    image = generate_image("un coucher de soleil magnifique sur la montagne")
    image.save("generated_image.png")
    print("Image générée avec succès!")