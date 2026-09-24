import streamlit as st
from google import genai
import streamlit.components.v1 as components

# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# ============================================
# STYLE
# ============================================

st.markdown("""
<style>
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.login-box {
    background: linear-gradient(135deg, #111827, #2563eb);
    padding: 35px 25px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.login-title {
    font-size: 34px;
    font-weight: 800;
}

.login-text {
    font-size: 16px;
    margin-top: 8px;
}

.hero {
    background: linear-gradient(135deg, #111827, #2563eb);
    padding: 30px 24px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-text {
    font-size: 17px;
}

.section-title {
    font-size: 22px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 48px;
}

.stDownloadButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 48px;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# ÉTAT CONNEXION
# ============================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False

if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = ""

# ============================================
# ÉCRAN CONNEXION / INSCRIPTION
# ============================================

if not st.session_state.connecte:

    st.markdown("""
    <div class="login-box">
        <div class="login-title">🤖 IA-Creator</div>
        <div class="login-text">
            Crée du contenu professionnel avec l'intelligence artificielle
        </div>
    </div>
    """, unsafe_allow_html=True)

    choix = st.radio(
        "Accès",
        ["🔐 Se connecter", "📝 Créer un compte"],
        horizontal=True
    )

    st.markdown(
        "<div class='section-title'>👤 Tes informations</div>",
        unsafe_allow_html=True
    )

    nom = st.text_input(
        "Nom",
        placeholder="Ton nom"
    )

    email = st.text_input(
        "Adresse e-mail",
        placeholder="exemple@email.com"
    )

    mot_de_passe = st.text_input(
        "Mot de passe",
        type="password",
        placeholder="Ton mot de passe"
    )

    if choix == "📝 Créer un compte":

        confirmation = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            placeholder="Confirme ton mot de passe"
        )

        if st.button(
            "🚀 CRÉER MON COMPTE",
            use_container_width=True
        ):

            if not nom.strip():
                st.warning("⚠️ Entre ton nom.")

            elif not email.strip():
                st.warning("⚠️ Entre ton adresse e-mail.")

            elif not mot_de_passe:
                st.warning("⚠️ Entre un mot de passe.")

            elif mot_de_passe != confirmation:
                st.error("❌ Les deux mots de passe sont différents.")

            else:
                st.session_state.connecte = True
                st.session_state.utilisateur = nom

                st.success(
                    "✅ Compte créé pour cette session !"
                )

                st.rerun()

    else:

        if st.button(
            "🔑 SE CONNECTER",
            use_container_width=True
        ):

            if not email.strip():
                st.warning("⚠️ Entre ton adresse e-mail.")

            elif not mot_de_passe:
                st.warning("⚠️ Entre ton mot de passe.")

            else:
                st.session_state.connecte = True
                st.session_state.utilisateur = (
                    nom.strip() if nom.strip() else "Créateur"
                )

                st.success("✅ Connexion réussie !")

                st.rerun()

    st.markdown(
        """
        <div class="footer">
            🔒 Tes informations seront connectées à un vrai système
            de comptes dans l'étape suivante.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# ============================================
# APPLICATION
# ============================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🤖 IA-Creator</div>
    <div class="hero-text">
        Crée du contenu professionnel avec l'intelligence artificielle
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# PROFIL CONNECTÉ
# ============================================

col1, col2 = st.columns([3, 1])

with col1:
    st.write(
        "👋 Bienvenue **"
        + st.session_state.utilisateur
        + "** !"
    )

with col2:
    if st.button("🚪 Sortir"):
        st.session_state.connecte = False
        st.session_state.utilisateur = ""
        st.rerun()

# ============================================
# GEMINI
# ============================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error("❌ Impossible de connecter Gemini.")
    st.info("Vérifie le secret GEMINI_API_KEY dans Streamlit.")
    st.stop()

# ============================================
# HISTORIQUE
# ============================================

if "historique" not in st.session_state:
    st.session_state.historique = []

# ============================================
# OUTIL
# ============================================

st.markdown(
    "<div class='section-title'>🚀 Que veux-tu créer ?</div>",
    unsafe_allow_html=True
)

outil = st.selectbox(
    "Choisis un outil",
    [
        "Créer une idée",
        "Créer un texte",
        "Créer un script vidéo",
        "Créer une idée d'affiche",
        "Créer un prompt d'image IA"
    ],
    label_visibility="collapsed"
)

# ============================================
# STYLE
# ============================================

st.markdown(
    "<div class='section-title'>🎨 Choisis ton style</div>",
    unsafe_allow_html=True
)

style = st.selectbox(
    "Style",
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
    ],
    label_visibility="collapsed"
)

# ============================================
# PLATEFORME
# ============================================

st.markdown(
    "<div class='section-title'>📱 Plateforme</div>",
    unsafe_allow_html=True
)

plateforme = st.selectbox(
    "Plateforme",
    [
        "TikTok",
        "YouTube",
        "Facebook",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ],
    label_visibility="collapsed"
)

# ============================================
# FORMAT IMAGE
# ============================================

format_image = ""

if outil == "Créer un prompt d'image IA":

    st.markdown(
        "<div class='section-title'>📐 Format de l'image</div>",
        unsafe_allow_html=True
    )

    format_image = st.selectbox(
        "Format",
        [
            "1080 x 1080 - Carré",
            "1080 x 1920 - Vertical",
            "1920 x 1080 - Paysage"
        ],
        label_visibility="collapsed"
    )

# ============================================
# DURÉE VIDÉO
# ============================================

duree = ""

if outil == "Créer un script vidéo":

    st.markdown(
        "<div class='section-title'>⏱️ Durée de la vidéo</div>",
        unsafe_allow_html=True
    )

    duree = st.selectbox(
        "Durée",
        [
            "10 secondes",
            "15 secondes",
            "30 secondes",
            "60 secondes"
        ],
        label_visibility="collapsed"
    )

# ============================================
# DEMANDE
# ============================================

st.markdown(
    "<div class='section-title'>📝 Ta demande</div>",
    unsafe_allow_html=True
)

sujet = st.text_area(
    "Ta demande",
    height=150,
    placeholder="Exemple : crée une vidéo sur l'intelligence artificielle",
    label_visibility="collapsed"
)

# ============================================
# CRÉATION
# ============================================

    if st.button("🗑️ Effacer l'historique"):

        st.session_state.historique = []

        st.rerun()

# ============================================
# PIED DE PAGE
# ============================================

st.markdown(
    """
    <div class="footer">
        🤖 IA-Creator · Crée plus vite avec l'IA
    </div>
    """,
    unsafe_allow_html=True
)
