import streamlit as st
import pandas as pd
import plotly.express as px
import logging

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if not st.session_state.get("authenticated") or not st.session_state.get("rgpd_ok"):
    st.warning("Veuillez vous connecter depuis la page d'accueil.")
    st.stop()

logging.info(f"{st.session_state.username} | page: dashboard")

@st.cache_data
def load():
    return pd.read_csv("data/insurance_clean.csv")

df = load()

st.title("📊 Dashboard — Analyse des données")

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Patients", f"{len(df):,}")
c2.metric("Frais moyens", f"{df.charges.mean():,.0f} €")
c3.metric("Frais max", f"{df.charges.max():,.0f} €")
c4.metric("% Fumeurs", f"{(df.smoker=='yes').mean()*100:.1f}%")

st.markdown("---")

# Filtres
with st.expander("🔧 Filtres"):
    smoker_filter = st.multiselect("Fumeur", ["yes", "no"], default=["yes", "no"])
    age_range = st.slider("Tranche d'âge", 18, 64, (18, 64))

dff = df[df.smoker.isin(smoker_filter) & df.age.between(*age_range)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("IMC vs Frais médicaux")
    fig = px.scatter(dff, x="bmi", y="charges", color="smoker",
                     color_discrete_map={"yes": "#E24B4A", "no": "#1D9E75"},
                     labels={"bmi": "IMC", "charges": "Frais (€)", "smoker": "Fumeur"},
                     opacity=0.6)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Âge vs Frais médicaux")
    fig2 = px.scatter(dff, x="age", y="charges", color="smoker",
                      color_discrete_map={"yes": "#E24B4A", "no": "#1D9E75"},
                      labels={"age": "Âge", "charges": "Frais (€)", "smoker": "Fumeur"},
                      opacity=0.6)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Distribution des frais")
fig3 = px.histogram(dff, x="charges", nbins=50, color="smoker",
                    color_discrete_map={"yes": "#E24B4A", "no": "#1D9E75"},
                    barmode="overlay", opacity=0.7,
                    labels={"charges": "Frais (€)", "smoker": "Fumeur"})
st.plotly_chart(fig3, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Frais moyens par région")
    reg = dff.groupby("region_fr")["charges"].mean().reset_index().sort_values("charges")
    fig4 = px.bar(reg, x="charges", y="region_fr", orientation="h",
                  color="charges", color_continuous_scale="Blues",
                  labels={"charges": "Frais moyens (€)", "region_fr": "Région"})
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.subheader("⚖️ Coefficients du modèle (biais)")
    coefs = pd.DataFrame({
        "Variable": ["Fumeur", "Enfants", "IMC", "Âge", "Sexe"],
        "Impact (€)": [23654, 427, 328, 257, -8]
    }).sort_values("Impact (€)")
    fig5 = px.bar(coefs, x="Impact (€)", y="Variable", orientation="h",
                  color="Impact (€)", color_continuous_scale="RdBu",
                  title="Le statut fumeur domine largement")
    st.plotly_chart(fig5, use_container_width=True)

st.info("**Atténuation du biais fumeur :** le coefficient +23 654 € reflète une réalité médicale documentée. Il est affiché en toute transparence dans le simulateur et ne constitue pas une discrimination au sens juridique.")
