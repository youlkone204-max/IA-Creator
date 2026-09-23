import streamlit as st

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
    if description.strip():
        st.success("Ta demande a été reçue !")
        st.write("Type :", option)
        st.write("Description :", description)
    else:
        st.warning("Écris d'abord une description.")
