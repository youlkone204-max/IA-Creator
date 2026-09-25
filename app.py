import streamlit as st
import streamlit.components.v1 as components
from google import genai
from supabase import create_client

# ============================================================
# IA-CREATOR
# ============================================================

st.set_page_config(
    page_title="IA-Creator",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# STYLE
# ============================================================

CSS = """
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
    margin: 15px 0;
}

.success-box {
    background: #e8f8ee;
    border-radius: 18px;
    padding: 18px;
    color: #146c35;
    margin-bottom: 20px;
}

footer {
    text-align: center;
    color: #737b8c;
    margin-top: 50px;
    padding-bottom: 20px;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# SUPABASE
# ============================================================

try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error("❌ Impossible de connecter Supabase.")
    st.info("Vérifie SUPABASE_URL et SUPABASE_KEY dans Secrets.")
    st.stop()

# ============================================================
# GEMINI
# ============================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("❌ GEMINI_API_KEY est introuvable.")
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
# RECUPERER LA SESSION SUPABASE
# ============================================================

try:
    session_response = supabase.auth.get_session()

    if session_response and session_response.user:
        st.session_state.connecte = True
        st.session_state.utilisateur = session_response.user
        st.session_state.email_utilisateur = (
            session_response.user.email or ""
        )
except Exception:
    pass

# ============================================================
# CONNEXION / INSCRIPTION
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

    choix = st.radio(
        "Choisis une option",
        ["🔐 Se connecter", "📝 Créer un compte"],
        horizontal=True
    )

    # --------------------------------------------------------
    # CONNEXION
    # --------------------------------------------------------

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

        if st.button(
            "🔓 SE CONNECTER",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "⚠️ Entre ton adresse e-mail et ton mot de passe."
                )

            else:

                try:

                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    if response.user:

                        st.session_state.connecte = True
                        st.session_state.utilisateur = response.user
                        st.session_state.email_utilisateur = (
                            response.user.email or ""
                        )

                        st.success("✅ Connexion réussie !")
                        st.rerun()

                except Exception as e:

                    message = str(e)

                    if "Email not confirmed" in message:

                        st.error(
                            "📧 Ton adresse e-mail n'est pas encore confirmée."
                        )

                    else:

                        st.error(
                            "❌ Adresse e-mail ou mot de passe incorrect."
                        )

    # --------------------------------------------------------
    # INSCRIPTION
    # --------------------------------------------------------

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

        if st.button(
            "📝 CRÉER MON COMPTE",
            use_container_width=True
        ):

            if not nom or not email or not password or not password2:

                st.warning("⚠️ Remplis tous les champs.")

            elif len(password) < 6:

                st.warning(
                    "⚠️ Le mot de passe doit contenir au moins 6 caractères."
                )

            elif password != password2:

                st.error(
                    "❌ Les deux mots de passe sont différents."
                )

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

                        if response.session is None:

                            st.success(
                                "✅ Compte créé avec succès !"
                            )

                            st.info(
                                "📧 Vérifie ta boîte e-mail pour confirmer "
                                "ton adresse, puis connecte-toi."
                            )

                        else:

                            st.session_state.connecte = True
                            st.session_state.utilisateur = response.user
                            st.session_state.email_utilisateur = (
                                response.user.email or ""
                            )

                            st.success(
                                "🎉 Bienvenue sur IA-Creator !"
                            )

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

    st.markdown(
        """
        <div class="info-box">
            🔒 Tes comptes sont gérés par Supabase.
            <br><br>
            Tes identifiants ne sont pas enregistrés dans le code.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <footer>
            🤖 IA-Creator<br>
            Crée • Apprends • Développe tes idées avec l'IA
        </footer>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# ============================================================
# UTILISATEUR CONNECTE
# ============================================================

user = st.session_state.utilisateur

nom_utilisateur = "Créateur"

try:

    metadata = user.user_metadata or {}

    if metadata.get("full_name"):
        nom_utilisateur = metadata["full_name"]

except Exception:
    pass

# ============================================================
# EN-TETE
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

st.markdown(
    f"""
    <div class="success-box">
        👋 Bienvenue <strong>{nom_utilisateur}</strong> !
        <br>
        📧 {st.session_state.email_utilisateur}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DECONNEXION
# ============================================================

if st.button(
    "🚪 Se déconnecter",
    use_container_width=True
):

    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.connecte = False
    st.session_state.utilisateur = None
    st.session_state.email_utilisateur = ""

    st.rerun()

st.divider()

# ============================================================
# OUTILS
# ============================================================

st.markdown(
    '<div class="section-title">🛠️ Tes outils IA</div>',
    unsafe_allow_html=True
)

outil = st.selectbox(
    "Choisis ce que tu veux créer",
    [
        "💡 Créer une idée",
        "✍️ Créer un texte",
        "🎬 Créer un script vidéo",
        "🎨 Créer une idée d’affiche",
        "🖼️ Créer un prompt d’image IA"
    ]
)

style = st.selectbox(
    "🎨 Choisis un style",
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

plateforme = st.selectbox(
    "📱 Pour quelle plateforme ?",
    [
        "TikTok",
        "YouTube",
        "Facebook",
        "Instagram",
        "WhatsApp",
        "Toutes les plateformes"
    ]
)

format_image = ""

if "prompt d’image" in outil.lower() or "affiche" in outil.lower():

    format_image = st.selectbox(
        "📐 Format",
        [
            "1080 x 1080 - Carré",
            "1080 x 1920 - Vertical",
            "1920 x 1080 - Paysage"
        ]
    )

duree_video = ""

if "script vidéo" in outil.lower():

    duree_video = st.selectbox(
        "⏱️ Durée de la vidéo",
        [
            "10 secondes",
            "15 secondes",
            "30 secondes",
            "60 secondes"
        ]
    )

demande = st.text_area(
    "📝 Ta demande",
    placeholder="Exemple : crée une idée de vidéo sur l'intelligence artificielle...",
    height=150
)

# ============================================================
# GENERATION
# ============================================================

if st.button(
    "✨ CRÉER AVEC L'IA",
    use_container_width=True
):

    if not demande.strip():

        st.warning(
            "⚠️ Écris d'abord ce que tu veux créer."
        )

    else:

        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        if "Créer une idée" in outil:

            instruction = "\n".join([
                "Tu es un expert en création de contenu.",
                "",
                "Crée une idée de contenu originale.",
                "",
                "Demande :",
                demande,
                "",
                "Plateforme :",
                plateforme,
                "",
                "Style :",
                style,
                "",
                "Donne :",
                "1. Le concept",
                "2. Le titre",
                "3. L'accroche",
                "4. Le déroulement",
                "5. Un appel à l'action",
                "",
                "Réponds en français."
            ])

        elif "Créer un texte" in outil:

            instruction = "\n".join([
                "Tu es un expert en rédaction et création de contenu.",
                "",
                "Crée un texte prêt à publier.",
                "",
                "Demande :",
                demande,
                "",
                "Plateforme :",
                plateforme,
                "",
                "Style :",
                style,
                "",
                "Le texte doit être naturel, professionnel et accrocheur.",
                "Réponds en français."
            ])

        elif "script vidéo" in outil.lower():

            instruction = "\n".join([
                "Tu es un expert en création de scripts vidéo.",
                "",
                "Crée un script vidéo complet.",
                "",
                "Sujet :",
                demande,
                "",
                "Plateforme :",
                plateforme,
                "",
                "Style :",
                style,
                "",
                "Durée :",
                duree_video,
                "",
                "Structure :",
                "- Accroche",
                "- Scène 1",
                "- Scène 2",
                "- Scène 3",
                "- Conclusion",
                "- Appel à l'action",
                "",
                "Le script doit être facile à filmer.",
                "Réponds en français."
            ])

        elif "affiche" in outil.lower():

            instruction = "\n".join([
                "Tu es un directeur artistique professionnel.",
                "",
                "Crée une idée d'affiche très professionnelle.",
                "",
                "Sujet :",
                demande,
                "",
                "Plateforme :",
                plateforme,
                "",
                "Style :",
                style,
                "",
                "Format :",
                format_image,
                "",
                "Décris :",
                "- Le personnage ou sujet principal",
                "- La position",
                "- L'arrière-plan",
                "- Les couleurs",
                "- L'éclairage",
                "- Les éléments graphiques",
                "- Le titre",
                "- Le texte secondaire",
                "- L'appel à l'action",
                "",
                "Réponds en français."
            ])

        else:

            instruction = "\n".join([
                "Tu es un expert en prompts pour générateurs d'images IA.",
                "",
                "Crée un prompt d'image professionnel, détaillé et directement utilisable.",
                "",
                "Sujet :",
                demande,
                "",
                "Plateforme :",
                plateforme,
                "",
                "Style :",
                style,
                "",
                "Format :",
                format_image,
                "",
                "Le prompt doit décrire précisément :",
                "- Le sujet",
                "- La composition",
                "- L'environnement",
                "- L'éclairage",
                "- Les détails visuels",
                "- Le style",
                "- La qualité",
                "- Le cadrage",
                "",
                "Réponds en français."
            ])

        # ----------------------------------------------------
        # GENERATION GEMINI
        # ----------------------------------------------------

        with st.spinner(
            "🤖 IA-Creator prépare ta création..."
        ):

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=instruction
                )

                resultat = response.text

                if resultat:

                    st.markdown(
                        '<div class="section-title">✨ Ton résultat</div>',
                        unsafe_allow_html=True
                    )

                    st.text_area(
                        "Résultat",
                        resultat,
                        height=400,
                        key="resultat_final"
                    )

                    # ------------------------------------------------
                    # COPIER
                    # ------------------------------------------------

                    texte_js = (
                        resultat
                        .replace("\\", "\\\\")
                        .replace("`", "\\`")
                        .replace("${", "\\${")
                    )

                    components.html(
                        f"""
                        <button
                            onclick="navigator.clipboard.writeText(`{texte_js}`).then(() => alert('✅ Texte copié !'))"
                            style="
                                width:100%;
                                padding:14px;
                                border-radius:14px;
                                border:1px solid #ddd;
                                background:white;
                                font-size:16px;
                                font-weight:bold;
                                cursor:pointer;
                            "
                        >
                            📋 Copier le résultat
                        </button>
                        """,
                        height=65
                    )

                    # ------------------------------------------------
                    # TELECHARGER
                    # ------------------------------------------------

                    st.download_button(
                        "⬇️ Télécharger le résultat",
                        data=resultat,
                        file_name="ia_creator_resultat.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    # ------------------------------------------------
                    # HISTORIQUE
                    # ------------------------------------------------

                    st.session_state.historique.insert(
                        0,
                        {
                            "outil": outil,
                            "demande": demande,
                            "resultat": resultat
                        }
                    )

            except Exception as e:

                st.error(
                    "❌ Une erreur est survenue pendant la génération."
                )

                st.caption(str(e))

# ============================================================
# HISTORIQUE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🕘 Historique de cette session</div>',
    unsafe_allow_html=True
)

if st.session_state.historique:

    for element in st.session_state.historique:

        titre = element["demande"][:50]

        with st.expander(
            f"{element['outil']} — {titre}"
        ):

            st.write(element["resultat"])

    if st.button(
        "🗑️ Effacer l'historique",
        use_container_width=True
    ):

        st.session_state.historique = []
        st.rerun()

else:

    st.info(
        "Aucune création dans cette session."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <footer>
        🤖 IA-Creator<br>
        Crée • Apprends • Développe tes idées avec l'IA
    </footer>
    """,
    unsafe_allow_html=True
)
