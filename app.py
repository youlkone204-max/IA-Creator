import streamlit as st
from google import genai

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# TITRE
# =========================================================

st.title("🤖 IA-Creator")

st.write(
    "Apprends • Crée • Développe tes idées avec l'intelligence artificielle"
)

# =========================================================
# CONNEXION GEMINI
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:

    st.error("❌ Impossible de charger la clé Gemini.")

    st.stop()

# =========================================================
# TYPE DE CRÉATION
# =========================================================

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

# =========================================================
# STYLE
# =========================================================

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

# =========================================================
# PLATEFORME
# =========================================================

st.subheader("📱 Plateforme")

plateforme = st.selectbox(
    "Où vas-tu utiliser le contenu ?",
    [
        "TikTok",
        "YouTube",
        "Facebook",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ]
)

# =========================================================
# FORMAT IMAGE
# =========================================================

format_image = "Non applicable"

if type_creation == "🖼️ Créer un prompt d'image IA":

    st.subheader("📐 Format de l'image")

    format_image = st.selectbox(
        "Choisis le format",
        [
            "1080 × 1080 — Carré",
            "1080 × 1920 — Vertical",
            "1920 × 1080 — Paysage",
            "Format portrait",
            "Format paysage"
        ]
    )

# =========================================================
# DURÉE VIDÉO
# =========================================================

duree = "Non applicable"

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

# =========================================================
# DEMANDE
# =========================================================

st.subheader("📝 Ta demande")

sujet = st.text_area(
    "Décris ce que tu veux créer",
    placeholder=(
        "Exemple : une affiche professionnelle pour "
        "une formation en intelligence artificielle."
    ),
    height=150
)

# =========================================================
# BOUTON
# =========================================================

creer = st.button(
    "✨ Créer avec l'IA",
    use_container_width=True
)

# =========================================================
# TRAITEMENT
# =========================================================

if creer:

    if not sujet.strip():

        st.warning(
            "⚠️ Écris d'abord ce que tu veux créer."
        )

        st.stop()

    # =====================================================
    # CONTEXTE COMMUN
    # =====================================================

    contexte = f"""
Demande :
{sujet}

Style :
{style}

Plateforme :
{plateforme}
"""

    # =====================================================
    # IDÉE
    # =====================================================

    if type_creation == "💡 Créer une idée":

        prompt = f"""
Tu es un expert en créativité, marketing digital
et intelligence artificielle.

{contexte}

Crée une idée originale et réaliste.

Présente :

1. NOM DE L'IDÉE
2. CONCEPT
3. PUBLIC CIBLE
4. COMMENT LA RÉALISER
5. POURQUOI ELLE EST INTÉRESSANTE
6. ACCROCHE
7. APPEL À L'ACTION

Réponds en français.
"""

    # =====================================================
    # TEXTE
    # =====================================================

    elif type_creation == "✍️ Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé
dans le marketing digital et les réseaux sociaux.

{contexte}

Crée un texte professionnel et accrocheur.

Le texte doit :

- commencer par une accroche forte ;
- être facile à comprendre ;
- être adapté à la plateforme ;
- correspondre au style choisi ;
- terminer par un appel à l'action.

Réponds en français.
"""

    # =====================================================
    # SCRIPT VIDÉO
    # =====================================================

    elif type_creation == "🎬 Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé
dans TikTok, YouTube Shorts et Facebook Reels.

{contexte}

Durée :
{duree}

Crée un script vidéo professionnel.

Pour chaque scène indique :

🎬 SCÈNE
⏱️ Durée
🎥 Image / action
🎙️ Narration / dialogue
📝 Texte à l'écran
✨ Effet / transition

Commence par une accroche très forte.

Termine par :
- une phrase mémorable ;
- un appel à s'abonner ;
- un appel à commenter.

Le script doit être facile à utiliser avec CapCut
ou un générateur vidéo IA.

Réponds en français.
"""

    # =====================================================
    # IDÉE D'AFFICHE
    # =====================================================

    elif type_creation == "🎨 Créer une idée d'affiche":

        prompt = f"""
Tu es un directeur artistique professionnel
spécialisé dans la publicité et le design graphique.

{contexte}

Crée un concept complet d'affiche publicitaire.

Présente :

1. TITRE PRINCIPAL
2. SOUS-TITRE
3. TEXTE PUBLICITAIRE
4. COULEURS
5. ÉLÉMENTS VISUELS
6. DISPOSITION
7. ACCROCHE
8.
