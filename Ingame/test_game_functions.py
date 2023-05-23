from unittest import TestCase
import unittest
import game_functions as gf
import time

# @unittest.skip("시간이 너무 오래 걸림")
# def test_set_window_difficulty_3(self) -> None:
#     uno = UNOGame()
#     for number in self.player_num:
#         self.uno = Game(uno, number, 3)
#         self.uno.set_window()
#         self.assertTrue(self.uno.card_deck, 0)

# @unittest.skip("테스트하는데 오래걸림")
# def test_set_window_player_card(self) -> None:
#     uno = UNOGame()
#     """카드 배열이 성공적으로 나눠지는지 확인, 카드가 개수 및 정확한 카드인지 확인"""
#     for number in self.player_num:
#         for difficulty in self.difficulties:
#             self.uno = Game(uno, number, difficulty)
#             card_deck_len = len(self.uno.set_deck())
#             self.uno.set_window()
#             self.assertEqual(len(self.uno.player), number)
#             for num in range(number):
#                 card = set(self.uno.player[num]) & set(self.test_card_deck)
#                 self.assertSetEqual(set(self.uno.player[num]), card)
#                 if difficulty == 3:
#                     print(len(self.uno.player[num]))
#                     pass
#                     # 일단 보류
#                     self.assertEqual(
#                         len(self.uno.player[num]), card_deck_len // number)
#                 else:
#                     pass
#                     self.assertEqual(len(self.uno.player[num]), 7)
#             del self.uno

# @unittest.skip
# def test_probability_difficulty_two_deck(self) -> None:
#     """기술카드가 50% 더 잘 나오게 하는 테스트"""
#     uno = UNOGame()
#     uno_game = Game(uno)
#     skill_card = 0
#     rest_card = 0
#     for _ in range(1000):
#         uno_game.card_deck = uno_game.set_deck()
#         uno_game.difficulty_two_deck()
#         for card in uno_game.player[1]:
#             if '0' <= card[-1] <= '9':
#                 rest_card += 1
#             else:
#                 skill_card += 1
#     if 0.45 > skill_card / 7000 or skill_card / 7000 > 0.55:
#         self.fail()


class TestGame(TestCase):
    def setUp(self) -> None:
        """시작화면 테스트에서 사용할 selected 상수를 설정합니다."""

        self.uno = gf.Game()
        self.player_num = [2, 3, 4]
        self.difficulties = [1, 2, 3, 4]
        self.test_card_deck = []
        for color in ['red', 'green', 'blue', 'yellow', 'wild']:
            if color != 'wild':
                for number in range(10):
                    self.test_card_deck.append('_'.join([color, str(number)]))
            for skill in ['_pass', '_reverse', '_plus_two', '_basic', '_plus_four', '_change']:
                self.test_card_deck.append(''.join([color, skill]))
        self.test_card_deck.append('red_yellow')
        self.test_card_deck.append("blue_green")

    def test_set_deck(self):
        """카드 묶음이 제대로 생성되는지 확인하는 테스트"""
        card_list = self.uno.set_deck()
        for card_name in card_list:
            self.assertIn(card_name, self.test_card_deck)

    def test_set_deck_len(self) -> None:
        card_list = self.uno.set_deck()
        self.assertEqual(len(card_list), 116)

    def test_measure_set_deck_time(self):
        start_time = time.time()
        print(self.uno.set_deck())
        end_time = time.time()
        execution_time = end_time - start_time
        print("set_deck : ", execution_time)
        if execution_time >= 1.0:
            self.fail()

    @unittest.skip("구현 중")
    def test_player_init(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_hand_out_deck(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_set_name(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_show_name(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_set_window(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_get_next_player(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_show_now_turn(self):
        self.fail()

    # @unittest.skip("구현 중")
    def test_measure_print_computer_box_time(self):
        start_time = time.time()
        self.uno.print_computer_box()
        end_time = time.time()
        execution_time = end_time - start_time
        print("print_computer_box : ", execution_time)
        if execution_time >= 1.0:
            self.fail()

    @unittest.skip("구현 중")
    def test_measure_print_window_time(self):
        start_time = time.time()
        self.uno.print_window()
        end_time = time.time()
        execution_time = end_time - start_time
        print("print_window : ", execution_time)
        if execution_time >= 1.0:
            self.fail()

    @unittest.skip("구현 중")
    def test_draw_color_rect(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_check_card(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_pick_color_card(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_pick_color(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_card_change(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_card_skill(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_pick_player(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_least_num(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_give_card(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_restart(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_no_temp(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_timer(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_check_player(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_selected_turn(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_computer_play(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_startgame(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_playgame(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_user_play(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_get_from_deck(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_pause(self):
        self.fail()

    @unittest.skip("구현 중")
    def test_check_uno_button(self):
        self.fail()

    def tearDown(self) -> None:
        pass
