"""
Advent of code 2023 template file

Author: Alex Traveylan
Date: 2023-12-06
"""
import time

from app.template import get_example, get_input, ints, submit

if __name__ == "__main__":
    DAY = 7
    PART = 2
    exemple_or_real = int(input("Exemple (0) ou Réel (1) ? "))

    if exemple_or_real == 0:
        s = get_example(DAY).strip()
    else:
        s = get_input(DAY).strip()

    debut = time.perf_counter()
    # Your code here

    camel_card_keys = "AKQT98765432J"
    camel_card = {key: i + 1 for i, key in enumerate(camel_card_keys[::-1])}

    reversed_camel_card = {value: key for key, value in camel_card.items()}

    def line_into_hand_score(line: str) -> tuple[str, int]:
        """Convert a line into a hand and a score"""
        hand, score = line.split()
        return hand, int(score)

    def max_card(hand: str) -> str:
        if hand == "JJJJJ":
            return "J"

        set_hand = list(set(hand))
        max_card_count = sorted(
            [(hand.count(card), card) for card in set_hand if card != "J"],
            key=lambda x: (x[0], camel_card[x[1]]),
            reverse=True,
        )

        return max_card_count[0][1]

    def change_J_to_max_count(hand: str) -> str:
        copy_hand = hand
        max_card_count = max_card(hand)
        return copy_hand.replace("J", max_card_count)

    def file_into_hands_scores(file: str) -> list[tuple[str, int]]:
        """Convert a file into a list of hands and scores"""
        return [line_into_hand_score(line) for line in file.splitlines()]

    def is_five_of_a_kind(hand: str) -> bool:
        """Check if a hand is a five of a kind"""
        return len(set(hand)) == 1

    def is_four_of_a_kind(hand: str) -> bool:
        """Check if a hand is a four of a kind"""
        set_hand = list(set(hand))
        return len(set_hand) == 2 and (
            hand.count(set_hand[0]) == 4 or hand.count(set_hand[1]) == 4
        )

    def is_full_house(hand: str) -> bool:
        set_hand = list(set(hand))
        return len(set_hand) == 2 and (
            (hand.count(set_hand[0]) == 3 and hand.count(set_hand[1]) == 2)
            or (hand.count(set_hand[0]) == 2 and hand.count(set_hand[1]) == 3)
        )

    def is_three_of_a_kind(hand: str) -> bool:
        set_hand = list(set(hand))
        return len(set_hand) == 3 and (
            hand.count(set_hand[0]) == 3
            or hand.count(set_hand[1]) == 3
            or hand.count(set_hand[2]) == 3
        )

    def is_two_pairs(hand: str) -> bool:
        return len(set(hand)) == 3

    def is_one_pair(hand: str) -> bool:
        return len(set(hand)) == 4

    def is_high_card(hand: str) -> bool:
        return len(set(hand)) == 5

    def detect_hand(hand: str) -> int:
        changed_hand = change_J_to_max_count(hand)

        if is_five_of_a_kind(changed_hand):
            return 7
        elif is_four_of_a_kind(changed_hand):
            return 6
        elif is_full_house(changed_hand):
            return 5
        elif is_three_of_a_kind(changed_hand):
            return 4
        elif is_two_pairs(changed_hand):
            return 3
        elif is_one_pair(changed_hand):
            return 2
        elif is_high_card(changed_hand):
            return 1
        else:
            raise ValueError("Hand not recognized")

    def strongest_card_index(hand: str, index: int) -> str:
        return camel_card[hand[index]]

    def order_hands(hands_scores: list[tuple[str, int]]) -> list[str]:
        return sorted(
            hands_scores,
            key=lambda hand_score: (
                detect_hand(hand_score[0]),
                strongest_card_index(hand_score[0], 0),
                strongest_card_index(hand_score[0], 1),
                strongest_card_index(hand_score[0], 2),
                strongest_card_index(hand_score[0], 3),
                strongest_card_index(hand_score[0], 4),
            ),
        )

    hands_scores = file_into_hands_scores(s)

    sorted_hands_scores = order_hands(hands_scores)

    ans = 0
    for i, (hand, score) in enumerate(sorted_hands_scores):
        ans += score * (i + 1)

    # fin du code
    fin = time.perf_counter()
    print(f"Temps d'exécution : {fin - debut:.2f} secondes")
    if exemple_or_real == 1:
        submit(DAY, PART, ans)
    else:
        print(ans)
