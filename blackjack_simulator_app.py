# blackjack_simulator_app.py

import random
import streamlit as st

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

def simulate_hand(player_hand, dealer_card, action, einsatz=10):
    # Blackjack direkt auswerten
    if action == "blackjack" and hand_value(player_hand) == 21 and len(player_hand) == 2:
        dealer_hand = [dealer_card, draw_card()]
        if hand_value(dealer_hand) == 21:
            return 0  # Push
        return einsatz * 1.5

    # Spieleraktion simulieren
    if action == "double":
        player_hand.append(draw_card())
        player_total = hand_value(player_hand)
        if player_total > 21:
            return -einsatz * 2
    else:
        while action == "hit" and hand_value(player_hand) < 21:
            player_hand.append(draw_card())
        player_total = hand_value(player_hand)
        if player_total > 21:
            return -einsatz

    # Dealer zieht
    dealer_hand = [dealer_card, draw_card()]
    while hand_value(dealer_hand) < 17 or (hand_value(dealer_hand) == 17 and is_soft(dealer_hand)):
        dealer_hand.append(draw_card())
    dealer_total = hand_value(dealer_hand)

    # Ergebnis berechnen
    if player_total > 21:
        return -einsatz
    elif dealer_total > 21 or player_total > dealer_total:
        return einsatz * (2 if action == "double" else 1)
    elif player_total < dealer_total:
        return -einsatz * (2 if action == "double" else 1)
    else:
        return 0  # Push

def simulate_blackjack(player_total, dealer_card, einsatz=10, rounds=100_000):
    actions = ["stand", "hit", "double"]
    possible_hands = []

    # Alle 2-Karten-Kombis mit dem gewünschten player_total finden
    for card1 in cards:
        for card2 in cards:
            hand = [card1, card2]
            if hand_value(hand) == player_total:
                possible_hands.append(hand)

    if not possible_hands:
        return {}, ("Keine gültigen Hände", {})

    results = {a: [] for a in actions}
    results["blackjack"] = []

    for _ in range(rounds):
        hand = random.choice(possible_hands)
        # Blackjack-Check
        if hand_value(hand) == 21 and len(hand) == 2:
            results["blackjack"].append(simulate_hand(hand[:], dealer_card, "blackjack", einsatz))
            continue

        for action in actions:
            res = simulate_hand(hand[:], dealer_card, action, einsatz)
            results[action].append(res)

    def analyse(results):
        total = len(results)
        if total == 0:
            return {"win": 0, "loss": 0, "push": 0, "average": 0}
        wins = sum(1 for r in results if r > 0)
        losses = sum(1 for r in results if r < 0)
        pushes = total - wins - losses
        avg = sum(results) / total
        return {
            "win": wins / total,
            "loss": losses / total,
            "push": pushes / total,
            "average": avg
        }

    stats = {action: analyse(results[action]) for action in results}
    best_action = max(stats.items(), key=lambda x: x[1]["average"])
    return stats, best_action

# --- Streamlit UI ---
st.set_page_config(page_title="Blackjack Simulator", layout="centered")
st.title("🃏 Blackjack Entscheidungs-Simulator")

col1, col2 = st.columns(2)
player_total = col1.number_input("🧍 Spieler Total", min_value=4, max_value=21, value=12)
dealer_card = col2.number_input("🪙 Dealer Karte", min_value=2, max_value=11, value=10)
einsatz = st.slider("💰 Einsatz (€)", 1, 1_000_000_000_000_000_000, 10, 1)
rounds = st.slider("🔁 Runden", 1000, 500_000, 100_000, step=1000)

if st.button("Simulation starten"):
    with st.spinner("Simuliere..."):
        stats, best = simulate_blackjack(player_total, dealer_card, einsatz, rounds)

    for action, data in stats.items():
        st.subheader(f"{action.upper()}")
        st.write(f"✅ Gewinn: {data['win']:.2%}")
        st.write(f"❌ Verlust: {data['loss']:.2%}")
        st.write(f"➖ Push: {data['push']:.2%}")
        st.write(f"📈 Ø Gewinn/Verlust pro Runde: {data['average']:.2f} €")

    st.success(f"➡ Beste Entscheidung: **{best[0].upper()}** mit Ø {best[1]['average']:.2f} € pro Runde")
