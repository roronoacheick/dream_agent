import streamlit as st
from backend import generate_image
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Dream Agent",
    page_icon="🎨"
)

st.title("🎨 Dream Agent")

if not os.getenv("HF_TOKEN"):
    st.error("❌ Token Hugging Face manquant dans .env")
    st.stop()

dream_text = st.text_input(
    "Décris l'image que tu veux générer :",
    placeholder="Ex: Un coucher de soleil sur la montagne"
)

if st.button("Générer l'image", type="primary"):
    if not dream_text.strip():
        st.error("Veuillez entrer une description !")
    else:
        with st.spinner("Génération en cours... ⚡"):
            try:
                image = generate_image(dream_text)
                st.image(image, caption="Image générée")
                st.success("✅ Image générée !")
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
