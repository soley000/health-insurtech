# Health InsurTech — Simulateur de frais médicaux

## Structure du projet

```
health-insurtech/
├── app.py                          ← point d'entrée (login + consentement RGPD)
├── pages/
│   ├── 1_Dashboard.py              ← exploration des données
│   ├── 2_Simulateur.py             ← simulation en temps réel
│   └── 3_RGPD.py                   ← note de conformité
├── model/
│   ├── model_lr.pkl                ← régression linéaire (R²=0.781)
│   └── model_dt.pkl                ← arbre de décision (R²=0.864)
├── data/
│   └── insurance_clean.csv         ← dataset sans PII
├── notebooks/
│   └── analyse_modelisation.ipynb  ← EDA complète + comparaison modèles
├── requirements.txt
└── .streamlit/config.toml
```

## Lancement local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Identifiants : `admin` / `admin123` ou `demo` / `demo2024`

## Déploiement Streamlit Cloud

1. Pusher ce dossier sur GitHub (repo public ou privé)
2. Aller sur https://share.streamlit.io → "New app"
3. Sélectionner le repo, branche `main`, fichier `app.py`
4. Déployer — l'app sera accessible via une URL HTTPS publique

## Notebook

Ouvrir `notebooks/analyse_modelisation.ipynb` dans Jupyter pour suivre tout le cheminement :
EDA → corrélations → régression linéaire → arbre de décision → comparaison R² → sauvegarde des modèles.
