
# m3X0Ru - Simulateur de Marge Prop Firm

Ce simulateur Streamlit permet de calculer la **taille de lot maximale autorisée** selon ton capital, ton levier et le prix de l’actif, sans jamais risquer de blocage sur FTMO, MFF, The Funded Trader, etc.

## 🚀 Déploiement Streamlit Cloud
1. Fork ce repo sur GitHub : https://github.com/taipansec
2. Va sur [Streamlit Cloud](https://share.streamlit.io)
3. Connecte ton GitHub et sélectionne le fichier `simulateur_marge_propfirm.py`
4. Lance le déploiement ➝ ton simulateur est en ligne !

## 🧠 Calcul utilisé
- Marge max = Capital × Ratio (%)
- Valeur position max = Marge max × Levier
- Lots max = Valeur position max / (Prix actif × Taille contrat)

## 📱 Mobile-friendly
Ce simulateur est 100% responsive et prêt pour mobile !

---

© 2025 – m3X0Ru by TaipanSec 💠
