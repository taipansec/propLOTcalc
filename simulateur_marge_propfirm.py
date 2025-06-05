
import streamlit as st
from PIL import Image

st.set_page_config(page_title="m3X0Ru - Simulateur de Marge", page_icon="⚔️")

st.title("⚔️ m3X0Ru - Simulateur de Marge Prop Firm")
st.markdown("**Évite les blocages 'Not enough money' sur FTMO et prop firms.** Calcule ta taille de lot maximale sans jamais dépasser une marge sécurisée. Maîtrise le levier. Sois un Jedi.")

# Affichage du logo
logo = Image.open("logo.png")
st.image(logo, width=120)

pip_values = {
    "XAUUSD": 10,
    "EURUSD": 10,
    "GBPUSD": 10,
    "GBPJPY": 9.3,
    "BTCUSD": 1
}

with st.form("form"):
    pair = st.selectbox("Paire", options=list(pip_values.keys()))
    capital = st.number_input("Capital total (USD)", value=200000.0)
    price = st.number_input("Prix actuel de l’actif", value=3370.0)
    contract_size = st.number_input("Taille d’un contrat standard", value=100)
    leverage = st.number_input("Levier autorisé (ex: 30 pour 1:30)", value=30)
    safe_margin_percent = st.slider("🔐 Marge maximale autorisée (% du capital)", min_value=10, max_value=90, value=25, step=1)
    safe_margin_ratio = safe_margin_percent / 100
    sl_pips = st.number_input("Stop-Loss (en pips)", value=250.0)
    risk_percent = st.number_input("Risque % du capital", value=1.0)

    submitted = st.form_submit_button("Calculer")

    if submitted:
        pip_value = pip_values[pair]

        # Bloc 1 : Simulateur de marge FTMO
        max_margin_available = capital * safe_margin_ratio
        max_position_value = max_margin_available * leverage
        max_lots = max_position_value / (price * contract_size)

        real_position_value = max_lots * price * contract_size
        real_margin_used = real_position_value / leverage
        margin_ratio_used = real_margin_used / capital

        is_ftmo_safe = margin_ratio_used <= 0.3

        if is_ftmo_safe:
            st.warning(f"⚠️ Tu peux ouvrir jusqu’à {max_lots:.2f} lots, mais cela utilise {margin_ratio_used*100:.2f}% de ton capital en marge. FTMO peut bloquer au-delà de 30 %.")
        else:
            st.success(f"✅ Tu peux ouvrir jusqu’à {max_lots:.2f} lots. Marge utilisée : {margin_ratio_used*100:.2f} % – FTMO OK.")
        st.markdown("### Détail du calcul FTMO :")
        st.markdown(f"- Marge max autorisée : {max_margin_available:.2f} USD")
        st.markdown(f"- Valeur max de la position : {max_position_value:.2f} USD")
        st.markdown(f"- Taille contrat : {contract_size}")
        st.markdown(f"- Levier : 1:{int(leverage)}")
        st.markdown(f"- Marge réelle utilisée : {real_margin_used:.2f} USD ({margin_ratio_used*100:.2f}% du capital)")

        if is_ftmo_safe:
            st.error("⚠️ Zone de blocage FTMO probable : marge utilisée dépasse 30 % du capital.")
        else:
            st.info("🟢 Zone de sécurité FTMO : marge utilisée raisonnable.")

        tag = "🟢 Zone FTMO OK" if margin_ratio_used <= 0.3 else "🔴 Zone FTMO à risque"
        st.markdown(f"**{tag}**")

        # Bloc 2 : Calculette type Myfxbook
        risk_amount = capital * (risk_percent / 100)
        lot_by_risk = risk_amount / (sl_pips * pip_value)

        st.markdown("### Taille de lot calculée selon ton risque :")
        st.markdown(f"- Risque : {risk_amount:.2f} USD")
        st.markdown(f"- SL : {sl_pips} pips")
        st.markdown(f"- Valeur du pip : {pip_value} USD par lot")
        st.markdown(f"- => Taille de lot recommandée : {lot_by_risk:.2f} lots")
