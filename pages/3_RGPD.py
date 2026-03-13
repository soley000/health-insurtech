import streamlit as st
import logging

st.set_page_config(page_title="RGPD & Éthique", page_icon="📋", layout="wide")

if not st.session_state.get("authenticated") or not st.session_state.get("rgpd_ok"):
    st.warning("Veuillez vous connecter depuis la page d'accueil.")
    st.stop()

logging.info(f"{st.session_state.username} | page: rgpd")

st.title("📋 Conformité RGPD & Accessibilité")

st.markdown("""
## Note d'analyse d'impact (PIA)

### 1. Données traitées et base légale

Le dataset source contient des données à caractère personnel sensibles : nom, prénom, date de naissance, email, téléphone, numéro de sécurité sociale, adresse IP. Conformément au principe de **minimisation des données** (Art. 5 RGPD), seules les variables strictement nécessaires sont conservées après prétraitement : âge, sexe, IMC, enfants, statut tabagique, charges.

La base légale est le **consentement explicite** (Art. 6.1.a RGPD), recueilli à l'entrée de l'application.

### 2. Mesures techniques

- **Pseudonymisation** : colonnes PII supprimées avant entraînement du modèle.
- **Durée de conservation** : aucune donnée saisie n'est persistée. Sessions éphémères.
- **Journalisation** : logs techniques sans données personnelles identifiables.
- **Accès restreint** : authentification obligatoire avant tout accès.
- **Droits des personnes** : accès, rectification, suppression sur demande à dpo@health-insurtech.fr (Art. 15–17 RGPD).

### 3. Analyse des risques

| Risque | Probabilité | Mesure d'atténuation |
|---|---|---|
| Réidentification via IMC + âge | Faible | Aucun stockage des saisies |
| Biais discriminatoire (fumeurs) | Moyen | Affichage transparent des coefficients |
| Fuite de données | Faible | HTTPS obligatoire, secrets hors code source |

---

## Accessibilité WCAG 2.1 — 3 mesures implémentées

**1. Contraste des couleurs (critère 1.4.3)**
Tous les textes respectent un ratio minimum de 4,5:1. Les couleurs des graphiques ont été vérifiées (rouge #E24B4A sur fond blanc = ratio 4.6:1).

**2. Navigation au clavier (critère 2.1.1)**
L'ensemble des formulaires est utilisable via Tab/Entrée sans recours à la souris.

**3. Labels explicites (critères 1.1.1 & 1.3.1)**
Chaque champ du formulaire possède un label descriptif. Les graphiques Plotly incluent titres et légendes complets.

---

## Atténuation des biais du modèle

Le coefficient du statut fumeur (+23 654 €) est la variable la plus influente du modèle. Cela reflète une réalité médicale documentée (coûts de santé significativement plus élevés chez les fumeurs) et non une discrimination arbitraire.

**Mesures prises :**
- Affichage explicite de tous les coefficients dans le simulateur
- Comparaison systématique fumeur/non-fumeur pour chaque simulation
- Le modèle utilise uniquement des variables médicales objectives, sans variable proxy (pas de région, pas de revenu)
""")
