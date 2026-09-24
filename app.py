import streamlit as st
from google import genai

# ==========================================
# IA-CREATOR
# ==========================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Crée avec l'intelligence artificielle")

# ==========================================
# CONNEXION GEMINI
# ==========================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ Impossible de connecter Gemini.")
    st.info("Vérifie le secret GEMINI_API_KEY dans Streamlit.")
    st.stop()

# ==========================================
# OUTIL
# ==========================================

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

# ==========================================
# STYLE
# ==========================================

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

# ==========================================
# PLATEFORME
# ==========================================

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

# ==========================================
# FORMAT IMAGE
# ==========================================

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

# ==========================================
# DURÉE VIDÉO
# ==========================================

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

# ==========================================
# DEMANDE
# ==========================================

sujet = st.text_area(
    "📝 Ta demande",
    height=150,
    placeholder="Exemple : crée une vidéo sur l'intelligence artificielle"
)

# ==========================================
# BOUTON
# ==========================================

if st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    # ======================================
    # SCRIPT VIDÉO PROFESSIONNEL
    # ======================================

    if outil == "Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans
TikTok, YouTube Shorts et Facebook Reels.

Ta mission est de créer un script vidéo court,
dynamique, professionnel et facile à produire
avec CapCut.

SUJET :
{sujet}

PLATEFORME :
{plateforme}

STYLE :
{style}

DURÉE :
{duree}

RÈGLES IMPORTANTES :

1. Le début doit contenir une accroche très forte
dans les premières secondes.

2. Le script doit être adapté à la durée demandée.

3. Le rythme doit être dynamique.

4. Chaque scène doit être simple à filmer ou à créer
avec des images, vidéos ou éléments IA.

5. Le contenu doit être clair et naturel.

6. Évite les phrases trop longues.

7. Prévois des changements visuels réguliers.

8. Le résultat doit être directement utilisable
dans CapCut.

STRUCTURE OBLIGATOIRE :

TITRE DE LA VIDÉO

ACCROCHE :
Une phrase courte et très forte pour attirer
l'attention immédiatement.

SCÈNE 1
⏱️ Durée :
🎬 Plan / ce que l'on voit :
🎙️ Narration / dialogue :
📝 Texte à l'écran :
✨ Effet / transition :
🎵 Ambiance sonore :

SCÈNE 2
⏱️ Durée :
🎬 Plan / ce que l'on voit :
🎙️ Narration / dialogue :
📝 Texte à l'écran :
✨ Effet / transition :
🎵 Ambiance sonore :

SCÈNE 3
⏱️ Durée :
🎬 Plan / ce que l'on voit :
🎙️ Narration / dialogue :
📝 Texte à l'écran :
✨ Effet / transition :
🎵 Ambiance sonore :

Continue avec autant de scènes que nécessaire
pour respecter exactement la durée demandée.

À la fin, ajoute :

🔥 MOMENT FORT
Explique brièvement le moment visuel ou verbal
qui doit retenir particulièrement l'attention.

📢 APPEL À L'ACTION
Termine avec une phrase naturelle invitant
le spectateur à :
- s'abonner
- aimer la vidéo
- commenter

📝 LÉGENDE
Propose une courte légende adaptée à la plateforme.

#️⃣ HASHTAGS
Propose des hashtags pertinents.

IMPORTANT :
- Réponds uniquement en français.
- Ne donne aucune explication sur ton fonctionnement.
- Ne parle pas de l'intelligence artificielle comme si elle était
  nécessairement le sujet de la vidéo.
- Respecte le sujet
