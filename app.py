import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Apprends • Crée • Développe tes idées avec l'intelligence artificielle")

# Connexion Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Impossible de charger la clé Gemini.")
    st.stop()

# Type de création
st.subheader("🚀 Que veux-tu créer ?")

type_creation = st.selectbox(
    "Choisis ton outil",
    [
        "💡 Créer une idée",
        "✍️ Créer un texte",
        "🎬 Créer un script vidéo",
        "🎨 Créer une idée d'affiche",
        "🖼️ Créer un prompt d'image IA"
    ]
)

# Style
st.subheader("🎨 Style")

style = st.selectbox(
    "Choisis un style",
    [
        "🔥 Viral et accrocheur",
        "💼 Professionnel",
        "🎓 Éducatif",
        "😂 Amusant",
        "❤️ Émotionnel",
        "💎 Premium et élégant",
        "🎬 Cinématographique",
        "📸 Photorealiste",
        "🎨 3D ultra-réaliste"
    ]
)

# Plateforme
st.subheader("📱 Plateforme")

plateforme = st.selectbox(
    "Où utiliser le contenu ?",
    [
        "TikTok",
        "YouTube",
        "Facebook",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ]
)

# Format image
format_image = ""

if type_creation == "🖼️ Créer un prompt d'image IA":

    st.subheader("📐 Format de l'image")

    format_image = st.selectbox(
        "Choisis le format",
        [
            "1080 × 1080 — Carré",
            "1080 × 1920 — Vertical",
            "1920 × 1080 — Paysage",
            "Portrait",
            "Paysage"
        ]
    )

# Durée vidéo
duree = ""

if type_creation == "🎬 Créer un script vidéo":

    st.subheader("⏱️ Durée")

    duree = st.selectbox(
        "Durée de la vidéo",
        [
            "10 secondes",
            "15 secondes",
            "30 secondes",
            "45 secondes",
            "60 secondes",
            "90 secondes"
        ]
    )

# Demande
st.subheader("📝 Ta demande")

sujet = st.text_area(
    "Décris ce que tu veux créer",
    placeholder="Exemple : une affiche professionnelle pour une formation en intelligence artificielle.",
    height=150
)

# Bouton
creer = st.button(
    "✨ Créer avec l'IA",
    use_container_width=True
)

if creer:

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    # Prompt idée
    if type_creation == "💡 Créer une idée":

        prompt = (
            "Tu es un expert en créativité, marketing digital "
            "et intelligence artificielle.\n\n"
            "Demande : " + sujet + "\n\n"
            "Style : " + style + "\n"
            "Plateforme : " + plateforme + "\n\n"
            "Crée une idée originale et réaliste.\n\n"
            "Présente :\n"
            "1. Nom de l'idée\n"
            "2. Concept\n"
            "3. Public cible\n"
            "4. Comment la réaliser\n"
            "5. Pourquoi elle est intéressante\n"
            "6. Accroche\n"
            "7. Appel à l'action\n\n"
            "Réponds en français."
        )

    # Prompt texte
    elif type_creation == "✍️ Créer un texte":

        prompt = (
            "Tu es un rédacteur professionnel spécialisé "
            "dans le marketing digital et les réseaux sociaux.\n\n"
            "Demande : " + sujet + "\n\n"
            "Style : " + style + "\n"
            "Plateforme : " + plateforme + "\n\n"
            "Crée un texte professionnel et accrocheur.\n"
            "Commence par une accroche forte.\n"
            "Utilise des phrases faciles à comprendre.\n"
            "Termine par un appel à l'action.\n\n"
            "Réponds en français."
        )

    # Prompt vidéo
    elif type_creation == "🎬 Créer un script vidéo":

        prompt = (
            "Tu es un scénariste professionnel spécialisé "
            "dans TikTok, YouTube Shorts et Facebook Reels.\n\n"
            "Demande : " + sujet + "\n\n"
            "Style : " + style + "\n"
            "Plateforme : " + plateforme + "\n"
            "Durée : " + duree + "\n\n"
            "Crée un script vidéo professionnel.\n\n"
            "Pour chaque scène indique :\n"
            "- Numéro de scène\n"
            "- Durée\n"
            "- Image et action\n"
            "- Narration ou dialogue\n"
            "- Texte à l'écran\n"
            "- Effet ou transition\n\n"
            "Commence par une accroche très forte.\n"
            "Termine par une phrase mémorable, "
            "un appel à s'abonner et un appel à commenter.\n\n"
            "Réponds en français."
        )

    # Prompt affiche
    elif type_creation == "🎨 Créer une idée d'affiche":

        prompt = (
            "Tu es un directeur artistique professionnel "
            "
