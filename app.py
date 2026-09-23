import streamlit as st
from google import genai

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Apprends • Crée • Développe tes idées avec l'IA")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ Impossible de charger la clé Gemini.")
    st.stop()

st.subheader("🚀 Que veux-tu créer ?")

type_creation = st.selectbox(
    "Choisis un outil",
    [
        "💡 Créer une idée",
        "✍️ Créer un texte",
        "🎬 Créer un script vidéo",
        "🎨 Créer une idée d'affiche"
    ]
)

st.subheader("📝 Ta demande")

sujet = st.text_area(
    "Décris ce que tu veux créer",
    placeholder="Exemple : une vidéo TikTok sur l'intelligence artificielle.",
    height=150
)

if st.button("✨ Créer avec l'IA", use_container_width=True):

    if not sujet.strip():
        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    if type_creation == "💡 Créer une idée":

        prompt = f"""
Tu es un expert en créativité, marketing digital et intelligence artificielle.

La demande de l'utilisateur est :
{sujet}

Propose une idée originale et facile à réaliser.

Présente :
1. Nom de l'idée
2. Concept
3. Comment la réaliser
4. Pourquoi elle est intéressante
5. Une accroche forte
6. Un conseil pour la rendre plus attractive

Réponds en français.
"""

    elif type_creation == "✍️ Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé dans les réseaux sociaux.

La demande de l'utilisateur est :
{sujet}

Écris un texte professionnel, naturel et accrocheur.

Le texte doit :
- commencer par une accroche forte ;
- être facile à comprendre ;
- utiliser des phrases courtes ;
- donner envie de continuer à lire ;
- terminer par un appel à l'action.

Réponds en français.
"""

    elif type_creation == "🎬 Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans TikTok,
YouTube Shorts et Facebook Reels.

La demande de l'utilisateur est :
{sujet}

Crée un script vidéo professionnel.

SCÈNE 1
Image et action :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

SCÈNE 2
Image et action :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

SCÈNE 3
Image et action :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

SCÈNE 4
Image et action :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

SCÈNE 5
Image et action :
Narration ou dialogue :
Texte à l'écran :
Effet ou transition :

À la fin :
- une phrase forte ;
- un appel à s'abonner ;
- un appel à commenter.

Réponds en français.
"""

    else:

        prompt = f"""
Tu es un directeur artistique spécialisé dans la publicité
et le design graphique.

La demande de l'utilisateur est :
{sujet}

Crée un concept complet d'affiche publicitaire.

Présente :
1. Titre principal
2. Sous-titre
3. Texte publicitaire
4. Couleurs
5. Éléments visuels
6. Disposition de l'affiche
7. Accroche
8. Appel à l'action

L'affiche doit être moderne, professionnelle et adaptée
aux réseaux sociaux.

Réponds en français.
"""

    try:

        with st.spinner("🤖 IA-Creator prépare ta réponse..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        if response.text:

            resultat = response.text

            st.success("✅ Création terminée !")

            st.subheader("✨ Ton résultat")

            st.text_area(
                "Résultat",
                value=resultat,
                height=400
            )

            st.download_button(
                "📥 Télécharger le résultat",
                data=resultat,
                file_name="IA-Creator-resultat.txt",
                mime="text/plain",
                use_container_width=True
            )

        else:

            st.warning("⚠️ Gemini n'a retourné aucun résultat.")

    except Exception as e:

        st.error("❌ Gemini n'a pas pu générer la réponse.")
        st.write(str(e))
