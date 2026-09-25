import streamlit as st
import streamlit.components.v1 as components
from google import genai
from supabase import create_client
import html
import json


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background: #f7f9fc;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #2563eb);
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.9;
    }

    .section-title {
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .info-box {
        padding: 15px;
        border-radius: 12px;
        background: #eef4ff;
        border-left: 5px solid #2563eb;
        margin: 10px 0;
    }

    .success-box {
        padding: 15px;
        border-radius: 12px;
        background: #ecfdf5;
        border-left: 5px solid #10b981;
        margin: 10px 0;
    }

    footer {
        text-align: center;
        margin-top: 40px;
        color: #777;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONNEXION SUPABASE
# ============================================================

try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        supabase_url,
        supabase_key
    )

except Exception as e:
    st.error("Erreur de connexion à Supabase.")
    st.stop()


# ============================================================
# CONNEXION GEMINI
# ============================================================

try:
    gemini_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=gemini_key
    )

except Exception:
    st.error("Erreur avec la clé Gemini.")
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
# FONCTION : CHARGER L'HISTORIQUE
# ============================================================

def charger_historique(user_id):
    try:
        resultat = (
            supabase
            .table("historique")
            .select("*")
            .eq("user_id", str(user_id))
            .order("created_at", desc=True)
            .execute()
        )

        return resultat.data or []

    except Exception:
        return []


# ============================================================
# FONCTION : SAUVEGARDER DANS L'HISTORIQUE
# ============================================================

def sauvegarder_historique(
    user_id,
    mode,
    style,
    plateforme,
    demande,
    resultat
):
    try:
        supabase.table("historique").insert(
            {
                "user_id": str(user_id),
                "mode": mode,
                "style": style,
                "plateforme": plateforme,
                "demande": demande,
                "resultat": resultat
            }
        ).execute()

        return True

    except Exception as e:
        st.warning("Le résultat a été créé, mais n'a pas pu être enregistré.")
        return False


# ============================================================
# PAGE DE CONNEXION / INSCRIPTION
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
        '<div class="section-title">🔐 Connexion à ton compte</div>',
        unsafe_allow_html=True
    )

    onglet_connexion, onglet_inscription = st.tabs(
        ["🔑 Se connecter", "📝 Créer un compte"]
    )

    # --------------------------------------------------------
    # CONNEXION
    # --------------------------------------------------------

    with onglet_connexion:

        email_connexion = st.text_input(
            "📧 Adresse email",
            key="email_connexion"
        )

        password_connexion = st.text_input(
            "🔒 Mot de passe",
            type="password",
            key="password_connexion"
        )

        if st.button(
            "🚀 Se connecter",
            use_container_width=True
        ):

            if not email_connexion or not password_connexion:

                st.warning(
                    "Entre ton email et ton mot de passe."
                )

            else:

                try:

                    reponse = supabase.auth.sign_in_with_password(
                        {
                            "email": email_connexion.strip(),
                            "password": password_connexion
                        }
                    )

                    if reponse.user:

                        st.session_state.connecte = True
                        st.session_state.utilisateur = reponse.user
                        st.session_state.email_utilisateur = email_connexion.strip()

                        st.session_state.historique = charger_historique(
                            reponse.user.id
                        )

                        st.success("Connexion réussie !")
                        st.rerun()

                    else:

                        st.error(
                            "Impossible de se connecter."
                        )

                except Exception as e:

                    st.error(
                        "Email ou mot de passe incorrect."
                    )

    # --------------------------------------------------------
    # INSCRIPTION
    # --------------------------------------------------------

    with onglet_inscription:

        nom_inscription = st.text_input(
            "👤 Ton nom",
            key="nom_inscription"
        )

        email_inscription = st.text_input(
            "📧 Ton email",
            key="email_inscription"
        )

        password_inscription = st.text_input(
            "🔒 Crée un mot de passe",
            type="password",
            key="password_inscription"
        )

        password_confirmation = st.text_input(
            "🔒 Confirme le mot de passe",
            type="password",
            key="password_confirmation"
        )

        if st.button(
            "✨ Créer mon compte",
            use_container_width=True
        ):

            if not nom_inscription:
                st.warning("Entre ton nom.")

            elif not email_inscription:
                st.warning("Entre ton email.")

            elif not password_inscription:
                st.warning("Entre un mot de passe.")

            elif password_inscription != password_confirmation:
                st.error("Les deux mots de passe sont différents.")

            elif len(password_inscription) < 6:
                st.warning(
                    "Le mot de passe doit contenir au moins 6 caractères."
                )

            else:

                try:

                    reponse = supabase.auth.sign_up(
                        {
                            "email": email_inscription.strip(),
                            "password": password_inscription,
                            "options": {
                                "data": {
                                    "full_name": nom_inscription.strip()
                                }
                            }
                        }
                    )

                    if reponse.user:

                        if reponse.session:

                            st.session_state.connecte = True
                            st.session_state.utilisateur = reponse.user
                            st.session_state.email_utilisateur = email_inscription.strip()
                            st.session_state.historique = []

                            st.success(
                                "Compte créé avec succès !"
                            )

                            st.rerun()

                        else:

                            st.success(
                                "Compte créé ! Vérifie ton email si une confirmation est demandée, puis connecte-toi."
                            )

                    else:

                        st.error(
                            "Impossible de créer le compte."
                        )

                except Exception as e:

                    st.error(
                        "Impossible de créer le compte. Vérifie les informations."
                    )

    st.markdown(
        """
        <footer>
            🤖 IA-Creator • Création assistée par intelligence artificielle
        </footer>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# UTILISATEUR CONNECTÉ
# ============================================================

user = st.session_state.utilisateur


# ============================================================
# EN-TÊTE
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🤖 IA-Creator</h1>
        <p>Crée avec l'intelligence artificielle</p>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '<div class="success-box">✅ Tu es connecté à ton compte.</div>',
        unsafe_allow_html=True
    )

    st.write(
        "👋 Bienvenue dans IA-Creator !"
    )

with col2:

    if st.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.connecte = False
        st.session_state.utilisateur = None
        st.session_state.email_utilisateur = ""
        st.session_state.historique = []

        st.rerun()


# ============================================================
# OUTILS IA
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Que veux-tu créer ?</div>',
    unsafe_allow_html=True
)

outil = st.selectbox(
    "Choisis un outil",
    [
        "💡 Créer une idée",
        "✍️ Créer un texte",
        "🎬 Créer un script vidéo",
        "🎨 Créer une idée d'affiche",
        "🖼️ Créer un prompt d'image IA"
    ]
)


# ============================================================
# STYLE
# ============================================================

style = st.selectbox(
    "🎨 Choisis le style",
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


# ============================================================
# PLATEFORME
# ============================================================

plateforme = st.selectbox(
    "📱 Plateforme",
    [
        "TikTok",
        "Facebook",
        "YouTube",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ]
)


# ============================================================
# OPTIONS VIDÉO
# ============================================================

duree = ""

if outil == "🎬 Créer un script vidéo":

    duree = st.selectbox(
        "⏱️ Durée de la vidéo",
        [
            "30 secondes",
            "60 secondes",
            "90 secondes",
            "2 minutes",
            "3 minutes"
        ]
    )


# ============================================================
# FORMAT IMAGE
# ============================================================

format_image = ""

if outil in [
    "🎨 Créer une idée d'affiche",
    "🖼️ Créer un prompt d'image IA"
]:

    format_image = st.selectbox(
        "📐 Format de l'image",
        [
            "Vertical 9:16",
            "Carré 1:1",
            "Horizontal 16:9",
            "Affiche 4:5"
        ]
    )


# ============================================================
# DEMANDE
# ============================================================

st.markdown(
    '<div class="section-title">📝 Ta demande</div>',
    unsafe_allow_html=True
)

demande = st.text_area(
    "Explique ce que tu veux créer",
    placeholder="Exemple : crée une vidéo sur les avantages de l'intelligence artificielle...",
    height=160
)


# ============================================================
# CRÉATION
# ============================================================

if st.button(
    "✨ Créer avec l'IA",
    use_container_width=True
):

    if not demande.strip():

        st.warning(
            "Écris d'abord ce que tu veux créer."
        )

    else:

        with st.spinner("🤖 L'IA est en train de créer..."):

            if outil == "💡 Créer une idée":

                instruction = (
                    "Tu es un expert en création de contenu. "
                    "Donne une idée originale et concrète sur le sujet suivant : "
                    + demande
                    + ". Style : "
                    + style
                    + ". Plateforme : "
                    + plateforme
                    + ". Donne un titre accrocheur, le concept, "
                    "l'accroche et une explication claire."
                )

            elif outil == "✍️ Créer un texte":

                instruction = (
                    "Tu es un expert en rédaction et réseaux sociaux. "
                    "Rédige un texte professionnel et engageant sur : "
                    + demande
                    + ". Style : "
                    + style
                    + ". Plate
