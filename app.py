import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Crée avec l'intelligence artificielle")

# Connexion Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ Impossible de connecter Gemini.")
    st.info("Vérifie le secret GEMINI_API_KEY dans Streamlit.")
    st.stop()

# Outil
outil = st.selectbox(
    "🚀 Que veux-tu créer ?",
    [
        "Créer une idée",
        "Créer un texte",
        "Créer un script vidéo",
        "Créer une idée d'affiche",
        "Créer un prompt d'image IA"
    ]
)

# Style
style = st.selectbox(
    "🎨 Style",
    [
        "Viral et accrocheur",
        "Professionnel",
        "Éducatif",
        "Amusant",
        "Émotionnel",
        "Premium et élégant",
        "Cinématographique",
        "Photorealiste",
        "3D ultra-réaliste"
    ]
)

# Plateforme
plateforme = st.selectbox(
    "📱 Plateforme",
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

if outil == "Créer un prompt d'image IA":
    format_image = st.selectbox(
        "📐 Format",
        [
            "1080 x 1080 - Carré",
            "1080 x 1920 - Vertical",
            "1920 x 1080 - Paysage"
        ]
    )

# Durée vidéo
duree = ""

if outil == "Créer un script vidéo":
    duree = st.selectbox(
        "⏱️ Durée",
        [
            "10 secondes",
            "15 secondes",
            "30 secondes",
            "60 secondes"
        ]
    )

# Demande
sujet = st.text_area(
    "📝 Ta demande",
    height=150,
    placeholder="Exemple : crée une vidéo sur l'intelligence artificielle"
)

# Bouton
if st.button("✨ CRÉER AVEC L'IA", use_container_width=True):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    # SCRIPT VIDÉO
    if outil == "Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans TikTok,
YouTube Shorts et Facebook Reels.

Crée un script vidéo professionnel et dynamique.

Sujet : {sujet}
Plateforme : {plateforme}
Style : {style}
Durée : {duree}

Le script doit être directement utilisable avec CapCut.

Commence par une accroche très forte.

Organise le script scène par scène.

Pour chaque scène indique :

SCÈNE
Durée :
Ce que l'on voit à l'écran :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :
Ambiance sonore :

Respecte la durée totale demandée.

Termine par un appel à l'action naturel invitant
les spectateurs à s'abonner, aimer la vidéo et commenter.

Ajoute également :

TITRE DE LA VIDÉO

LÉGENDE

HASHTAGS

Réponds uniquement en français.
"""

    # IDÉE
    elif outil == "Créer une idée":

        prompt = f"""
Tu es un expert en création de contenu.

Crée une idée originale à partir de cette demande :

{sujet}

Plateforme : {plateforme}
Style : {style}

Donne :

1. Titre
2. Concept
3. Accroche
4. Déroulement
5. Appel à l'action
6. Hashtags

Réponds en français.
"""

    # TEXTE
    elif outil == "Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé dans
les réseaux sociaux.

Crée un texte à partir de cette demande :

{sujet}

Plateforme : {plateforme}
Style : {style}

Le texte doit être naturel, clair et accrocheur.

Termine par un appel à l'action.

Ajoute des hashtags pertinents.

Réponds en français.
"""

    # AFFICHE
    elif outil == "Créer une idée d'affiche":

        prompt = f"""
Tu es un directeur artistique professionnel.

Crée une idée d'affiche professionnelle.

Sujet : {sujet}
Plateforme : {plateforme}
Style : {style}

Donne :

1. Concept visuel
2. Sujet principal
3. Arrière-plan
4. Éclairage
5. Couleurs
6. Texte principal
7. Texte secondaire
8. Composition
9. Éléments graphiques
10. Appel à l'action

Réponds en français.
"""

    # PROMPT IMAGE
    else:

        prompt = f"""
Tu es un expert en création de
