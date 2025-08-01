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
    if action == "blackjack" and hand_value(player_hand) == 21 and len(player_hand) == 2:
        dealer_hand = [dealer_card, draw_card()]
        if hand_value(dealer_hand) == 21:
            return 0
        return einsatz * 1.5

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

    dealer_hand = [dealer_card, draw_card()]
    while hand_value(dealer_hand) < 17 or (hand_value(dealer_hand) == 17 and is_soft(dealer_hand)):
        dealer_hand.append(draw_card())
    dealer_total = hand_value(dealer_hand)

    if player_total > 21:
        return -einsatz
    elif dealer_total > 21 or player_total > dealer_total:
        return einsatz * (2 if action == "double" else 1)
    elif player_total < dealer_total:
        return -einsatz * (2 if action == "double" else 1)
    else:
        return 0

def simulate_blackjack(player_total, dealer_card, einsatz=10, rounds=100_000):
    actions = ["stand", "hit", "double"]
    possible_hands = []
for card1 in cards:
    for card2 in cards:
        hand = [card1, card2]
        if hand_value(hand) == player_total:
            possible_hands.append(hand)


    results = {a: [] for a in actions}
    results["blackjack"] = []

    for _ in range(rounds):
        hand = random.choice(possible_hands)
        if hand_value(hand) == 21 and len(hand) == 2:
            results["blackjack"].append(simulate_hand(hand[:], dealer_card, "blackjack", einsatz))
            continue

        for action in actions:
            res = simulate_hand(hand[:], dealer_card, action, einsatz)
            results[action].append(res)

   def simulate_blackjack(player_total, dealer_card, einsatz=10, rounds=100_000):
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    def hand_value(hand):
        total = sum(hand)
        # Ass als 1 zählen, wenn Gesamt > 21
        aces = hand.count(11)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def simulate_hand(hand, dealer_card, action, einsatz):
        # Simuliere Spieleraktion (stand, hit, double)
        player_total = hand_value(hand)
        if action == "hit":
            hand.append(random.choice(cards))
            player_total = hand_value(hand)
            if player_total > 21:
                return -einsatz  # verloren
        elif action == "double":
            hand.append(random.choice(cards))
            player_total = hand_value(hand)
            einsatz *= 2
            if player_total > 21:
                return -einsatz

        # Dealer zieht
        dealer_hand = [dealer_card, random.choice(cards)]
        dealer_total = hand_value(dealer_hand)
        while dealer_total < 17:
            dealer_hand.append(random.choice(cards))
            dealer_total = hand_value(dealer_hand)

        # Ergebnis
        if player_total > 21:
            return -einsatz
        elif dealer_total_


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
        st.write(f"📈 Ø Gewinn/Verlust pro Runde: `{data['average']:.2f} €`")

    st.success(f"➡ Beste Entscheidung: **{best[0].upper()}** mit Ø `{best[1]['average']:.2f} €` pro Runde")
