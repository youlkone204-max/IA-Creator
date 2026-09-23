import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖"
)

st.title("🤖 IA-Creator")
st.write("Crée avec l'intelligence artificielle")

# Connexion Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erreur avec la clé Gemini.")
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
    height=150
)

# Bouton
if st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
):

    if not sujet.strip():

        st.warning("Écris d'abord ta demande.")
        st.stop()

    # Prompt envoyé à Gemini
    prompt = (
        "Tu es un expert professionnel en intelligence artificielle, "
        "marketing digital et création de contenu.\n\n"
        "Outil : " + outil + "\n"
        "Demande : " + sujet + "\n"
        "Style : " + style + "\n"
        "Plateforme : " + plateforme + "\n"
        "Format : " + format_image + "\n"
        "Durée : " + duree + "\n\n"
        "Crée une réponse professionnelle, claire et détaillée. "
        "Réponds en français."
    )

    # Génération Gemini
    try:

        with st.spinner("IA-Creator travaille..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        if response.text:

            resultat = response.text

            st.success("Création terminée !")

            st.subheader("✨ Ton résultat")

            # Résultat
            st.text_area(
                "Résultat",
                resultat,
                height=500
            )

            # Zone de copie
            st.code(
                resultat,
                language="text"
            )

            # Téléchargement
            st.download_button(
                "📥 Télécharger le résultat",
                resultat,
                "IA-Creator-resultat.txt",
                "text/plain",
                use_container_width=True
            )

        else:

            st.warning(
                "Gemini n'a retourné aucun résultat."
            )

    except Exception as e:

        st.error("Erreur Gemini.")
        st.write(str(e))
