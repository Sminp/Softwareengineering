from unittest import TestCase
from Ingame.src.component import computer as com


class TestAI(TestCase):
    def setUp(self) -> None:
        self.player_deck = ['red_5', 'yellow_skip', 'wild_basic', 'blue_draw_two', 'green_reverse', 'wild', 'red_7', 'blue_3',
                       'red_2']

    def test_basic_play_no_matching_card(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 0)

    def test_basic_play_wild_card(self):
        now_card = 'wild_basic'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 'wild_basic')

    def test_basic_play_color_match(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 'yellow_skip')

    def test_basic_play_number_match(self):
        now_card = 'red_5'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 'red_7')

    def test_basic_play_color_number_match(self):
        now_card = 'blue_3'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 'blue_draw_two')

    def test_special_play_no_matching_card(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.special_play(), 0)

    def test_special_play_match(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.special_play(), 'red_5')

    def test_special_play_zero_match(self):
        now_card = 'red_0'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.special_play(), 'green_reverse')

    def test_advanced_play_with_special_cards(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.advanced_play('player2'), 'wild_basic')

    def test_advanced_play_with_one_card_left(self):
        now_card = 'yellow_8'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.advanced_play('player2'), 'red_5')

    def test_advanced_play_with_only_color_matching_cards(self):
        now_card = 'green_5'
        game = com.AI(2, self.player_deck, now_card)
        self.assertIsNone(game.advanced_play('player2'))

    def test_advanced_play_with_no_matching_cards(self):
        now_card = 'green_5'
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.advanced_play('player2'), 'wild_basic')

    """
    def setUp(self):
        self.game = Game()
        self.game.player_num = 3
        self.game.player_deck = ['red_2', 'red_skip', 'blue_5', 'wild', 'wild_4', 'green_4']
        self.game.now_card = 'green_6'

    def test_find_solution(self):
        # Test with multiple valid cards
        self.assertIn(self.game.find_solution(['green']), ['green_4', 'wild'])

        # Test with only one valid card
        self.assertEqual(self.game.find_solution(['6']), 'wild')

        # Test with no valid cards
        self.assertIsNone(self.game.find_solution(['red']))
        """

    def test_find_solution(self):
        self.fail()

    def test_check_same_color(self):
        self.fail()

    def test_calculate_p(self):
        self.fail()
