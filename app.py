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
# STYLE PROFESSIONNEL
# ============================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #111827, #2563eb);
    padding: 30px 24px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.20);
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-text {
    font-size: 17px;
    opacity: 0.92;
}

.section-title {
    font-size: 22px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
}

.info-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
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

textarea {
    border-radius: 12px !important;
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
# EN-TÊTE
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
# CONNEXION GEMINI
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
    '<div class="section-title">🚀 Que veux-tu créer ?</div>',
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
    '<div class="section-title">🎨 Choisis ton style</div>',
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
    '<div class="section-title">📱 Plateforme</div>',
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
# OPTIONS IMAGE
# ============================================

format_image = ""

if outil == "Créer un prompt d'image IA":

    st.markdown(
        '<div class="section-title">📐 Format de l'image</div>',
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
# OPTIONS VIDÉO
# ============================================

duree = ""

if outil == "Créer un script vidéo":

    st.markdown(
        '<div class="section-title">⏱️ Durée de la vidéo</div>',
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
    '<div class="section-title">📝 Ta demande</div>',
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

if st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
):

    if not sujet.strip():

        st.warning("⚠️ Écris d'abord ta demande.")
        st.stop()

    # ========================================
    # IDÉE
    # ========================================

    if outil == "Créer une idée":

        prompt = (
            "Tu es un expert en création de contenu.\n\n"
            "Crée une idée originale à partir de cette demande :\n"
            + sujet
            + "\n\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\nDonne :\n"
            "1. Titre\n"
            "2. Concept\n"
            "3. Accroche\n"
            "4. Déroulement\n"
            "5. Appel à l'action\n"
            "6. Hashtags\n\n"
            "Réponds en français."
        )

    # ========================================
    # TEXTE
    # ========================================

    elif outil == "Créer un texte":

        prompt = (
            "Tu es un rédacteur professionnel spécialisé "
            "dans les réseaux sociaux.\n\n"
            "Crée un texte à partir de cette demande :\n"
            + sujet
            + "\n\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\n"
            "Le texte doit être naturel, clair et accrocheur.\n"
            "Termine par un appel à l'action.\n"
            "Ajoute des hashtags pertinents.\n\n"
            "Réponds en français."
        )

    # ========================================
    # SCRIPT VIDÉO
    # ========================================

    elif outil == "Créer un script vidéo":

        prompt = (
            "Tu es un scénariste professionnel spécialisé "
            "dans TikTok, YouTube Shorts et Facebook Reels.\n\n"
            "Crée un script vidéo professionnel et dynamique.\n\n"
            "SUJET : "
            + sujet
            + "\nPLATEFORME : "
            + plateforme
            + "\nSTYLE : "
            + style
            + "\nDURÉE : "
            + duree
            + "\n\n"
            "Le script doit être directement utilisable avec CapCut.\n\n"
            "Commence par une accroche très forte.\n"
            "Respecte la durée demandée.\n"
            "Utilise des phrases courtes et dynamiques.\n\n"
            "Pour chaque scène indique exactement :\n\n"
            "SCÈNE 1\n"
            "Durée :\n"
            "Ce que l'on voit à l'écran :\n"
            "Narration ou dialogue :\n"
            "Texte à l'écran :\n"
            "Effet ou transition :\n"
            "Ambiance sonore :\n\n"
            "Continue avec les scènes suivantes "
            "jusqu'à couvrir toute la durée.\n\n"
            "À la fin ajoute :\n"
            "TITRE DE LA VIDÉO\n"
            "LÉGENDE\n"
            "HASHTAGS\n"
            "APPEL À L'ACTION\n\n"
            "L'appel à l'action doit encourager les spectateurs "
            "à s'abonner, aimer la vidéo et commenter.\n\n"
            "Réponds uniquement en français."
        )

    # ========================================
    # AFFICHE
    # ========================================

    elif outil == "Créer une idée d'affiche":

        prompt = (
            "Tu es un directeur artistique professionnel.\n\n"
            "Crée une idée d'affiche professionnelle.\n\n"
            "Sujet : "
            + sujet
            + "\nPlateforme : "
            + plateforme
            + "\nStyle : "
            + style
            + "\n\n"
            "Donne :\n"
            "1. Concept visuel\n"
            "2. Sujet principal\n"
            "3. Arrière-plan\n"
            "4. Éclairage\n"
            "5. Couleurs\n"
            "6. Texte principal\n"
            "7. Texte secondaire\n"
            "8. Composition\n"
            "9. Éléments graphiques\n"
            "10. Appel à l'action\n\n"
            "Réponds en français."
        )

    # ========================================
    # PROMPT IMAGE
    # ========================================

    else:

        prompt = (
            "Tu es un expert professionnel en création "
            "de prompts pour générateurs d'images IA.\n\n"
            "Crée un prompt d'image détaillé et professionnel.\n\n"
            "Sujet : "
            + sujet
            + "\nStyle : "
            + style
            + "\nFormat : "
            + format_image
            + "\nPlateforme : "
            + plateforme
            + "\n\n"
            "Décris :\n"
            "- sujet principal\n"
            "- apparence\n"
            "- vêtements\n"
            "- posture\n"
            "- expression\n"
            "- environnement\n"
            "- arrière-plan\n"
            "- éclairage\n"
            "- couleurs\n"
            "- composition\n"
            "- profondeur de champ\n"
            "- ambiance\n"
            "- détails visuels\n"
            "- qualité\n\n"
            "Donne uniquement le prompt final prêt à copier.\n"
            "Réponds en français."
        )

    # ========================================
    # GÉNÉRATION
    # ========================================

    try:

        with st.spinner("🤖 Gemini est en train de créer..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        resultat = response.text

        # ====================================
        # HISTORIQUE
        # ====================================

        st.session_state.historique.insert(
            0,
            {
                "outil": outil,
                "sujet": sujet,
                "style": style,
                "plateforme": plateforme,
                "resultat": resultat
            }
        )

        st.success("✅ Création terminée !")

        st.markdown(
            '<div class="section-title">✨ Ton résultat</div>',
            unsafe_allow_html=True
        )

        st.text_area(
            "Résultat",
            value=resultat,
            height=350,
            key="resultat_ia"
        )

        # ====================================
        # COPIER
        # ====================================

        resultat_js = (
            resultat
            .replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("${", "\\${")
        )

        components.html(
            """
            <button
                onclick="copierResultat()"
                style="
                    width:100%;
                    padding:14px;
                    background:#2563eb;
                    color:white;
                    border:none;
                    border-radius:12px;
                    font-size:16px;
                    font-weight:bold;
                    cursor:pointer;
                "
            >
                📋 COPIER LE RÉSULTAT
            </button>

            <script>
            function copierResultat() {

                const texte = `""" + resultat_js + """`;

                navigator.clipboard.writeText(texte).then(function() {

                    alert("✅ Résultat copié !");

                }).catch(function() {

                    alert("❌ Impossible de copier automatiquement.");

                });
            }
            </script>
            """,
            height=65
        )

        # ====================================
        # TÉLÉCHARGER
        # ====================================

        st.download_button(
            label="📥 Télécharger le résultat",
            data=resultat,
            file_name="ia_creator_resultat.txt",
            mime="text/plain",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            "❌ Une
