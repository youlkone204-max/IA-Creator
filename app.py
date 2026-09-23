import streamlit as st
from google import genai

# Configuration
st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# Titre
st.title("🤖 IA-Creator")
st.write("Bienvenue dans ton espace de création avec l'intelligence artificielle.")

# Connexion à Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:
    st.error("❌ Impossible de charger la clé Gemini.")
    st.stop()


# Choix de la création
type_creation = st.selectbox(
    "Que veux-tu créer ?",
    [
        "Créer une idée",
        "Créer un texte",
        "Créer un script vidéo",
        "Créer une idée d'affiche"
    ]
)


# Sujet
sujet = st.text_area(
    "Décris ce que tu veux créer :",
    placeholder="Exemple : une vidéo TikTok sur l'intelligence artificielle..."
)


# Bouton
if st.button("✨ Créer", use_container_width=True):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ce que tu veux créer.")
        st.stop()

    # Création du prompt
    if type_creation == "Créer une idée":

        prompt = f"""
Tu es un expert en créativité et en intelligence artificielle.

Sujet :
{sujet}

Donne une idée originale et facile à réaliser.

Présente :
1. L'idée
2. Pourquoi elle est intéressante
3. Comment la réaliser
4. Une accroche puissante

Réponds en français.
"""

    elif type_creation == "Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé dans les réseaux sociaux.

Sujet :
{sujet}

Écris un texte professionnel, naturel,
accrocheur et facile à comprendre.

Réponds en français.
"""

    elif type_creation == "Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé
dans TikTok, YouTube Shorts et Facebook Reels.

Sujet :
{sujet}

Crée un script vidéo professionnel.

SCÈNE 1
Image / action :
Dialogue / narration :
Texte à l'écran :

SCÈNE 2
Image / action :
Dialogue / narration :
Texte à l'écran :

SCÈNE 3
Image / action :
Dialogue / narration :
Texte à l'écran :

Termine avec :
- une phrase forte
- un appel à s'abonner
- un appel à commenter

Réponds en français.
"""

    else:

        prompt = f"""
Tu es un expert en publicité et en design graphique.

Sujet :
{sujet}

Propose une idée d'affiche publicitaire professionnelle.

Donne :
1. Le titre
2. Le sous-titre
3. Le texte publicitaire
4. Les couleurs
5. Les éléments visuels
6. La disposition
7. L'appel à l'action

Réponds en français.
"""


    # Appel Gemini
    try:

        with st.spinner("IA-Creator prépare ta réponse..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        if response.text:

            st.success("✅ Création terminée !")

            st.markdown("### ✨ Résultat")

            st.write(response.text)

        else:

            st.warning("⚠️ Gemini n'a retourné aucun texte.")

    except Exception as e:

        st.error("❌ Gemini n'a pas pu générer la réponse.")

        st.write(str(e))
