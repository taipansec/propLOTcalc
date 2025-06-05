
import streamlit as st
from PIL import Image

st.set_page_config(page_title="m3X0Ru - Simulateur de Marge", page_icon="💠")

st.title("💠 m3X0Ru - Simulateur de Marge Prop Firm")
st.markdown("**Évite les blocages 'Not enough money' sur FTMO et prop firms.** Calcule ta taille de lot maximale sans jamais dépasser une marge sécurisée. Maîtrise le levier. Sois un Jedi.")

# Affichage du logo
logo = Image.open("logo.png")
st.image(logo, width=120)

with st.form("form"):
    capital = st.number_input("💰 Capital total (USD)", value=200000.0)
    price = st.number_input("📈 Prix actuel de l’actif", value=3370.0)
    contract_size = st.number_input("📦 Taille d’un contrat standard (ex: 100 pour XAUUSD)", value=100)
    leverage = st.number_input("🧮 Levier autorisé (ex: 30 pour 1:30)", value=30)
    safe_margin_ratio = st.slider("🔐 % max de capital utilisé en marge", min_value=0.1, max_value=0.5, value=0.25, step=0.01)

    submitted = st.form_submit_button("Calculer")

    if submitted:
        max_margin_available = capital * safe_margin_ratio
        max_position_value = max_margin_available * leverage
        max_lots = max_position_value / (price * contract_size)

        st.success(f"✅ Tu peux ouvrir jusqu’à **{max_lots:.2f} lots** sans dépasser **{safe_margin_ratio*100:.0f}%** de marge.")
        st.markdown(f'''
        ### 📊 Détail du calcul :
        - **Marge max autorisée** : `{max_margin_available:.2f} USD`
        - **Valeur max de la position** : `{max_position_value:.2f} USD`
        - **Taille contrat** : `{contract_size}`
        - **Levier** : `1:{int(leverage)}`
        ''')
