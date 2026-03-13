import streamlit as st
import numpy as np
import pickle
import logging

st.set_page_config(page_title="Simulateur", page_icon="🔮", layout="wide")

if not st.session_state.get("authenticated") or not st.session_state.get("rgpd_ok"):
    st.warning("Veuillez vous connecter depuis la page d'accueil.")
    st.stop()

logging.info(f"{st.session_state.username} | page: simulateur")

@st.cache_resource
def load_model():
    with open("model/model_lr.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("🔮 Simulateur de frais médicaux")
st.info("Aucune donnée nominative n'est collectée. Les résultats sont indicatifs.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Vos informations")
    age      = st.slider("Âge", 18, 64, 35)
    bmi      = st.number_input("IMC (kg/m²)", 15.0, 55.0, 25.0, step=0.1)
    children = st.selectbox("Enfants à charge", [0, 1, 2, 3, 4, 5])
    sex      = st.radio("Sexe", ["Femme", "Homme"], horizontal=True)
    smoker   = st.radio("Fumeur(euse) ?", ["Non", "Oui"], horizontal=True)

    if st.button("💰 Estimer mes frais", use_container_width=True, type="primary"):
        sex_enc    = 1 if sex == "Homme" else 0
        smoker_enc = 1 if smoker == "Oui" else 0

        pred = model.predict([[age, sex_enc, bmi, children, smoker_enc]])[0]
        pred_ns = model.predict([[age, sex_enc, bmi, children, 0]])[0]
        pred_s  = model.predict([[age, sex_enc, bmi, children, 1]])[0]

        st.session_state.result = {
            "pred": pred, "pred_ns": pred_ns, "pred_s": pred_s,
            "age": age, "bmi": bmi, "smoker_enc": smoker_enc
        }
        logging.info(f"{st.session_state.username} | sim | age={age} bmi={bmi:.1f} smoker={smoker_enc} => {pred:.0f}")

with col2:
    if "result" in st.session_state:
        r = st.session_state.result
        st.markdown("#### Résultats")
        st.success(f"### Estimation : **{max(r['pred'], 0):,.0f} €** / an")

        c1, c2 = st.columns(2)
        c1.metric("Non-fumeur", f"{max(r['pred_ns'], 0):,.0f} €")
        c2.metric("Fumeur", f"{max(r['pred_s'], 0):,.0f} €",
                  delta=f"+{r['pred_s'] - r['pred_ns']:,.0f} €")

        st.markdown("##### Détail des facteurs")
        factors = {
            "Âge":     257.1  * r["age"],
            "IMC":     327.5  * r["bmi"],
            "Enfants": 427.3  * r.get("children", 0),
            "Fumeur":  23653.9 * r["smoker_enc"],
        }
        import plotly.express as px, pandas as pd
        df_f = pd.DataFrame(factors.items(), columns=["Facteur", "Impact (€)"])
        fig = px.bar(df_f, x="Facteur", y="Impact (€)",
                     color="Impact (€)", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

        st.caption("⚠️ Estimation indicative basée sur un modèle statistique. Ne constitue pas un devis contractuel.")
    else:
        st.markdown("#### Résultats")
        st.markdown("Remplissez le formulaire et cliquez sur **Estimer mes frais**.")
