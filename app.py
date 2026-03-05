import streamlit as st
from backend import generate_image, generate_video_immersive
import os
from dotenv import load_dotenv
import speech_recognition as sr
import tempfile

load_dotenv()

st.set_page_config(
    page_title="Dream Agent",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé ultra moderne et époustouflant
st.markdown("""
<style>
    /* Fond sombre professionnel */
    .stApp {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a0a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Barre latérale stylisée */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0a2e 0%, #0f0f1e 100%);
        border-right: 2px solid #ff006e;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }
    
    /* Onglets stylisés */
    [data-testid="stTabs"] [aria-selected="true"] {
        border-bottom: 3px solid #ff006e !important;
    }
    
    [data-testid="stTabs"] button {
        color: #b0b0b0 !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTabs"] [aria-selected="true"] button {
        color: #ff006e !important;
    }
    
    /* Titre principal - Gradient vibrant */
    h1 {
        background: linear-gradient(120deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.8em !important;
        letter-spacing: -1px;
    }
    
    h2 {
        color: #ff006e;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 0, 110, 0.3);
    }
    
    h3 {
        color: #8338ec;
        font-weight: 600;
    }
    
    /* Divider personnalisé */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff006e, #8338ec, transparent);
        margin: 1.5em 0;
    }
    
    /* Text input et textarea */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #1a0a2e !important;
        border: 2px solid #8338ec !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border: 2px solid #ff006e !important;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.5) !important;
    }
    
    /* Bouton principal */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #ff006e, #8338ec) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(255, 0, 110, 0.4) !important;
    }
    
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255, 0, 110, 0.6) !important;
    }
    
    /* Messages de succès */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left: 4px solid #06ffa5 !important;
    }
    
    .stSuccess {
        background-color: rgba(6, 255, 165, 0.1) !important;
    }
    
    .stInfo {
        background-color: rgba(51, 56, 236, 0.1) !important;
        border-left: 4px solid #3a86ff !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 110, 0.1) !important;
        border-left: 4px solid #ff006e !important;
    }
    
    .stWarning {
        background-color: rgba(255, 140, 0, 0.1) !important;
        border-left: 4px solid #ffa500 !important;
    }
    
    /* Boîte à conseils */
    .tip-box {
        background: linear-gradient(135deg, rgba(51, 56, 236, 0.15), rgba(131, 56, 236, 0.15)) !important;
        border-left: 4px solid #8338ec !important;
        border-radius: 10px !important;
        padding: 16px !important;
        margin: 1em 0;
        backdrop-filter: blur(10px);
    }
    
    .tip-box strong {
        color: #06ffa5;
    }
    
    /* Labels et placeholders */
    label {
        color: #b0b0b0 !important;
        font-weight: 600 !important;
    }
    
    /* Spinner personnalisé */
    [data-testid="stSpinner"] > div {
        color: #ff006e !important;
    }
    
    /* Séparateur visuel */
    .stDivider {
        margin: 2em 0;
    }
    
    /* Audio input */
    [data-testid="stAudioInput"] {
        border: 2px solid #8338ec;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Colonnes spacing */
    [data-testid="column"] {
        gap: 2rem;
    }
    
    /* Animation de fond subtile */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Texte descriptif */
    p {
        color: #d0d0d0;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

if not os.getenv("HF_TOKEN"):
    st.error("❌ Token Hugging Face manquant dans .env")
    st.stop()

# Personnalisation de la barre latérale
st.sidebar.markdown("""
<h2 style="color: #ff006e; text-align: center; margin-bottom: 0.5em;">🎵 Dream Agent</h2>
<p style="text-align: center; color: #b0b0b0; font-style: italic;">Crée l'univers de ta musique avec l'IA</p>
""", unsafe_allow_html=True)
st.sidebar.divider()

# Navigation
page = st.sidebar.radio(
    "📍 Où veux-tu aller ?", 
    ["🎨 Couvertures d'Album", "🎬 Génération Vidéo", "🎵 Génération Intro"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(131, 56, 236, 0.15), rgba(255, 0, 110, 0.15)); border-radius: 10px; padding: 12px; margin-top: 1em;">
<strong style="color: #06ffa5;">✨ Conseils pour créer :</strong>
<ul style="color: #d0d0d0; margin-top: 0.5em; padding-left: 20px;">
<li>Sois détaillé et précis</li>
<li>Décris les couleurs et émotions</li>
<li>Utilise l'audio pour plus de liberté</li>
<li>N'aie pas peur d'être créatif !</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PAGE 1 : GÉNÉRATEUR DE COUVERTURES D'ALBUM
# ============================================================================
if page == "🎨 Couvertures d'Album":
    # Header époustouflant
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("# 🎨 Couvertures d'Album")
        st.markdown("<p style='color: #06ffa5; font-size: 1.1em; font-weight: 600;'>Transforme ta vision en couverture d'album d'exception</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Onglets : Texte ou Vocal
    tab1, tab2 = st.tabs(["✍️ Écrire ta vision", "🎤 Parler ta vision"])
    
    dream_text = ""
    
    with tab1:
        st.markdown("### 📝 Décris ta couverture d'album")
        st.markdown("<p style='color: #b0b0b0;'>Laisse libre cours à ton imagination. Donne des détails sur les couleurs, le style, l'atmosphère...</p>", unsafe_allow_html=True)
        
        dream_text = st.text_area(
            "Ton idée :",
            placeholder="Ex: Une rose rouge mystérieuse, style cyberpunk néon, lueurs violettes et roses, fond noir profond, détaillé et lumineux",
            height=120,
            key="album_text"
        )
        
        st.markdown("""
        <div class="tip-box">
        💡 <strong>Comment bien décrire :</strong>
        <ul>
        <li>Les éléments principaux (objets, personnages)</li>
        <li>Les couleurs dominantes et secondaires</li>
        <li>Le style artistique (réaliste, abstrait, cyberpunk, etc.)</li>
        <li>L'émotion ou l'ambiance générale</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎤 Parle ta couverture d'album")
        st.markdown("<p style='color: #b0b0b0;'>Raconte à voix haute ce que tu imagines. Le texte sera converti automatiquement.</p>", unsafe_allow_html=True)
        
        audio_file = st.audio_input("Appuie sur le bouton pour parler 🎤", key="album_audio")
        
        if audio_file:
            st.info("🔄 Conversion de ton audio en cours...")
            
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
                st.success(f"✅ Texte reconnu : *{dream_text}*")
                
                # Nettoyer le fichier temporaire
                os.remove(tmp_path)
                
            except sr.UnknownValueError:
                st.error("❌ Je n'ai pas compris ton audio. Essaie de parler plus clairement.")
            except sr.RequestError as e:
                st.error(f"❌ Problème de connexion : {e}")
    
    st.divider()
    
    # Afficher le texte final
    if dream_text:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(131, 56, 236, 0.1)); border-radius: 10px; padding: 16px; border-left: 4px solid #ff006e;'>
        <h3 style='color: #06ffa5; margin-top: 0;'>🎯 Ta description</h3>
        <p style='color: #ffffff; font-size: 1.05em;'>{dream_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton de génération
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Générer ma couverture", type="primary", use_container_width=True, key="generate_album"):
            if not dream_text.strip():
                st.error("Veuillez entrer ou dicter une description !")
            else:
                with st.spinner("🎨 Création magique en cours... Attends, c'est en train de prendre forme..."):
                    try:
                        # Générer l'image
                        image = generate_image(dream_text)
                        
                        # Afficher l'image avec style
                        st.divider()
                        st.markdown("### 🖼️ Voilà ta couverture d'album !")
                        st.image(image, caption="Couverture générée par l'IA", use_container_width=True)
                        
                        st.success("✅ C'est magnifique ! Tu peux générer d'autres couvertures ou essayer une nouvelle description.", icon="✨")
                        
                    except Exception as e:
                        st.error(f"❌ Oups, une erreur s'est produite : {str(e)}")
                        st.info("💡 Essaie avec une description légèrement différente ou réessaie dans quelques instants.")

# ============================================================================
# PAGE 2 : GÉNÉRATION VIDÉO
# ============================================================================
elif page == "🎬 Génération Vidéo":
    # Header époustouflant
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("# 🎬 Génération Vidéo")
        st.markdown("<p style='color: #06ffa5; font-size: 1.1em; font-weight: 600;'>Donne vie à tes vidéos musicales les plus folles</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Onglets : Texte ou Vocal
    tab1, tab2 = st.tabs(["✍️ Écrire ta vidéo", "🎤 Parler ta vidéo"])
    
    video_text = ""
    
    with tab1:
        st.markdown("### 📝 Décris la vidéo que tu veux générer")
        st.markdown("<p style='color: #b0b0b0;'>Imagine les mouvements, les transitions, les éléments visuels...</p>", unsafe_allow_html=True)
        
        video_text = st.text_area(
            "Ton idée :",
            placeholder="Ex: Un coucher de soleil magnifique sur une montagne enneigée, avec des oiseaux qui volent, ambiance cinématographique",
            height=120,
            key="video_text"
        )
        
        st.markdown("""
        <div class="tip-box">
        💡 <strong>Comment bien décrire une vidéo :</strong>
        <ul>
        <li>Les mouvements de caméra (zoom, panoramique, etc.)</li>
        <li>Les transitions et effets visuels</li>
        <li>L'ambiance et les couleurs dominantes</li>
        <li>La durée et le rythme souhaités</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎤 Parle ta vidéo")
        st.markdown("<p style='color: #b0b0b0;'>Décris à voix haute la vidéo que tu imagines.</p>", unsafe_allow_html=True)
        
        audio_file = st.audio_input("Appuie sur le bouton pour parler 🎤", key="video_audio")
        
        if audio_file:
            st.info("🔄 Conversion de ton audio en cours...")
            
            try:
                # Créer un fichier temporaire pour l'audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_file.getvalue())
                    tmp_path = tmp.name
                
                # Reconnaître la parole
                recognizer = sr.Recognizer()
                
                with sr.AudioFile(tmp_path) as source:
                    audio = recognizer.record(source)
                
                video_text = recognizer.recognize_google(audio, language="fr-FR")
                st.success(f"✅ Texte reconnu : *{video_text}*")
                
                # Nettoyer le fichier temporaire
                os.remove(tmp_path)
                
            except sr.UnknownValueError:
                st.error("❌ Je n'ai pas compris ton audio. Essaie de parler plus clairement.")
            except sr.RequestError as e:
                st.error(f"❌ Problème de connexion : {e}")
    
    st.divider()
    
    # Afficher le texte final
    if video_text:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(131, 56, 236, 0.1)); border-radius: 10px; padding: 16px; border-left: 4px solid #ff006e;'>
        <h3 style='color: #06ffa5; margin-top: 0;'>🎯 Ta description</h3>
        <p style='color: #ffffff; font-size: 1.05em;'>{video_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton de génération
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎬 Générer ma vidéo", type="primary", use_container_width=True, key="generate_video"):
            if not video_text.strip():
                st.error("Veuillez entrer ou dicter une description !")
            else:
                with st.spinner("🎬 Création de ta vidéo immersive en cours... C'est magique ce qui se passe là-dedans..."):
                    try:
                        video_data = generate_video_immersive(video_text)
                        
                        st.divider()
                        st.markdown("### 🎥 Voilà ta vidéo immersive !")
                        st.video(video_data)
                        
                        st.success("✅ Vidéo immersive générée ! Elle boucle en continu pour une expérience immersive.", icon="🎬")
                        
                    except Exception as e:
                        st.error(f"❌ Oups, une erreur s'est produite : {str(e)}")
                        st.info("💡 La génération vidéo immersive utilise Google Cloud. Assure-toi d'avoir une connexion stable.")

# ============================================================================
# PAGE 3 : GÉNÉRATION INTRO
# ============================================================================
elif page == "🎵 Génération Intro":
    # Header époustouflant
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("# 🎵 Génération Intro")
        st.markdown("<p style='color: #06ffa5; font-size: 1.1em; font-weight: 600;'>Crée l'introduction parfaite pour tes morceaux</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Onglets : Texte ou Vocal
    tab1, tab2 = st.tabs(["✍️ Écrire ton intro", "🎤 Parler ton intro"])
    
    intro_text = ""
    
    with tab1:
        st.markdown("### 📝 Décris l'intro que tu veux générer")
        st.markdown("<p style='color: #b0b0b0;'>Genre musical, instruments, tempo, ambiance...</p>", unsafe_allow_html=True)
        
        intro_text = st.text_area(
            "Ton idée :",
            placeholder="Ex: Une intro dynamique avec des beat hip-hop, 808 percussifs, synthés modernes, ambiance urbaine futuriste",
            height=120,
            key="intro_text"
        )
        
        st.markdown("""
        <div class="tip-box">
        💡 <strong>Comment bien décrire une intro :</strong>
        <ul>
        <li>Le genre musical (hip-hop, R&B, électro, etc.)</li>
        <li>Les instruments que tu imagines</li>
        <li>Le tempo et l'énergie</li>
        <li>L'ambiance générale (sombre, énergique, relaxe, etc.)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎤 Parle ton intro")
        st.markdown("<p style='color: #b0b0b0;'>Décris à voix haute l'intro musicale que tu as en tête.</p>", unsafe_allow_html=True)
        
        audio_file = st.audio_input("Appuie sur le bouton pour parler 🎤", key="intro_audio")
        
        if audio_file:
            st.info("🔄 Conversion de ton audio en cours...")
            
            try:
                # Créer un fichier temporaire pour l'audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_file.getvalue())
                    tmp_path = tmp.name
                
                # Reconnaître la parole
                recognizer = sr.Recognizer()
                
                with sr.AudioFile(tmp_path) as source:
                    audio = recognizer.record(source)
                
                intro_text = recognizer.recognize_google(audio, language="fr-FR")
                st.success(f"✅ Texte reconnu : *{intro_text}*")
                
                # Nettoyer le fichier temporaire
                os.remove(tmp_path)
                
            except sr.UnknownValueError:
                st.error("❌ Je n'ai pas compris ton audio. Essaie de parler plus clairement.")
            except sr.RequestError as e:
                st.error(f"❌ Problème de connexion : {e}")
    
    st.divider()
    
    # Afficher le texte final
    if intro_text:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(131, 56, 236, 0.1)); border-radius: 10px; padding: 16px; border-left: 4px solid #ff006e;'>
        <h3 style='color: #06ffa5; margin-top: 0;'>🎯 Ta description</h3>
        <p style='color: #ffffff; font-size: 1.05em;'>{intro_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton de génération
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Générer mon intro", type="primary", use_container_width=True, key="generate_intro"):
            if not intro_text.strip():
                st.error("Veuillez entrer ou dicter une description !")
            else:
                with st.spinner("🎵 Création de ton intro en cours... L'IA est en train de créer ta musique..."):
                    st.info("🚀 La fonction de génération d'intro est actuellement en développement. Reviens bientôt !")
                    # La fonction generate_intro() sera appelée ici une fois implémentée
                    # audio_data = generate_intro(intro_text)
                    # st.audio(audio_data)
