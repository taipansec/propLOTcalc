
import streamlit as st
from PIL import Image

st.set_page_config(page_title="m3X0Ru - Simulateur de Marge", page_icon="💠")

st.title("💠 m3X0Ru - Simulateur de Marge Prop Firm")
st.markdown("**Calcule ta taille de lot maximale selon le risque et vérifie la marge FTMO.**")

# Affichage du logo
logo = Image.open("logo.png")
st.image(logo, width=120)

# Valeurs de pip par lot standard pour différentes paires
pip_values = {
    "XAUUSD": 10,
    "EURUSD": 10,
    "GBPUSD": 10,
    "GBPJPY": 9.3,
    "BTCUSD": 1
}

with st.form("form"):
    pair = st.selectbox("💱 Choisis ta paire", options=list(pip_values.keys()))
    capital = st.number_input("💰 Capital total (USD)", value=200000.0)
    price = st.number_input("📈 Prix actuel de l’actif", value=3370.0)
    contract_size = st.number_input("📦 Taille d’un contrat standard", value=100)
    leverage = st.number_input("🧮 Levier autorisé (ex: 30 pour 1:30)", value=30)
    sl_pips = st.number_input("🎯 Stop-Loss (en pips)", value=250.0)
    risk_percent = st.number_input("⚠️ Risque % du capital", value=1.0)
    safe_margin_ratio = st.slider("🔐 % max de capital utilisé en marge", min_value=0.1, max_value=0.9, value=0.3, step=0.01)

    submitted = st.form_submit_button("Calculer")

    if submitted:
        pip_value = pip_values[pair]
        risk_amount = capital * (risk_percent / 100)
        lot_size_risk = risk_amount / (sl_pips * pip_value)

        # Calcul marge
        position_value = lot_size_risk * price * contract_size
        margin_required = position_value / leverage
        margin_ratio_used = margin_required / capital

        # Calcul max lots FTMO en fonction de la marge autorisée
        max_margin_available = capital * safe_margin_ratio
        max_position_value = max_margin_available * leverage
        max_lots_ftmo = max_position_value / (price * contract_size)

        st.markdown("### 🧠 Résultat combiné :")
        st.write(f"📌 **Lot calculé selon le risque** : `{lot_size_risk:.2f} lots`")
        st.write(f"🧮 **Marge requise** : `{margin_required:.2f} USD` (**{margin_ratio_used*100:.2f}% du capital**)")
        st.write(f"🛡️ **Lot FTMO maximum autorisé (marge safe)** : `{max_lots_ftmo:.2f} lots`")

        if lot_size_risk > max_lots_ftmo:
            st.error("⚠️ Le lot calculé dépasse la marge autorisée FTMO. Réduis ton risque, ton SL, ou fractionne le trade.")
        else:
            st.success("✅ Ce lot respecte la marge FTMO autorisée. Tu peux le trader sans blocage.")
