import streamlit as st
from google import genai

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #666666;
    margin-bottom: 30px;
}

.info-box {
    padding: 18px;
    border-radius: 15px;
    background-color: #f5f7fb;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITRE
# =========================================================

st.markdown(
    '<div class="main-title">🤖 IA-Creator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Apprends • Crée • Développe tes idées avec l’IA</div>',
    unsafe_allow_html=True
)

# =========================================================
# CONNEXION GEMINI
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:

    st.error(
        "❌ Impossible de connecter IA-Creator à Gemini. "
        "Vérifie les Secrets de Streamlit."
    )

    st.stop()

# =========================================================
# CHOIX DE L'OUTIL
# =========================================================

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

# =========================================================
# DESCRIPTION DES OUTILS
# =========================================================

descriptions = {

    "💡 Créer une idée":
        "Trouve rapidement des idées originales pour tes projets, contenus ou activités.",

    "✍️ Créer un texte":
        "Crée des textes professionnels pour TikTok, Facebook, WhatsApp, YouTube ou Instagram.",

    "🎬 Créer un script vidéo":
        "Transforme ton idée en scénario vidéo avec scènes, narration, dialogues et appel à l'action.",

    "🎨 Créer une idée d'affiche":
        "Obtiens une conception complète d'affiche avec titre, couleurs, éléments visuels et texte publicitaire."
}

st.info(descriptions[type_creation])

# =========================================================
# DEMANDE UTILISATEUR
# =========================================================

st.subheader("📝 Ta demande")

sujet = st.text_area(
    "Décris ce que tu veux créer",
    placeholder=(
        "Exemple : "
        "Je veux créer une vidéo TikTok pour promouvoir une formation en intelligence artificielle."
    ),
    height=150
)

# =========================================================
# BOUTON
# =========================================================

creer = st.button(
    "✨ Créer avec l'IA",
    use_container_width=True
)

# =========================================================
# TRAITEMENT
# =========================================================

if creer:

    if not sujet.strip():

        st.warning(
            "⚠️ Écris d'abord ce que tu veux créer."
        )

        st.stop()

    # -----------------------------------------------------
    # PROMPT : IDÉE
    # -----------------------------------------------------

    if type_creation == "💡 Créer une idée":

        prompt = f"""
Tu es un expert mondial en créativité, marketing digital,
intelligence artificielle et création de contenu.

L'utilisateur veut créer une idée à partir de cette demande :

{sujet}

Propose une idée originale, réaliste et intéressante.

Présente clairement :

1. NOM DE L'IDÉE
2. CONCEPT
3. COMMENT LA RÉALISER
4. POURQUOI ELLE PEUT INTÉRESSER LE PUBLIC
5. ACCROCHE PUISSANTE
6. CONSEIL POUR LA RENDRE PLUS ATTRACTIVE

Réponds en français.
"""

    # -----------------------------------------------------
    # PROMPT : TEXTE
    # -----------------------------------------------------

    elif type_creation == "✍️ Créer un texte":

        prompt = f"""
Tu es un rédacteur professionnel spécialisé dans
le marketing digital et les réseaux sociaux.

Voici la demande :

{sujet}

Crée un texte professionnel, naturel et convaincant.

Le texte doit :

- commencer par une accroche forte ;
- être facile à comprendre ;
- utiliser des phrases courtes ;
- donner envie de continuer à lire ;
- terminer par un appel à l'action.

Réponds en français.
"""

    # -----------------------------------------------------
    # PROMPT : SCRIPT VIDÉO
    # -----------------------------------------------------

    elif type_creation == "🎬 Créer un script vidéo":

        prompt = f"""
Tu es un scénariste professionnel spécialisé dans
TikTok, YouTube Shorts, Facebook Reels et vidéos virales.

Sujet :

{sujet}

Crée un script vidéo professionnel et dynamique.

STRUCTURE :

🎬 SCÈNE 1
Image / action :
Narration / dialogue :
Texte à l'écran :
Effet ou transition :

🎬 SCÈNE 2
Image / action :
Narration / dialogue :
Texte à l'écran :
Effet ou transition :

🎬 SCÈNE 3
Image / action :
Narration / dialogue :
Texte à l'écran :
Effet ou transition :

🎬 SCÈNE 4
Image / action :
Narration / dialogue :
Texte à l'écran :
Effet ou transition :

🎬 SCÈNE 5
Image / action :
Narration / dialogue :
Texte à l'écran :
Effet ou transition :

TERMINE PAR :

🔥 Une phrase forte
📢 Un appel à s'abonner
💬 Un appel à commenter

Le script doit être facile à utiliser pour créer
une vidéo avec CapCut ou un générateur vidéo IA.

Réponds en français.
"""

    # -----------------------------------------------------
    # PROMPT : AFFICHE
    # -----------------------------------------------------

    else:

        prompt = f"""
Tu es un directeur artistique professionnel,
expert en publicité, design graphique et marketing.

Voici la demande :

{sujet}

Crée un concept complet d'affiche publicitaire.

Présente :

1. 🎯 TITRE PRINCIPAL
2. 📝 SOUS-TITRE
3. 📢 TEXTE PUBLICITAIRE
4. 🎨 COULEURS
5. 🖼️ ÉLÉMENTS VISUELS
6. 📐 DISPOSITION DE L'AFFICHE
7. 🔥 ACCROCHE
8. 📞 APPEL À L'ACTION

L'affiche doit être moderne, professionnelle,
lisible sur téléphone et adaptée à Facebook,
TikTok, WhatsApp et Instagram.

Réponds en français.
"""

    # =====================================================
    # APPEL GEMINI
    # =====================================================

    try:

        with st.spinner(
            "🤖 IA-Creator prépare ta création..."
        ):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        # -------------------------------------------------
        # RÉSULTAT
        # -------------------------------------------------

        if response.text:

            resultat = response.text

            st.success("✅ Création terminée !")

            st.subheader("✨ Ton résultat")

            # Zone avec bouton de copie intégré
            st.code(
                resultat,
                language="
