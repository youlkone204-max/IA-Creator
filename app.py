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
# CHOIX DE L'OUTIL
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
# GÉNÉRATION
# ==========================================

if st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    # ======================================
    # PROMPT SCRIPT VIDÉO
    # ======================================

    if outil == "Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans
TikTok, YouTube Shorts et Facebook Reels.

Crée un script vidéo professionnel.

Sujet :
{sujet}

Plateforme :
{plateforme}

Style :
{style}

Durée :
{duree}

Le script doit être dynamique et facile à utiliser
pour créer une vidéo avec CapCut.

Commence avec une accroche très forte.

Organise le résultat scène par scène.

Pour chaque scène indique exactement :

SCÈNE 1
Durée :
Ce que l'on voit à l'écran :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

Continue avec les scènes suivantes.

Le script doit respecter la durée demandée.

Termine par un appel à l'action encourageant
les spectateurs à s'abonner, aimer la vidéo
et commenter.

Ne donne aucune explication inutile.
Donne directement le script.
"""

    # ======================================
    # PROMPT IDÉE
    # ======================================

    elif outil == "Créer une idée":

        prompt = f"""
Tu es un expert en création de contenu.

Donne une idée de contenu originale et intéressante.

Demande :
{sujet}

Plateforme :
{plateforme}

Style :
{style}

Donne :

1. Titre
2. Concept
3. Accroche
4. Déroulement
5. Appel à l'action

Réponds en français.
"""

    # ======================================
    # PROMPT TEXTE
    # ======================================

    elif outil == "Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé
dans les réseaux sociaux.

Crée un texte de qualité à partir de cette demande :

{sujet}

Plateforme :
{plateforme}

Style :
{style}

Le texte doit être naturel, accrocheur et adapté
à la plateforme choisie.

Ajoute un appel à l'action à la fin.

Réponds en français.
"""

    # ======================================
    # PROMPT AFFICHE
    # ======================================

    elif outil == "Créer une idée d'affiche":

        prompt = f"""
Tu es un directeur artistique professionnel.

Crée une idée d'affiche professionnelle.

Sujet :
{sujet}

Plateforme :
{plateforme}

Style :
{style}

Donne :

1. Concept visuel
2. Sujet principal
3. Arrière-plan
4. Couleurs
5. Éclairage
6. Texte principal
7. Texte secondaire
8. Composition
9. Éléments graphiques
10. Appel à l'action

Réponds en français.
"""

    # ======================================
    # PROMPT IMAGE IA
    # ======================================

    else:

        prompt = f"""
Tu es un expert professionnel en création de prompts
pour générateurs d'images IA.

Crée un prompt d'image extrêmement détaillé.

Sujet :
{sujet}

Style :
{style}

Format :
{format_image}

Plateforme :
{plateforme}

Le prompt doit préciser :

- sujet principal
- apparence
- vêtements
- posture
- expression
- environnement
- arrière-plan
- éclairage
- couleurs
- composition
- profondeur de champ
- qualité
- détails réalistes
- ambiance

Donne uniquement le prompt final prêt à copier.

Réponds en français.
"""

    # ======================================
    # APPEL GEMINI
    # ======================================

    try:

        with st.spinner("🤖 Gemini est en train de créer..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        resultat = response.text

        st.success("✅ Création terminée !")

        st.markdown("## ✨ Ton résultat")

        st.write(resultat)

        # ==================================
        # TÉLÉCHARGEMENT
        # ==================================

        st.download_button(
            label="📥 Télécharger le résultat",
            data=resultat,
            file_name="ia_creator_resultat.txt",
            mime="text/plain",
            use_container_width=True
        )

    except Exception as e:

        st.error("❌ Une erreur est survenue pendant la génération.")

        st.code(str(e))
