import os
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
import math
import numpy as np
import imageio
import tempfile

load_dotenv()

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
PROMPTS_DIR = Path("prompts")


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def generate_image(dream_text: str, model_id: str = DEFAULT_MODEL) -> Image.Image:
   
    dream_text = dream_text.strip()
    if not dream_text:
        raise ValueError("La description ne peut pas être vide.")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("Token HF_TOKEN manquant dans .env")

    # Charger le template de couverture
    cover_template = load_file(PROMPTS_DIR / "cover_template.txt")
    
    enhanced_prompt = cover_template.format(dream_text=dream_text)
    
    client = InferenceClient(token=token)
    image = client.text_to_image(enhanced_prompt, model=model_id)
    
    return image


def generate_video(dream_text: str) -> bytes:
   
    dream_text = dream_text.strip()
    if not dream_text:
        raise ValueError("La description ne peut pas être vide.")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("Token HF_TOKEN manquant dans .env")

    # Charger le template de couverture
    cover_template = load_file(PROMPTS_DIR / "cover_template.txt")
    enhanced_prompt = cover_template.format(dream_text=dream_text)
    
    try:
        client = InferenceClient(token=token)
        
        print("🎬 Génération de la vidéo...")
        
        video_bytes = client.text_to_video(
            enhanced_prompt,
            model="damo-vilab/text-to-video-ms-1.7b"
        )
        
        return video_bytes
        
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la génération vidéo HF: {str(e)}")


def generate_video_immersive(dream_text: str) -> bytes:
    """
    Génère une vidéo immersive en boucle avec animation fluide.
    Crée une base d'image statique avec des animations de zoom/rotation.
    """
    dream_text = dream_text.strip()
    if not dream_text:
        raise ValueError("La description ne peut pas être vide.")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("Token HF_TOKEN manquant dans .env")

    try:
        print("🎬 Génération de la vidéo immersive...")
        
        # 1️⃣ Générer l'image de base
        print("   📸 Création de l'image de base...")
        base_image = generate_image(dream_text)
        
        # 2️⃣ Créer l'animation en boucle avec des frames (150 frames = 5 secondes à 30 fps)
        print("   🎞️ Création des frames animées...")
        frames = create_looping_animation(base_image, num_frames=150, zoom_speed=1.02)
        
        # 3️⃣ Convertir les frames en vidéo MP4
        print("   📹 Encodage en vidéo MP4...")
        video_bytes = frames_to_video(frames, fps=30)
        
        print("✅ Vidéo immersive générée !")
        return video_bytes
        
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la génération vidéo immersive: {str(e)}")


def create_looping_animation(base_image: Image.Image, num_frames: int = 150) -> list:
    """
    Crée une animation fluide avec un effet de zoom qui va et vient.
    
    Args:
        base_image: L'image de départ
        num_frames: Nombre de frames (150 = 5 secondes à 30fps)
    
    Returns:
        Une liste de frames (images PIL)
    """
    frames = []
    width, height = base_image.size
    center_x, center_y = width // 2, height // 2
    
    for i in range(num_frames):
        # Calcul du zoom oscillant (va et vient)
        # sin() crée une onde entre -1 et 1
        progress = i / num_frames
        zoom_factor = 1.0 + 0.15 * (0.5 * (1 + math.sin(progress * 6.28)))
        
        # Calcul de la région à "cropper" (découper)
        new_width = int(width / zoom_factor)
        new_height = int(height / zoom_factor)
        
        # Découpe centrée
        left = center_x - new_width // 2
        top = center_y - new_height // 2
        right = left + new_width
        bottom = top + new_height
        
        # Découper et redimensionner l'image
        cropped = base_image.crop((left, top, right, bottom))
        frame = cropped.resize((width, height), Image.Resampling.LANCZOS)
        
        frames.append(frame)
    
    return frames


def frames_to_video(frames: list, fps: int = 30) -> bytes:
    """
    Convertit une liste de frames (images PIL) en vidéo MP4.
    
    Args:
        frames: Liste des images PIL à convertir
        fps: Images par seconde (30 fps = standard)
    
    Returns:
        Les données vidéo en bytes (prêtes à être lues par Streamlit)
    """
    # Créer un dossier temporaire pour la vidéo
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_video = os.path.join(tmp_dir, "output.mp4")
        
        # Convertir les images PIL en tableaux numpy (format que imageio comprend)
        frame_arrays = []
        for frame in frames:
            # PIL Image → RGB → numpy array
            array = np.array(frame.convert('RGB'))
            frame_arrays.append(array)
        
        # Sauvegarder les frames comme vidéo MP4
        imageio.mimsave(output_video, frame_arrays, fps=fps)
        
        # Lire la vidéo depuis le fichier et la retourner
        with open(output_video, 'rb') as f:
            video_bytes = f.read()
        
        return video_bytes


if __name__ == "__main__":
    image = generate_image("un coucher de soleil magnifique sur la montagne")
    image.save("generated_image.png")
    print("Image générée avec succès!")