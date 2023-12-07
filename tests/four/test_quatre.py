from app.four.code import CardParser, part_two


def test_card_parser():
    card = CardParser.from_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")

    assert card.card_id == 1

    assert card.numbers_have == [41, 48, 83, 86, 17]

    assert card.winning_numbers == [83, 86, 6, 31, 17, 9, 48, 53]

    matches = card.number_matches()

    assert matches == 4

    assert card.score() == 8


def test_part_two():
    card_1 = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    card_2 = "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"
    card_3 = "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"
    card_4 = "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"
    card_5 = "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"
    card_6 = "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"

    cards = [card_1, card_2, card_3, card_4, card_5, card_6]

    cards_parsed = [CardParser.from_card(card) for card in cards]

    result = part_two(cards_parsed)

    expected = 30

    assert result == expected
