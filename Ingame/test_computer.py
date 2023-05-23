from unittest import TestCase
import computer as com


class TestAI(TestCase):
    def setUp(self) -> None:
        self.player_deck = ['red_5', 'yellow_pass', 'wild_basic', 'blue_draw_two', 'green_reverse', 'wild_basic',
                            'red_7', 'blue_3', 'red_2']
        player_deck_solution = ['red_2', 'red_pass', 'blue_5', 'wild_basic', 'wild_4', 'green_4']
        now = 'green_6'
        self.game = com.AI(3, player_deck_solution, now)

    def test_basic_play_no_matching_card(self):
        now_card = ['yellow_8']
        player_deck = ['red_5', 'yellow_skip', 'blue_draw_two', 'green_reverse', 'red_7', 'blue_3', 'red_2']
        game = com.AI(2, player_deck, now_card)
        self.assertEqual(game.basic_play(), 'yellow_skip')

    def test_basic_play_wild_card(self):
        now_card = ['wild_basic']
        game = com.AI(2, self.player_deck, now_card)
        self.assertIn(game.basic_play(), self.player_deck)

    def test_basic_play_color_match(self):
        now_card = ['yellow_8']
        player_deck = ['red_5', 'yellow_3', 'blue_draw_two', 'green_reverse', 'red_7', 'blue_3', 'red_2']
        game = com.AI(2, player_deck, now_card)
        self.assertEqual(game.basic_play(), 'yellow_3')

    def test_basic_play_number_match(self):
        now_card = ['red_7']
        player_deck = ['yellow_3', 'blue_draw_two', 'green_reverse', 'yellow_7', 'blue_3']
        game = com.AI(2, player_deck, now_card)
        self.assertEqual(game.basic_play(), 'yellow_7')

    #흠...
    def test_basic_play_color_number_match(self):
        now_card = ['blue_3']
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.basic_play(), 'blue_draw_two')

    def test_special_play_no_matching_card(self):
        now_card = ['yellow_8']
        game = com.AI(2, self.player_deck, now_card)
        self.assertEqual(game.special_play(), 0)

    def test_special_play_match(self):
        now_card = ['yellow_8']
        player_deck = ['red_5', 'green_7', 'blue_3', 'green_2']
        game = com.AI(2, player_deck, now_card)
        self.assertEqual(game.special_play(), 'green_2')

    def test_special_play_zero_match(self):
        now_card = ['red_0']
        player_deck = ['red_5', 'green_7', 'blue_3', 'green_2']
        game = com.AI(2, player_deck, now_card)
        self.assertIn(game.special_play(), player_deck)

    def test_advanced_play_with_special_cards(self):
        now_card = ['yellow_8']
        game = com.AI(2, self.player_deck, now_card)
        self.assertIn(game.advanced_play('player2'), ['wild_basic', 'yellow_pass'])

    def test_advanced_play_with_one_card_left(self):
        now_card = ['yellow_8']
        game = com.AI(2, self.player_deck, now_card)
        self.assertIn(game.advanced_play('player2'), ['red_5', 'yellow_pass'])

    def test_advanced_play_with_only_color_matching_cards(self):
        now_card = ['green_5']
        player_deck = ['red_1', 'yellow_pass', 'red_7', 'blue_3', 'red_2']
        game = com.AI(2, player_deck, now_card)
        self.assertIsNone(game.advanced_play('player2'))

    def test_advanced_play_with_no_matching_cards(self):
        now_card = ['green_5']
        game = com.AI(2, self.player_deck, now_card)
        self.assertIn(game.advanced_play('player2'), ['wild_basic',  'green_reverse'])

    def test_find_solution(self):
        # Test with multiple valid cards
        self.assertIn(self.game.find_solution(['green', '10']), ['green_4', 'wild_basic'])

        # Test with only one valid card
        self.assertEqual(self.game.find_solution(['purple', '6']), ['wild_basic'])

    def test_find_no_solution(self):
        player_deck = ['green_6', 'blue_1']
        game = com.AI(3, player_deck, ['red_10'])
        self.assertIsNone(game.find_solution(['red', '10']))

    def test_check_same_color(self):
        self.game.player_deck = ['red_1', 'blue_2', 'red_3', 'green_4']
        self.assertEqual(self.game.check_same_color('red'), True)
        self.assertEqual(self.game.check_same_color('blue'), False)
        self.assertEqual(self.game.check_same_color('green'), False)

        self.game.player_deck = ['wild', 'red_2', 'yellow_5']
        self.assertEqual(self.game.check_same_color('red'), False)
        self.assertEqual(self.game.check_same_color('blue'), False)
        self.assertEqual(self.game.check_same_color('yellow'), False)

    def test_calculate_p(self):
        game = com.AI(2, None, [0])
        game.wastes = ['red_5', 'yellow_7', 'green_skip']
        game.player_deck = ['yellow_2', 'green_reverse', 'red_9']
        result = game.calculate_p(['yellow_2', 'green_reverse', 'red_9'])
        self.assertEqual(result, 'red_9')

        game.wastes = ['red_5', 'yellow_7', 'green_skip']
        game.player_deck = ['yellow_2', 'green_reverse', 'wild']
        result = game.calculate_p(['yellow_2', 'green_reverse', 'wild'])
        self.assertEqual(result, 'yellow_2')
