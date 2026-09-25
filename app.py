import streamlit as st
import streamlit.components.v1 as components
from google import genai
from supabase import create_client

# ============================================================
# IA-CREATOR
# Comptes réels avec Supabase + génération avec Gemini
# ============================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f5f8ff 0%, #eef3ff 100%);
    }

    .hero {
        background: linear-gradient(135deg, #14213d, #2563eb);
        padding: 45px 25px;
        border-radius: 28px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(37, 99, 235, 0.20);
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 10px;
        font-weight: 800;
    }

    .hero p {
        font-size: 20px;
        margin: 0;
        opacity: 0.95;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #172033;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .info-box {
        background: #e7f0ff;
        border-radius: 18px;
        padding: 18px;
        color: #12508b;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .success-box {
        background: #e8f8ee;
        border-radius: 18px;
        padding: 18px;
        color: #146c35;
        margin-bottom: 20px;
    }

    .account-box {
        background: white;
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.06);
    }

    footer {
        text-align: center;
        color: #737b8c;
        margin-top: 50px;
        padding-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
        min-height: 45px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# INITIALISATION SUPABASE
# ============================================================

try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception as e:
    st.error("❌ Impossible de connecter Supabase.")
    st.info("Vérifie les secrets SUPABASE_URL et SUPABASE_KEY dans Streamlit.")
    st.stop()


# ============================================================
# INITIALISATION GEMINI
# ============================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ La clé GEMINI_API_KEY est introuvable.")
    st.stop()


# ============================================================
# SESSION
# ============================================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False

if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

if "email_utilisateur" not in st.session_state:
    st.session_state.email_utilisateur = ""

if "historique" not in st.session_state:
    st.session_state.historique = []


# ============================================================
# TENTATIVE DE RECUPERATION DE SESSION SUPABASE
# ============================================================

try:
    session_response = supabase.auth.get_session()

    if session_response and session_response.user:
        st.session_state.connecte = True
        st.session_state.utilisateur = session_response.user
        st.session_state.email_utilisateur = session_response.user.email or ""

except Exception:
    pass


# ============================================================
# PAGE DE CONNEXION / INSCRIPTION
# ============================================================

if not st.session_state.connecte:

    st.markdown("""
    <div class="hero">
        <h1>🤖 IA-Creator</h1>
        <p>Crée avec l'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🔐 Accéder à IA-Creator</div>',
        unsafe_allow_html=True
    )

    choix = st.radio(
        "Choisis une option",
        ["🔐 Se connecter", "📝 Créer un compte"],
        horizontal=True
    )

    # ========================================================
    # CONNEXION
    # ========================================================

    if choix == "🔐 Se connecter":

        st.markdown(
            '<div class="section-title">👤 Tes informations</div>',
            unsafe_allow_html=True
        )

        email = st.text_input(
            "Adresse e-mail",
            placeholder="Exemple : exemple@gmail.com"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="Entre ton mot de passe"
        )

        if st.button("🔓 SE CONNECTER", use_container_width=True):

            if not email or not password:
                st.warning("⚠️ Entre ton adresse e-mail et ton mot de passe.")

            else:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    if response.user:
                        st.session_state.connecte = True
                        st.session_state.utilisateur = response.user
                        st.session_state.email_utilisateur = response.user.email or ""

                        st.success("✅ Connexion réussie !")
                        st.rerun()

                except Exception as e:
                    message = str(e)

                    if "Email not confirmed" in message:
                        st.error(
                            "📧 Ton adresse e-mail n'est pas encore confirmée. "
                            "Vérifie ta boîte e-mail."
                        )
                    else:
                        st.error(
                            "❌ Adresse e-mail ou mot de passe incorrect."
                        )

    # ========================================================
    # INSCRIPTION
    # ========================================================

    else:

        st.markdown(
            '<div class="section-title">📝 Créer ton compte</div>',
            unsafe_allow_html=True
        )

        nom = st.text_input(
            "Nom",
            placeholder="Exemple : Issa"
        )

        email = st.text_input(
            "Adresse e-mail",
            placeholder="Exemple : exemple@gmail.com"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="Minimum 6 caractères"
        )

        password2 = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            placeholder="Répète ton mot de passe"
        )

        if st.button("📝 CRÉER MON COMPTE", use_container_width=True):

            if not nom or not email or not password or not password2:
                st.warning("⚠️ Remplis tous les champs.")

            elif len(password) < 6:
                st.warning(
                    "⚠️ Le mot de passe doit contenir au moins 6 caractères."
                )

            elif password != password2:
                st.error("❌ Les deux mots de passe sont différents.")

            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": email.strip(),
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": nom.strip()
                            }
                        }
                    })

                    if response.user:

                        # Si Supabase demande une confirmation e-mail,
                        # aucune session ne sera créée immédiatement.
                        if response.session is None:
                            st.success(
                                "✅ Compte créé avec succès !"
                            )

                            st.info(
                                "📧 Un e-mail de confirmation peut t'être envoyé. "
                                "Confirme ton adresse e-mail puis connecte-toi."
                            )

                        else:
                            st.session_state.connecte = True
                            st.session_state.utilisateur = response.user
                            st.session_state.email_utilisateur = (
                                response.user.email or ""
                            )

                            st.success("🎉 Bienvenue sur IA-Creator !")
                            st.rerun()

                except Exception as e:
                    message = str(e)

                    if "already registered" in message.lower():
                        st.error(
                            "❌ Cette adresse e-mail possède déjà un compte."
                        )
                    else:
                        st.error(
                            "❌ Impossible de créer le compte."
                        )

    st.markdown("""
    <div class="info-box">
        🔒 Tes comptes sont maintenant gérés par Supabase.
        <br><br>
        Tes identifiants ne sont pas enregistrés dans
