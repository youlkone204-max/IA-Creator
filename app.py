import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Crée avec l'intelligence artificielle")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ Impossible de connecter Gemini.")
    st.info("Vérifie le secret GEMINI_API_KEY dans Streamlit.")
    st.stop()

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

sujet = st.text_area(
    "📝 Ta demande",
    height=150,
    placeholder="Exemple : crée une vidéo sur l'intelligence artificielle"
)

if st.button("✨ CRÉER AVEC L'IA", use_container_width=True):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    if outil == "Créer une idée":

        prompt = (
            "Tu es un expert en création de contenu.\n\n"
            "Crée une idée originale à partir de cette demande :\n"
            + sujet
            + "\n\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\nDonne :\n"
            "1. Titre\n"
            "2. Concept\n"
            "3. Accroche\n"
            "4. Déroulement\n"
            "5. Appel à l'action\n"
            "6. Hashtags\n\n"
            "Réponds en français."
        )

    elif outil == "Créer un texte":

        prompt = (
            "Tu es un rédacteur professionnel spécialisé "
            "dans les réseaux sociaux.\n\n"
            "Crée un texte à partir de cette demande :\n"
            + sujet
            + "\n\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\n"
            "Le texte doit être naturel, clair et accrocheur.\n"
            "Termine par un appel à l'action.\n"
            "Ajoute des hashtags pertinents.\n\n"
            "Réponds en français."
        )

    elif outil == "Créer un script vidéo":

        prompt = (
            "Tu es un scénariste professionnel spécialisé "
            "dans TikTok, YouTube Shorts et Facebook Reels.\n\n"
            "Crée un script vidéo professionnel et dynamique.\n\n"
            "SUJET : "
            + sujet
            + "\nPLATEFORME : "
            + plateforme
            + "\nSTYLE : "
            + style
            + "\nDURÉE : "
            + duree
            + "\n\n"
            "Le script doit être directement utilisable avec CapCut.\n\n"
            "Commence par une accroche très forte.\n"
            "Respecte la durée demandée.\n"
            "Utilise des phrases courtes et dynamiques.\n\n"
            "Pour chaque scène indique exactement :\n\n"
            "SCÈNE 1\n"
            "Durée :\n"
            "Ce que l'on voit à l'écran :\n"
            "Narration ou dialogue :\n"
            "Texte à l'écran :\n"
            "Effet ou transition :\n"
            "Ambiance sonore :\n\n"
            "Continue avec les scènes suivantes "
            "jusqu'à couvrir toute la durée.\n\n"
            "À la fin ajoute :\n"
            "TITRE DE LA VIDÉO\n"
            "LÉGENDE\n"
            "HASHTAGS\n"
            "APPEL À L'ACTION\n\n"
            "L'appel à l'action doit encourager les spectateurs "
            "à s'abonner, aimer la vidéo et commenter.\n\n"
            "Réponds uniquement en français."
        )

    elif outil == "Créer une idée d'affiche":

        prompt = (
            "Tu es un directeur artistique professionnel.\n\n"
            "Crée une idée d'affiche professionnelle.\n\n"
            "Sujet : "
            + sujet
            + "\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\n"
            "Donne :\n"
            "1. Concept visuel\n"
            "2. Sujet principal\n"
            "3. Arrière-plan\n"
            "4. Éclairage\n"
            "5. Couleurs\n"
            "6. Texte principal\n"
            "7. Texte secondaire\n"
            "8. Composition\n"
            "9. Éléments graphiques\n"
            "10. Appel à l'action\n\n"
            "Réponds en français."
        )

    else:

        prompt = (
            "Tu es un expert professionnel en création "
            "de prompts pour générateurs d'images IA.\n\n"
            "Crée un prompt d'image détaillé et professionnel.\n\n"
            "Sujet : "
            + sujet
            + "\nStyle : "
            + style
            + "\nFormat : "
            + format_image
            + "\nPlateforme : "
            + plateforme
            + "\n\n"
            "Décris :\n"
            "- sujet principal\n"
            "- apparence\n"
            "- vêtements\n"
            "- posture\n"
            "- expression\n"
            "- environnement\n"
            "- arrière-plan\n"
            "- éclairage\n"
            "- couleurs\n"
            "- composition\n"
            "- profondeur de champ\n"
            "- ambiance\n"
            "- détails visuels\n"
            "- qualité\n\n"
            "Donne uniquement le prompt final prêt à copier.\n"
            "Réponds en français."
        )

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
