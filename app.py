import streamlit as st
import streamlit.components.v1 as components
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }

    .main {
        max-width: 900px;
        margin: auto;
    }

    .hero {
        background: linear-gradient(135deg, #111827, #2563eb);
        padding: 30px 22px;
        border-radius: 22px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.20);
    }

    .hero h1 {
        margin: 0;
        font-size: 38px;
        font-weight: 800;
    }

    .hero p {
        margin-top: 8px;
        font-size: 17px;
        opacity: 0.95;
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 10px;
        color: #111827;
    }

    .welcome {
        background: white;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .result-box {
        background: white;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #dbeafe;
        margin-top: 20px;
    }

    .history-card {
        background: white;
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        margin-top: 35px;
        padding: 20px;
        font-size: 14px;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 45px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION
# ============================================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False

if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = ""

if "historique" not in st.session_state:
    st.session_state.historique = []


# ============================================================
# ÉCRAN CONNEXION / INSCRIPTION
# ============================================================

if not st.session_state.connecte:

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 IA-Creator</h1>
            <p>Crée avec l'intelligence artificielle</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🔐 Accéder à IA-Creator</div>',
        unsafe_allow_html=True
    )

    mode = st.radio(
        "Choisis une option",
        ["🔐 Se connecter", "📝 Créer un compte"],
        horizontal=True
    )

    st.markdown("### 👤 Tes informations")

    nom = st.text_input(
        "Nom",
        placeholder="Exemple : Issa"
    )

    email = st.text_input(
        "Adresse e-mail",
        placeholder="Exemple : exemple@gmail.com"
    )

    mot_de_passe = st.text_input(
        "Mot de passe",
        type="password",
        placeholder="Entre ton mot de passe"
    )

    confirmation = ""

    if mode == "📝 Créer un compte":
        confirmation = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            placeholder="Répète ton mot de passe"
        )

    if mode == "📝 Créer un compte":

        if st.button(
            "🚀 CRÉER MON COMPTE",
            use_container_width=True
        ):

            if not nom:
                st.error("❌ Entre ton nom.")

            elif not email:
                st.error("❌ Entre ton adresse e-mail.")

            elif not mot_de_passe:
                st.error("❌ Entre un mot de passe.")

            elif mot_de_passe != confirmation:
                st.error("❌ Les deux mots de passe sont différents.")

            else:
                st.session_state.connecte = True
                st.session_state.utilisateur = nom

                st.success("✅ Compte créé avec succès !")
                st.rerun()

    else:

        if st.button(
            "🔓 SE CONNECTER",
            use_container_width=True
        ):

            if not nom:
                st.error("❌ Entre ton nom.")

            elif not email:
                st.error("❌ Entre ton adresse e-mail.")

            elif not mot_de_passe:
                st.error("❌ Entre ton mot de passe.")

            else:
                st.session_state.connecte = True
                st.session_state.utilisateur = nom

                st.success("✅ Connexion réussie !")
                st.rerun()

    st.info(
        "ℹ️ Cette première version utilise une connexion de session. "
        "Les vrais comptes persistants seront ajoutés ensuite."
    )

    st.markdown(
        """
        <div class="footer">
            🤖 IA-Creator<br>
            Crée • Apprends • Développe tes idées avec l'IA
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# CONNEXION
