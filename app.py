import streamlit as st
import logging, os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

st.set_page_config(page_title="Health InsurTech", page_icon="🏥", layout="wide")

USERS = {"admin": "admin123", "demo": "demo2024"}

# ── Login ──────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🏥 Health InsurTech")
    st.markdown("#### Connexion")
    username = st.text_input("Identifiant")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter", use_container_width=True):
        if USERS.get(username) == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            logging.info(f"LOGIN OK : {username}")
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect.")
            logging.warning(f"LOGIN FAIL : {username}")
    st.stop()

# ── Consentement RGPD ──────────────────────────────────────────────────────────
if "rgpd_ok" not in st.session_state:
    st.session_state.rgpd_ok = False

if not st.session_state.rgpd_ok:
    st.title("🔒 Consentement & Confidentialité")
    st.info("""
**Ce simulateur collecte uniquement :** âge, sexe, IMC, enfants, statut tabagique.

- Aucune donnée nominative n'est collectée ni conservée.
- Les saisies sont éphémères (session uniquement).
- Vous pouvez retirer votre consentement à tout moment.
- Contact DPO : dpo@health-insurtech.fr — Conformité RGPD (UE) 2016/679
    """)
    c1, c2 = st.columns(2)
    if c1.button("✅ J'accepte", use_container_width=True):
        st.session_state.rgpd_ok = True
        logging.info(f"RGPD CONSENT : {st.session_state.username}")
        st.rerun()
    if c2.button("❌ Je refuse", use_container_width=True):
        st.warning("Sans consentement, l'application ne peut pas fonctionner.")
    st.stop()

# ── Accueil ────────────────────────────────────────────────────────────────────
st.title("🏥 Health InsurTech — Accueil")
st.markdown(f"Bienvenue **{st.session_state.username}** 👋")
st.markdown("""
Utilisez la barre latérale pour naviguer :

- **📊 Dashboard** — exploration des données et analyse des biais
- **🔮 Simulateur** — estimez vos frais médicaux en temps réel
- **📋 RGPD & Éthique** — note de conformité et accessibilité
""")

st.sidebar.success("Connecté : " + st.session_state.username)
if st.sidebar.button("Se déconnecter"):
    for k in ["authenticated", "rgpd_ok", "username"]:
        st.session_state.pop(k, None)
    st.rerun()
