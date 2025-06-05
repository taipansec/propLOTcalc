import streamlit as st
from PIL import Image

st.set_page_config(page_title="m3X0Ru - Simulateur de Marge", page_icon="⚔️")

st.title("⚔️ m3X0Ru - Simulateur de Marge Prop Firm")
st.markdown("**Calcule ta taille de lot maximale selon le risque et vérifie la marge FTMO.**")

# Logo
logo = Image.open("logo.png")
st.image(logo, width=120)

# Valeurs du pip selon les paires
pip_values = {
    "XAUUSD": 10,
    "EURUSD": 10,
    "GBPUSD": 10,
    "GBPJPY": 9.3,
    "BTCUSD": 1
}

with st.form("form"):
    pair = st.selectbox("💱 Choisis ta paire", options=list(pip_values.keys()))

    capital = st.number_input("💰 **Capital total (USD)**", value=200000.0)

    price = st.number_input("📈 **Prix actuel de l’actif**", value=3370.0)

    contract_size = st.number_input("📦 **Taille d’un contrat standard**", value=100)

    leverage = st.number_input("🧮 **Levier autorisé (ex: 30 pour 1:30)**", value=30)

    sl_pips = st.number_input("🎯 **Stop-Loss (en pips)**", value=250.0)

    risk_percent = st.number_input("⚠️ **Risque % du capital**", value=1.0)

    safe_margin_percent = st.slider("🔐 Marge maximale autorisée (% du capital)", min_value=10, max_value=90, value=25, step=1)
    safe_margin_ratio = safe_margin_percent / 100

    submitted = st.form_submit_button("Calculer")

    if submitted:
        pip_value = pip_values[pair]
        risk_amount = capital * (risk_percent / 100)
        lot_size_risk = risk_amount / (sl_pips * pip_value)

        # Calcul de la marge
        position_value = lot_size_risk * price * contract_size
        margin_required = position_value / leverage
        margin_ratio_used = margin_required / capital

        # Calcul des lots FTMO selon la limite
        max_margin_available = capital * safe_margin_ratio
        max_position_value = max_margin_available * leverage
        max_lots = max_position_value / (price * contract_size)

        is_ftmo_safe = margin_ratio_used <= 0.3

        # Message synthétique principal
        if is_ftmo_safe:
            st.success(f"✅ Tu peux ouvrir jusqu’à {max_lots:.2f} lots. Marge utilisée : {margin_ratio_used*100:.2f}% – FTMO OK.")
        else:
            st.warning(f"⚠️ Tu peux ouvrir jusqu’à {max_lots:.2f} lots. Marge utilisée : {margin_ratio_used*100:.2f}% – zone à risque FTMO.")

        st.markdown("### 🧠 Résultat pour une utilisation FTMO :")
        st.markdown(f"- **Marge max autorisée** : `{max_margin_available:.2f} USD`")
        st.markdown(f"- **Valeur max de la position** : `{max_position_value:.2f} USD`")
        st.markdown(f"- **Taille contrat** : `{contract_size}`")
        st.markdown(f"- **Levier** : `1:{int(leverage)}`")
        st.markdown(f"- **Marge réelle utilisée** : `{margin_required:.2f} USD` (**{margin_ratio_used*100:.2f}% du capital**)")

        if is_ftmo_safe:
            st.info("🟢 Zone de sécurité FTMO : marge utilisée raisonnable.")
            st.markdown("🟢 **Zone FTMO OK**")
        else:
            st.error("⚠️ Zone de blocage FTMO probable : marge utilisée dépasse 30 % du capital.")
            st.markdown("🔴 **Zone FTMO à risque**")

        # Contrôle selon la marge personnalisée (slider)
        if margin_required > max_margin_available:
            st.error("🚫 Le lot calculé dépasse la marge que tu t’es toi-même fixée avec le slider rouge. Ajuste ton risque, ton SL ou fractionne le trade.")
        else:
            st.success("✅ Ce lot respecte la marge FTMO autorisée selon la limite que tu as fixée. Tu peux le trader sans blocage.")

        # Bloc Myfxbox-like
        estimated_risk = lot_size_risk * sl_pips * pip_value
        risk_percent_real = (estimated_risk / capital) * 100

        st.markdown("### 📐 Taille de lot calculée selon ton risque :")
        st.markdown(f"- 💰 **Risque** : `{risk_amount:.2f} USD`")
        st.markdown(f"- 🎯 **SL** : `{sl_pips}` pips")
        st.markdown(f"- 🧾 **Valeur du pip** : `{pip_value}` USD par lot")
        st.markdown(f"- ➕ => **Taille de lot recommandée** : `{lot_size_risk:.2f} lots`")