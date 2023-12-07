from pathlib import Path
from app.main import read_input_file


class CardParser:
    def __init__(
        self, card_id: int, numbers_have: list[int], winning_numbers: list[int]
    ):
        self.card_id = card_id
        self.numbers_have = numbers_have
        self.winning_numbers = winning_numbers

    def __repr__(self):
        return f"CardParser(card_id={self.card_id}, numbers_have={self.numbers_have}, winning_numbers={self.winning_numbers})"

    @classmethod
    def from_card(cls, card: str):
        """
        Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
        to
        CardParser(card_id=1, numbers_have=[41, 48, 83, 86, 17], winning_numbers=[83, 86, 6, 31, 17, 9, 48, 53])
        """

        card_id, numbers = card.strip().split(":")
        card_id = int(card_id.split()[1])

        numbers_have, winning_numbers = numbers.strip().split("|")
        numbers_have = [int(n) for n in numbers_have.strip().split()]
        winning_numbers = [int(n) for n in winning_numbers.strip().split()]

        return cls(card_id, numbers_have, winning_numbers)

    def number_matches(self):
        return len(set(self.numbers_have) & set(self.winning_numbers))

    def score(self):
        matches = self.number_matches()

        if matches == 0:
            return 0

        else:
            return 2 ** (matches - 1)

    def copy(self):
        return CardParser(
            self.card_id, self.numbers_have.copy(), self.winning_numbers.copy()
        )


def part_two(cards: list[CardParser]):
    cards_with_quantity = [
        [card, quantity] for card, quantity in zip(cards, [1] * len(cards))
    ]

    for index, (card, quantity) in enumerate(cards_with_quantity):
        matches = card.number_matches()

        if matches != 0:
            for i in range(matches):
                cards_with_quantity[index + i + 1][1] += quantity

    return sum(quantity for _, quantity in cards_with_quantity)


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    cards = [CardParser.from_card(line) for line in lines]

    print(sum([card.score() for card in cards]))

    print(part_two(cards))
