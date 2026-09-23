import streamlit as st
from google import genai

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# TITRE
# --------------------------------------------------

st.title("🤖 IA-Creator")
st.write("Bienvenue dans ton espace de création avec l'intelligence artificielle.")

# --------------------------------------------------
# CONNEXION À GEMINI
# --------------------------------------------------

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception as e:
    st.error("❌ Impossible de charger la clé Gemini.")
    st.stop()

# --------------------------------------------------
# CHOIX DU TYPE DE CRÉATION
# --------------------------------------------------

type_creation = st.selectbox(
    "Que veux-tu créer ?",
    [
        "Créer une idée",
        "Créer un texte",
        "Créer un script vidéo",
        "Créer une idée d'affiche"
    ]
)

# --------------------------------------------------
# SUJET
# --------------------------------------------------

sujet = st.text_area(
    "Décris ce que tu veux créer :",
    placeholder="Exemple : une vidéo TikTok sur les avantages de l'intelligence artificielle..."
)

# --------------------------------------------------
# BOUTON
# --------------------------------------------------

if st.button("✨ Créer", use_container_width=True):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ce que tu veux créer.")
        st.stop()

    # --------------------------------------------------
    # PROMPTS
    # --------------------------------------------------

    if type_creation == "Créer une idée":

        prompt = f"""
Tu es un expert en créativité, marketing digital et intelligence artificielle.

L'utilisateur veut créer une idée à partir de ce sujet :

{sujet}

Donne une idée originale, simple, intéressante et exploitable.
Explique :
1. L'idée
2. Pourquoi elle peut intéresser les gens
3. Comment la réaliser
4. Une phrase accrocheuse pour commencer

Réponds en français.
"""

    elif type_creation == "Créer un texte":

        prompt = f"""
Tu es un excellent rédacteur spécialisé dans les réseaux sociaux.

Écris un texte professionnel et naturel à partir de ce sujet :

{sujet}

Le texte doit être clair, accrocheur et facile à comprendre.
Il doit être adapté aux réseaux sociaux.

Réponds uniquement en français.
"""

    elif type_creation == "Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans les vidéos TikTok,
YouTube Shorts, Facebook Reels et contenus viraux.

Crée un script vidéo professionnel à partir de ce sujet :

{sujet}

Structure le script ainsi :

SCÈNE 1
- Image / action :
- Dialogue / narration :
- Texte à l'écran :

SCÈNE 2
- Image / action :
- Dialogue / narration :
- Texte à l'écran :

SCÈNE 3
- Image / action :
- Dialogue / narration :
- Texte à l'écran :

TERMINE PAR :
- Une phrase forte
- Un appel à s'abonner
- Un appel à commenter

Le script doit être dynamique et facile à transformer en vidéo.

Réponds en français.
"""

    else:

        prompt = f"""
Tu es un expert en publicité, design graphique et marketing.

Propose une idée d'affiche publicitaire professionnelle à partir de ce sujet :

{sujet}

Donne :

1. Le titre principal
2. Le sous-titre
3. Les éléments visuels à utiliser
4. Les couleurs recommandées
5. La disposition des éléments
6. Le texte publicitaire
7. Un appel à l'action

L'affiche doit être moderne, professionnelle et adaptée aux réseaux sociaux.

Réponds en français.
"""

    # --------------------------------------------------
    # APPEL GEMINI
    # --------------------------------------------------

    with st.spinner("IA-Creator prépare ta réponse..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
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

            st.code(str(e))
