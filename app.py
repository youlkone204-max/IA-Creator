import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IA-Creator")
st.write("Bienvenue dans ton espace de création avec l'intelligence artificielle.")

st.subheader("Que veux-tu créer ?")

option = st.selectbox(
    "Choisis une option",
    [
        "Créer une idée",
        "Créer un texte",
        "Créer un script vidéo",
        "Créer une idée d'affiche"
    ]
)

description = st.text_area(
    "Décris ce que tu veux créer :",
    placeholder="Écris ton idée ici..."
)

if st.button("Créer"):
    if not description.strip():
        st.warning("Écris d'abord une description.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            prompt = f"""
Tu es l'assistant IA de l'application IA-Creator.

Type de création : {option}

Demande de l'utilisateur :
{description}

Réponds en français, de manière claire, professionnelle et utile.
"""

            with st.spinner("IA-Creator prépare ta réponse..."):
                response = client.responses.create(
                    model="gpt-5.6-luna",
                    input=prompt
                )

            st.success("Création terminée !")
            st.write(response.output_text)

        except Exception as e:
            st.error("Une erreur est survenue.")
            st.write(str(e))
