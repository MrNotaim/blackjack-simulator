# blackjack_simulator_app.py

import random
import streamlit as st

# --- Blackjack Hilfsfunktionen ---
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

def draw_card():
    return random.choice(cards)

def hand_value(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_soft(hand):
    return 11 in hand and hand_value(hand) <= 21

def basic_strategy(player_total, dealer_card):
    # Sehr vereinfachte Strategie
    if player_total >= 17:
        return "stand"
    elif player_total >= 13 and dealer_card <= 6:
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

def simulate_round(player_total, dealer_card, action, einsatz):
    player_hand = [player_total - draw_card(), draw_card()]  # Dummy Hand mit gew. total
    while hand_value(player_hand) != player_total:
        player_hand = [draw_card(), draw_card()]
        if hand_value(player_hand) > player_total:
            player_hand = [player_total - 1, 1]  # Zurücksetzen

    if action == "double":
        einsatz *= 2
        player_hand.append(draw_card())
    elif action == "hit":
        while hand_value(player_hand) < 17:
            player_hand.append(draw_card())

    player_score = hand_value(player_hand)
    if player_score > 21:
        return -einsatz

    dealer_hand = [dealer_card, draw_card()]
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card())
    dealer_score = hand_value(dealer_hand)

    if dealer_score > 21 or player_score > dealer_score:
        return einsatz
    elif player_score < dealer_score:
        return -einsatz
    else:
        return 0

# --- Streamlit UI ---
st.set_page_config(page_title="Blackjack Einsatz-Bot", layout="centered")
st.title("🎯 Blackjack Einsatz-Strategie mit Bankroll-Verwaltung")

col1, col2 = st.columns(2)
player_total = col1.number_input("🧍 Spieler Total", min_value=4, max_value=21, value=12)
dealer_card = col2.number_input("🪙 Dealer Karte", min_value=2, max_value=11, value=6)

start_capital = st.number_input("💼 Startguthaben (€)", min_value=1, value=100_000)
initial_bet = st.number_input("🎯 Starteinsatz (€)", min_value=1, value=10_000)
rounds = st.slider("🔁 Anzahl Runden", 1, 100, 10)

if st.button("🔍 Simulation starten"):
    capital = start_capital
    einsatz = initial_bet
    verlauf = []

    for i in range(1, rounds + 1):
        if capital < 1:
            verlauf.append((i, "-", einsatz, "STOP", 0, capital))
            break

        action = basic_strategy(player_total, dealer_card)
        einsatz = min(einsatz, capital)  # Nicht mehr setzen als Kapital
        ergebnis = simulate_round(player_total, dealer_card, action, einsatz)
        capital += ergebnis

        if ergebnis > 0:
            next_bet = int(einsatz * 0.9)
        elif ergebnis < 0:
            next_bet = int(einsatz * 2) if capital >= einsatz * 2 else capital
        else:
            next_bet = einsatz

        verlauf.append((i, action.upper(), einsatz, "✅" if ergebnis > 0 else ("❌" if ergebnis < 0 else "➖"), ergebnis, capital))
        einsatz = next_bet

    st.subheader("📊 Verlauf")
    for eintrag in verlauf:
        st.write(f"Runde {eintrag[0]} | Aktion: {eintrag[1]} | Einsatz: {eintrag[2]} € | Ergebnis: {eintrag[3]} ({eintrag[4]} €) | Guthaben: {eintrag[5]} €")

    st.success(f"🏁 Endguthaben: {capital} €")

