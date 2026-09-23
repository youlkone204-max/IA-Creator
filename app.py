import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Crée des contenus professionnels avec l'intelligence artificielle")

# Connexion Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ Impossible de charger la clé Gemini.")
    st.stop()

# Outil
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
    placeholder="Exemple : une vidéo TikTok sur l'intelligence artificielle.",
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

    # IDÉE
    if type_creation == "💡 Créer une idée":

        prompt = "\n".join([
            "Tu es un expert en créativité, marketing digital et intelligence artificielle.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée une idée originale et réaliste.",
            "",
            "Présente :",
            "1. Nom de l'idée",
            "2. Concept",
            "3. Public cible",
            "4. Comment la réaliser",
            "5. Pourquoi elle est intéressante",
            "6. Accroche",
            "7. Appel à l'action",
            "",
            "Réponds en français."
        ])

    # TEXTE
    elif type_creation == "✍️ Créer un texte":

        prompt = "\n".join([
            "Tu es un rédacteur professionnel spécialisé dans le marketing digital et les réseaux sociaux.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée un texte professionnel et accrocheur.",
            "Commence par une accroche forte.",
            "Utilise des phrases faciles à comprendre.",
            "Termine par un appel à l'action.",
            "",
            "Réponds en français."
        ])

    # SCRIPT VIDÉO
    elif type_creation == "🎬 Créer un script vidéo":

        prompt = "\n".join([
            "Tu es un scénariste professionnel spécialisé dans TikTok, YouTube Shorts et Facebook Reels.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "Durée : " + duree,
            "",
            "Crée un script vidéo professionnel.",
            "",
            "Pour chaque scène indique :",
            "- Numéro de scène",
            "- Durée",
            "- Image et action",
            "- Narration ou dialogue",
            "- Texte à l'écran",
            "- Effet ou transition",
            "",
            "Commence par une accroche très forte.",
            "Termine par un appel à s'abonner et à commenter.",
            "",
            "Réponds en français."
        ])

    # AFFICHE
    elif type_creation == "🎨 Créer une idée d'affiche":

        prompt = "\n".join([
            "Tu es un directeur artistique professionnel spécialisé dans la publicité et le design graphique.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée un concept complet d'affiche publicitaire.",
            "",
            "Présente :",
            "1. Titre principal",
            "2. Sous-titre",
            "3. Texte publicitaire",
            "4. Couleurs",
            "5. Éléments visuels",
            "6. Disposition",
            "7. Accroche",
            "8. Appel à l'action",
            "9. Prompt pour générer l'affiche avec une IA",
            "",
            "Réponds en français."
        ])

    # PROMPT IMAGE
    else:

        prompt = "\n".join([
            "Tu es un expert professionnel en prompt engineering pour la génération d'images avec l'intelligence artificielle.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "Format : " + format_image,
            "",
            "Crée un prompt d'image très détaillé et professionnel.",
            "",
            "Le prompt doit préciser :",
            "1. Sujet principal",
            "2. Personnages ou objets",
            "3. Apparence",
            "4. Vêtements si nécessaire",
            "5. Environnement",
            "6. Arrière-plan",
            "7. Éclairage",
            "8. Composition",
            "9. Angle de caméra",
            "10. Profondeur de champ",
            "11. Style visuel",
            "12. Niveau de détail",
            "13. Qualité visuelle",
            "14. Format",
            "",
            "Crée deux parties :",
            "PROMPT FINAL",
            "",
            "PROMPT NÉGATIF",
            "",
            "Réponds en français."
        ])

    # GEMINI
    try:

        with st.spinner("🤖 IA-C
