import streamlit as st
from google import genai

# ==============================
# CONFIGURATION
# ==============================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# ==============================
# DESIGN
# ==============================

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f8fc;
    }

    .title-box {
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        background: linear-gradient(135deg, #111827, #374151);
        color: white;
        margin-bottom: 25px;
    }

    .title-box h1 {
        font-size: 38px;
        margin-bottom: 5px;
    }

    .title-box p {
        font-size: 16px;
        margin: 0;
    }

    .section-title {
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .info-box {
        padding: 15px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# EN-TÊTE
# ==============================

st.markdown(
    """
    <div class="title-box">
        <h1>🤖 IA-Creator</h1>
        <p>Crée des contenus professionnels avec l'intelligence artificielle</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="info-box">💡 <b>Transforme une simple idée en contenu professionnel.</b></div>',
    unsafe_allow_html=True
)

# ==============================
# CONNEXION GEMINI
# ==============================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error("❌ Impossible de charger la clé Gemini.")
    st.stop()

# ==============================
# OUTIL
# ==============================

st.markdown(
    '<div class="section-title">🚀 Que veux-tu créer ?</div>',
    unsafe_allow_html=True
)

type_creation = st.selectbox(
    "Choisis ton outil",
    [
        "💡 Créer une idée",
        "✍️ Créer un texte",
        "🎬 Créer un script vidéo",
        "🎨 Créer une idée d'affiche",
        "🖼️ Créer un prompt d'image IA"
    ]
)

# ==============================
# STYLE
# ==============================

st.markdown(
    '<div class="section-title">🎨 Choisis un style</div>',
    unsafe_allow_html=True
)

style = st.selectbox(
    "Style",
    [
        "🔥 Viral et accrocheur",
        "💼 Professionnel",
        "🎓 Éducatif",
        "😂 Amusant",
        "❤️ Émotionnel",
        "💎 Premium et élégant",
        "🎬 Cinématographique",
        "📸 Photorealiste",
        "🎨 3D ultra-réaliste"
    ]
)

# ==============================
# PLATEFORME
# ==============================

st.markdown(
    '<div class="section-title">📱 Plateforme</div>',
    unsafe_allow_html=True
)

plateforme = st.selectbox(
    "Où utiliser le contenu ?",
    [
        "TikTok",
        "YouTube",
        "Facebook",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ]
)

# ==============================
# FORMAT IMAGE
# ==============================

format_image = ""

if type_creation == "🖼️ Créer un prompt d'image IA":

    st.markdown(
        '<div class="section-title">📐 Format de l’image</div>',
        unsafe_allow_html=True
    )

    format_image = st.selectbox(
        "Format",
        [
            "1080 × 1080 — Carré",
            "1080 × 1920 — Vertical",
            "1920 × 1080 — Paysage",
            "Portrait",
            "Paysage"
        ]
    )

# ==============================
# DURÉE VIDÉO
# ==============================

duree = ""

if type_creation == "🎬 Créer un script vidéo":

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
            "45 secondes",
            "60 secondes",
            "90 secondes"
        ]
    )

# ==============================
# DEMANDE
# ==============================

st.markdown(
    '<div class="section-title">📝 Ta demande</div>',
    unsafe_allow_html=True
)

sujet = st.text_area(
    "Décris ce que tu veux créer",
    placeholder="Exemple : crée une vidéo TikTok sur 5 outils d'intelligence artificielle utiles.",
    height=160
)

# ==============================
# BOUTON
# ==============================

creer = st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
)

# ==============================
# GÉNÉRATION
# ==============================

if creer:

    if not sujet.strip():

        st.warning("⚠️ Écris d'abord ta demande.")

        st.stop()

    # ==========================
    # IDÉE
    # ==========================

    if type_creation == "💡 Créer une idée":

        prompt = "\n".join([
            "Tu es un expert en créativité, marketing digital et intelligence artificielle.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée une idée originale et réaliste.",
            "",
            "Présente :",
            "1. Nom de l'idée",
            "2. Concept",
            "3. Public cible",
            "4. Comment la réaliser",
            "5. Pourquoi elle est intéressante",
            "6. Accroche",
            "7. Appel à l'action",
            "",
            "Réponds en français."
        ])

    # ==========================
    # TEXTE
    # ==========================

    elif type_creation == "✍️ Créer un texte":

        prompt = "\n".join([
            "Tu es un rédacteur professionnel spécialisé dans le marketing digital et les réseaux sociaux.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée un texte professionnel et accrocheur.",
            "Commence par une accroche forte.",
            "Utilise des phrases simples.",
            "Termine par un appel à l'action.",
            "",
            "Réponds en français."
        ])

    # ==========================
    # SCRIPT VIDÉO
    # ==========================

    elif type_creation == "🎬 Créer un script vidéo":

        prompt = "\n".join([
            "Tu es un scénariste professionnel spécialisé dans TikTok, YouTube Shorts et Facebook Reels.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "Durée : " + duree,
            "",
            "Crée un script vidéo professionnel.",
            "",
            "Pour chaque scène indique :",
            "- Numéro de scène",
            "- Durée",
            "- Image et action",
            "- Narration ou dialogue",
            "- Texte à l'écran",
            "- Effet ou transition",
            "",
            "Commence par une accroche très forte.",
            "Termine par un appel à s'abonner et à commenter.",
            "",
            "Réponds en français."
        ])

    # ==========================
    # AFFICHE
    # ==========================

    elif type_creation == "🎨 Créer une idée d'affiche":

        prompt = "\n".join([
            "Tu es un directeur artistique professionnel spécialisé dans la publicité et le design graphique.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "",
            "Crée un concept complet d'affiche publicitaire.",
            "",
            "Présente :",
            "1. Titre principal",
            "2. Sous-titre",
            "3. Texte publicitaire",
            "4. Couleurs",
            "5. Éléments visuels",
            "6. Disposition",
            "7. Accroche",
            "8. Appel à l'action",
            "9. Prompt pour générer l'affiche avec une IA",
            "",
            "Réponds en français."
        ])

    # ==========================
    # PROMPT IMAGE
    # ==========================

    else:

        prompt = "\n".join([
            "Tu es un expert professionnel en prompt engineering pour la génération d'images avec l'intelligence artificielle.",
            "",
            "Demande : " + sujet,
            "Style : " + style,
            "Plateforme : " + plateforme,
            "Format : " + format_image,
            "",
            "Crée un prompt d'image très détaillé et professionnel.",
            "",
            "Le prompt doit préciser :",
            "1. Sujet principal",
            "2. Personnages ou objets",
            "3. Apparence",
            "4. Vêtements si nécessaire",
            "5. Environnement",
            "6. Arrière-plan",
            "7. Éclairage",
            "8. Composition",
            "9. Angle de caméra",
            "10. Profondeur de champ",
            "11. Style visuel",
            "12. Niveau de détail",
            "13. Qualité visuelle",
            "14. Format",
            "",
            "Crée deux parties :",
            "",
            "PROMPT FINAL",
            "",
            "PROMPT NÉGATIF",
            "",
            "Réponds en français."
        ])

    # ==========================
    # GEMINI
    # ==========================

    try:

        with st.spinner("🤖 IA-Creator travaille..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        if response.text:

            resultat = response.text

            st.success("✅ Création terminée !")

            st.markdown(
                '<div class="section-title">✨ Ton résultat</div>',
                unsafe_allow_html=True
            )

            st.text_area(st.text_area(
    "Résultat",
    value=resultat,
    height=550
)

st.code(resultat, language="text")
            )

            # ======================
            # TÉLÉCHARGEMENT
            # ======================

            st.download_button(
                label="📥 Télécharger le résultat",
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
