import streamlit as st
import streamlit.components.v1 as components
from google import genai
from supabase import create_client
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

st.markdown("""
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
    font-size: 40px;
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
}

.success-box {
    padding: 15px;
    border-radius: 12px;
    background: #ecfdf5;
    border-left: 5px solid #10b981;
}

footer {
    text-align: center;
    margin-top: 40px;
    color: #777;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SUPABASE
# ============================================================

try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error("Erreur de connexion à Supabase.")
    st.stop()

# ============================================================
# GEMINI
# ============================================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception:
    st.error("Erreur avec la clé Gemini.")
    st.stop()

# ============================================================
# SESSION STREAMLIT
# ============================================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False

if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

if "historique" not in st.session_state:
    st.session_state.historique = []

if "access_token" not in st.session_state:
    st.session_state.access_token = ""

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = ""

# ============================================================
# RESTAURER LA SESSION SUPABASE
# ============================================================

if (
    st.session_state.access_token
    and st.session_state.refresh_token
):

    try:
        session_restore = supabase.auth.set_session(
            st.session_state.access_token,
            st.session_state.refresh_token
        )

        if session_restore and session_restore.user:

            st.session_state.utilisateur = session_restore.user
            st.session_state.connecte = True

            if session_restore.session:

                st.session_state.access_token = (
                    session_restore.session.access_token
                )

                st.session_state.refresh_token = (
                    session_restore.session.refresh_token
                )

    except Exception:
        pass

# ============================================================
# HISTORIQUE
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


def enregistrer_historique(
    user_id,
    mode,
    style,
    plateforme,
    demande,
    resultat
):

    try:

        supabase.table("historique").insert({
            "user_id": str(user_id),
            "mode": mode,
            "style": style,
            "plateforme": plateforme,
            "demande": demande,
            "resultat": resultat
        }).execute()

        return True

    except Exception:

        return False

# ============================================================
# PAGE CONNEXION
# ============================================================

if not st.session_state.connecte:

    st.markdown("""
    <div class="hero">
        <h1>🤖 IA-Creator</h1>
        <p>Crée avec l'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)

    connexion, inscription = st.tabs([
        "🔑 Se connecter",
        "📝 Créer un compte"
    ])

    # ========================================================
    # CONNEXION
    # ========================================================

    with connexion:

        email = st.text_input(
            "📧 Email",
            key="login_email"
        )

        password = st.text_input(
            "🔒 Mot de passe",
            type="password",
            key="login_password"
        )

        if st.button(
            "🚀 Se connecter",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Entre ton email et ton mot de passe."
                )

            else:

                try:

                    resultat_login = (
                        supabase.auth.sign_in_with_password({
                            "email": email.strip(),
                            "password": password
                        })
                    )

                    if resultat_login.user:

                        st.session_state.connecte = True

                        st.session_state.utilisateur = (
                            resultat_login.user
                        )

                        # IMPORTANT :
                        # On conserve les tokens de connexion.
                        if resultat_login.session:

                            st.session_state.access_token = (
                                resultat_login.session.access_token
                            )

                            st.session_state.refresh_token = (
                                resultat_login.session.refresh_token
                            )

                        # On charge l'historique.
                        st.session_state.historique = (
                            charger_historique(
                                resultat_login.user.id
                            )
                        )

                        st.success(
                            "Connexion réussie !"
                        )

                        st.rerun()

                except Exception:

                    st.error(
                        "Email ou mot de passe incorrect."
                    )

    # ========================================================
    # INSCRIPTION
    # ========================================================

    with inscription:

        nom = st.text_input(
            "👤 Nom",
            key="signup_name"
        )

        email2 = st.text_input(
            "📧 Email",
            key="signup_email"
        )

        password2 = st.text_input(
            "🔒 Mot de passe",
            type="password",
            key="signup_password"
        )

        confirmation = st.text_input(
            "🔒 Confirmer le mot de passe",
            type="password",
            key="signup_confirmation"
        )

        if st.button(
            "✨ Créer mon compte",
            use_container_width=True
        ):

            if not nom:

                st.warning("Entre ton nom.")

            elif not email2:

                st.warning("Entre ton email.")

            elif len(password2) < 6:

                st.warning(
                    "Le mot de passe doit contenir au moins 6 caractères."
                )

            elif password2 != confirmation:

                st.error(
                    "Les deux mots de passe sont différents."
                )

            else:

                try:

                    resultat_signup = (
                        supabase.auth.sign_up({
                            "email": email2.strip(),
                            "password": password2,
                            "options": {
                                "data": {
                                    "full_name": nom.strip()
                                }
                            }
                        })
                    )

                    if resultat_signup.user:

                        if resultat_signup.session:

                            st.session_state.connecte = True

                            st.session_state.utilisateur = (
                                resultat_signup.user
                            )

                            st.session_state.access_token = (
                                resultat_signup.session.access_token
                            )

                            st.session_state.refresh_token = (
                                resultat_signup.session.refresh_token
                            )

                            st.session_state.historique = []

                            st.success(
                                "Compte créé avec succès !"
                            )

                            st.rerun()

                        else:

                            st.success(
                                "Compte créé ! Vérifie ton email puis connecte-toi."
                            )

                except Exception:

                    st.error(
                        "Impossible de créer le compte."
                    )

    st.stop()

# ============================================================
# UTILISATEUR CONNECTÉ
# ============================================================

user = st.session_state.utilisateur

# ============================================================
# EN-TÊTE
# ============================================================

st.markdown("""
<div class="hero">
    <h1>🤖 IA-Creator</h1>
    <p>Crée avec l'intelligence artificielle</p>
</div>
""", unsafe_allow_html=True)

colonne1, colonne2 = st.columns([4, 1])

with colonne1:

    st.markdown(
        '<div class="success-box">✅ Tu es connecté.</div>',
        unsafe_allow_html=True
    )

with colonne2:

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
        st.session_state.historique = []
        st.session_state.access_token = ""
        st.session_state.refresh_token = ""

        st.rerun()

# ============================================================
# OUTIL
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
    "🎨 Style",
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
# OPTIONS
# ============================================================

duree = ""

if outil == "🎬 Créer un script vidéo":

    duree = st.selectbox(
        "⏱️ Durée",
        [
            "30 secondes",
            "60 secondes",
            "90 secondes",
            "2 minutes",
            "3 minutes"
        ]
    )

format_image = ""

if (
    outil == "🎨 Créer une idée d'affiche"
    or outil == "🖼️ Créer un prompt d'image IA"
):

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
    placeholder=(
        "Exemple : crée une vidéo sur les avantages de l'intelligence artificielle."
    ),
    height=160
)

# ============================================================
# CREATION
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

        if outil == "💡 Créer une idée":

            prompt = (
                "Tu es un expert en création de contenu. "
                "Crée une idée originale sur : "
                + demande
                + ". Style : "
                + style
                + ". Plateforme : "
                + plateforme
                + ". Donne un titre, une accroche, le concept et une explication."
            )

        elif outil == "✍️ Créer un texte":

            prompt = (
                "Tu es un expert en rédaction. "
                "Rédige un texte professionnel sur : "
                + demande
                + ". Style : "
                + style
                + ". Plateforme : "
                + plateforme
                + ". Le texte doit être prêt à publier."
            )

        elif outil == "🎬 Créer un script vidéo":

            prompt = (
                "Tu es un scénariste professionnel. "
                "Crée un script vidéo sur : "
                + demande
                + ". Style : "
                + style
                + ". Plateforme : "
                + plateforme
                + ". Durée : "
                + duree
                + ". Donne une accroche, les scènes, la conclusion et un appel à l'action."
            )

        elif outil == "🎨 Créer une idée d'affiche":

            prompt = (
                "Tu es un directeur artistique. "
                "Imagine une affiche professionnelle sur : "
                + demande
                + ". Style : "
                + style
                + ". Format : "
                + format_image
                + ". Décris le visuel, le texte, la composition, l'ambiance et l'éclairage."
            )

        else:

            prompt = (
                "Tu es un expert en génération d'images IA. "
                "Crée un prompt détaillé pour une image sur : "
                + demande
                + ". Style : "
                + style
                + ". Format : "
                + format_image
                + ". Décris le sujet, la composition, la lumière, l'arrière-plan et les détails."
            )

        with st.spinner(
            "🤖 Création en cours..."
        ):

            try:

                reponse = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                resultat = reponse.text

            except Exception:

                resultat = ""

                st.error(
                    "Une erreur est survenue avec Gemini."
                )

        # ====================================================
        # RESULTAT
        # ====================================================

        if resultat:

            st.markdown(
                '<div class="section-title">✨ Résultat</div>',
                unsafe_allow_html=True
            )

            st.text_area(
                "Ton contenu",
                resultat,
                height=400,
                key="resultat"
            )

            # =================================================
            # COPIER
            # =================================================

            texte_json = json.dumps(
                resultat
            )

            code_copie = (
                "<button onclick='copier()' "
                "style='width:100%;padding:12px;"
                "border:0;border-radius:10px;"
                "background:#2563eb;color:white;"
                "font-size:16px;font-weight:bold;'>"
                "📋 Copier le résultat"
                "</button>"
                "<script>"
                "function copier(){"
                "var texte="
                + texte_json
                + ";"
                "navigator.clipboard.writeText(texte);"
                "document.querySelector('button').innerText='✅ Copié !';"
                "}"
                "</script>"
            )

            components.html(
                code_copie,
                height=65
            )

            # =================================================
            # TELECHARGER
            # =================================================

            st.download_button(
                "⬇️ Télécharger",
                resultat,
                file_name="ia_creator_resultat.txt",
                mime="text/plain",
                use_container_width=True
            )

            # =================================================
            # SAUVEGARDER DANS SUPABASE
            # =================================================

            sauvegarde = enregistrer_historique(
                user.id,
                outil,
                style,
                plateforme,
                demande.strip(),
                resultat
            )

            if sauvegarde:

                st.session_state.historique = (
                    charger_historique(
                        user.id
                    )
                )

                st.success(
                    "✅ Création enregistrée dans ton historique."
                )

            else:

                st.warning(
                    "Le contenu a été créé, mais l'enregistrement dans l'historique a échoué."
                )

# ============================================================
# HISTORIQUE
# ============================================================

st.markdown(
    '<div class="section-title">📚 Mon historique</div>',
    unsafe_allow_html=True
)

# On recharge l'historique depuis Supabase
# avec la session restaurée.

historique = charger_historique(
    user.id
)

st.session_state.historique = historique

if not historique:

    st.info(
        "Ton historique est vide pour le moment."
    )

else:

    st.write(
        "Créations enregistrées :",
        len(historique)
    )

    for element in historique:

        identifiant = str(
            element.get("id", "")
        )

        mode = element.get(
            "mode",
            "Création"
        )

        date = element.get(
            "created_at",
            ""
        )

        demande_saved = element.get(
            "demande",
            ""
        )

        resultat_saved = element.get(
            "resultat",
            ""
        )

        with st.expander(
            mode + " • " + str(date)[:16]
        ):

            st.write(
                "📝 Demande :",
                demande_saved
            )

            st.text_area(
                "Résultat",
                resultat_saved,
                height=250,
                key="historique_" + identifiant
            )

# ============================================================
# EFFACER HISTORIQUE
# ============================================================

st.markdown("---")

if st.button(
    "🗑️ Effacer mon historique",
    use_container_width=True
):

    try:

        supabase.table("historique").delete().eq(
            "user_id",
            str(user.id)
        ).execute()

        st.session_state.historique = []

        st.success(
            "Historique supprimé."
        )

        st.rerun()

    except Exception:

        st.error(
            "Impossible de supprimer l'historique."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<div style='text-align:center;margin-top:40px;color:#777;'>"
    "🤖 IA-Creator • Ton espace de création IA"
    "</div>",
    unsafe_allow_html=True
)
