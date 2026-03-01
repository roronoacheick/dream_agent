import streamlit as st
from backend import generate_image
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Dream Agent",
    page_icon="🎨"
)

# Titre
st.title("🎨 Dream Agent")

# Vérifier que le token existe
if not os.getenv("HF_TOKEN"):
    st.error("❌ Token Hugging Face manquant dans .env")
    st.stop()

# Input du prompt
prompt = st.text_input(
    "Décris l'image que tu veux générer :",
    placeholder="Ex: Un coucher de soleil sur la montagne"
)

# Bouton de génération
if st.button("Générer l'image", type="primary"):
    if not prompt.strip():
        st.error("Veuillez entrer une description !")
    else:
        with st.spinner("Génération en cours... ⚡"):
            try:
                image = generate_image(prompt)
                st.image(image, caption="Image générée")
                st.success("✅ Image générée !")
                
            except Exception as e:
                st.error(f"Erreur : {str(e)}")





