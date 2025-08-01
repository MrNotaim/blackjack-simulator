# blackjack_simulator_app.py

import streamlit as st

# Basic Strategy Lookup (vereinfachte Version ohne Split)
def basic_strategy(player_total, dealer_card):
    if player_total >= 17:
        return "stand"
    elif 13 <= player_total <= 16 and dealer_card <= 6:
        return "stand"
    elif player_total == 12 and 4 <= dealer_card <= 6:
        return "stand"
    elif player_total == 11:
        return "double"
    elif player_total == 10 and dealer_card <= 9:
        return "double"
    elif player_total == 9 and 3 <= dealer_card <= 6:
        return "double"
    else:
        return "hit"

# Streamlit UI
st.set_page_config(page_title="Bankroll-Verwaltung", layout="centered")
st.title("💰 Bankroll-Verwaltung mit Strategie-Empfehlung")

# Session State
if "runden" not in st.session_state:
    st.session_state.runden = []
if "guthaben" not in st.session_state:
    st.session_state.guthaben = 0
if "einsatz" not in st.session_state:
    st.session_state.einsatz = 0

# Input
col1, col2 = st.columns(2)
player_total = col1.number_input("🧍 Spieler Total", 4, 21, value=12)
dealer_card = col2.number_input("🪙 Dealer Karte", 2, 11, value=6)

start_guthaben = st.number_input("💼 Startguthaben (€)", 1, 1_000_000_000, value=50_000, step=100)
start_einsatz = st.number_input("🎯 Starteinsatz (€)", 1, 1_000_000_000, value=10_000, step=100)
max_runden = st.slider("🔁 Anzahl Runden", 1, 100, 10)

empfohlene_aktion = basic_strategy(player_total, dealer_card)
st.info(f"🧠 Empfehlung: **{empfohlene_aktion.upper()}**")

# Buttons Runde starten
if st.button("🆕 Neue Session starten"):
    st.session_state.runden = []
    st.session_state.guthaben = start_guthaben
    st.session_state.einsatz = start_einsatz

if st.session_state.guthaben <= 0:
    st.error("❌ Kein Guthaben mehr! Bitte neue Session starten.")
elif len(st.session_state.runden) < max_runden:
    st.subheader(f"🎮 Runde {len(st.session_state.runden)+1}")
    st.write(f"Einsatz: {st.session_state.einsatz} €")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("✅ Gewonnen"):
        st.session_state.guthaben += st.session_state.einsatz
        st.session_state.runden.append(
            {"aktion": empfohlene_aktion, "einsatz": st.session_state.einsatz, "ergebnis": "Gewonnen", "guthaben": st.session_state.guthaben}
        )
        st.session_state.einsatz = start_einsatz  # zurücksetzen
    if col2.button("❌ Verloren"):
        st.session_state.guthaben -= st.session_state.einsatz
        st.session_state.runden.append(
            {"aktion": empfohlene_aktion, "einsatz": st.session_state.einsatz, "ergebnis": "Verloren", "guthaben": st.session_state.guthaben}
        )
        # 1.5x Einsatz oder so viel wie möglich
        next_einsatz = int(st.session_state.einsatz * 1.5)
        st.session_state.einsatz = min(next_einsatz, st.session_state.guthaben)
    if col3.button("➖ Push"):
        st.session_state.runden.append(
            {"aktion": empfohlene_aktion, "einsatz": st.session_state.einsatz, "ergebnis": "Push", "guthaben": st.session_state.guthaben}
        )

# Verlauf anzeigen
if st.session_state.runden:
    st.subheader("📊 Verlauf")
    for i, runde in enumerate(st.session_state.runden, 1):
        farbe = "✅" if runde["ergebnis"] == "Gewonnen" else "❌" if runde["ergebnis"] == "Verloren" else "➖"
        st.write(f"Runde {i} | Aktion: {runde['aktion'].upper()} | Einsatz: {runde['einsatz']} € | Ergebnis: {farbe} ({runde['ergebnis']}) | Guthaben: {runde['guthaben']} €")

    st.success(f"🏁 Endguthaben: {st.session_state.guthaben} €")

