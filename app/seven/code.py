"""
Advent of code 2023 template file

Author: Alex Traveylan
Date: 2023-12-06
"""
import time

from app.template import get_example, get_input, ints, submit

if __name__ == "__main__":
    DAY = 7
    PART = 1
    s = get_input(DAY).strip()
    # s = get_example(DAY).strip()
    debut = time.perf_counter()
    # Your code here

    camel_card_keys = "AKQJT98765432"
    camel_card = {key: i + 2 for i, key in enumerate(camel_card_keys[::-1])}

    def line_into_hand_score(line: str) -> tuple[str, int]:
        """Convert a line into a hand and a score"""
        hand, score = line.split()
        return hand, int(score)

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

    def detect_hand(hand: str) -> int:
        if is_five_of_a_kind(hand):
            return 7
        elif is_four_of_a_kind(hand):
            return 6
        elif is_full_house(hand):
            return 5
        elif is_three_of_a_kind(hand):
            return 4
        elif is_two_pairs(hand):
            return 3
        elif is_one_pair(hand):
            return 2
        else:
            return 1

    def score_first_hand_card(hand: str) -> int:
        set_card = list(set(hand))
        _, card = max((hand.count(card), card) for card in set_card)

        return camel_card[card]

    def score_second_hand_card(hand: str) -> int:
        set_card = list(set(hand))
        if len(set_card) > 1:
            count_card = sorted((hand.count(card), card) for card in set_card)
            return camel_card[count_card[1][1]]
        else:
            return 0

    def score_third_hand_card(hand: str) -> int:
        set_card = list(set(hand))
        if len(set_card) > 2:
            count_card = sorted((hand.count(card), card) for card in set_card)
            return camel_card[count_card[2][1]]
        else:
            return 0

    def score_fourth_hand_card(hand: str) -> int:
        set_card = list(set(hand))
        if len(set_card) > 3:
            count_card = sorted((hand.count(card), card) for card in set_card)
            return camel_card[count_card[3][1]]
        else:
            return 0

    def order_hands(hands_scores: list[tuple[str, int]]) -> list[str]:
        return sorted(
            hands_scores,
            key=lambda hand_score: (
                detect_hand(hand_score[0]),
                score_first_hand_card(hand_score[0]),
                score_second_hand_card(hand_score[0]),
                score_third_hand_card(hand_score[0]),
                score_fourth_hand_card(hand_score[0]),
            ),
        )

    hands_scores = file_into_hands_scores(s)

    sorted_hands_scores = order_hands(hands_scores)

    print(sorted_hands_scores)

    ans = 0
    for i, (hand, score) in enumerate(sorted_hands_scores):
        ans += score * (i + 1)

    print(ans)
    # fin du code
    fin = time.perf_counter()
    print(f"Temps d'exécution : {fin - debut:.2f} secondes")
    submit(DAY, PART, ans)
