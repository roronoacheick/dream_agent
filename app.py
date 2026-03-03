import streamlit as st
from backend import generate_image
import os
from dotenv import load_dotenv
import speech_recognition as sr
import tempfile

load_dotenv()

st.set_page_config(
    page_title="Dream Agent",
    page_icon="🎨"
)

st.title("🎨 Dream Agent")

if not os.getenv("HF_TOKEN"):
    st.error("❌ Token Hugging Face manquant dans .env")
    st.stop()

# Onglets : Texte ou Vocal
tab1, tab2 = st.tabs(["✍️ Écrire", "🎤 Parler"])

dream_text = ""

with tab1:
    st.subheader("Décris l'image que tu veux générer")
    dream_text = st.text_input(
        "Ton texte :",
        placeholder="Ex: Un coucher de soleil sur la montagne"
    )

with tab2:
    st.subheader("Enregistre ton rêve")
    
    audio_file = st.audio_input("Parle ton rêve 🎤")
    
    if audio_file:
        st.info("🔄 Conversion en cours...")
        
        try:
            # Créer un fichier temporaire pour l'audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.getvalue())
                tmp_path = tmp.name
            
            # Reconnaître la parole
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(tmp_path) as source:
                audio = recognizer.record(source)
            
            dream_text = recognizer.recognize_google(audio, language="fr-FR")
            st.success(f"✅ Texte reconnu : {dream_text}")
            
            # Nettoyer le fichier temporaire
            os.remove(tmp_path)
            
        except sr.UnknownValueError:
            st.error("❌ Impossible de comprendre l'audio. Essaie de parler plus clairement ou plus fort.")
        except sr.RequestError as e:
            st.error(f"❌ Erreur de connexion : {e}")

# Afficher le texte final
if dream_text:
    st.write(f"**Description finale :** {dream_text}")

# Bouton de génération
if st.button("🚀 Générer l'image", type="primary", use_container_width=True):
    if not dream_text.strip():
        st.error("Veuillez entrer ou dicter une description !")
    else:
        with st.spinner("Génération en cours... ⚡"):
            try:
                image = generate_image(dream_text)
                st.image(image, caption="Image générée", use_container_width=True)
                st.success("✅ Image générée !")
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
