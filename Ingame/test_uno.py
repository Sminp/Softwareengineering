import unittest
from unittest import TestCase
from unittest.mock import Mock
import pygame
import time
from constant import *
from game_functions import Game
from UNO import UNOGame
from UNO import Button
from settings import Slider


class TestUnoGame(TestCase):
    """Game 클래스 테스트"""

    def setUp(self) -> None:
        """시작화면 테스트에서 사용할 selected 상수를 설정합니다."""
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

    def test_set_deck(self) -> None:
        """카드 묶음이 제대로 생성되는지 테스트"""
        self.uno = Game()
        card_list = self.uno.set_deck()
        for card_name in card_list:
            self.assertIn(card_name, self.test_card_deck)
        del self.uno

    def test_set_deck_len(self) -> None:
        self.uno = Game()
        card_list = self.uno.set_deck()
        for card in self.test_card_deck:
            if card in card_list:
                card_list.remove(card)
        print(card_list)
        self.assertEqual(card_list, 120)

    def test_set_window_difficulty_3(self) -> None:
        for number in self.player_num:
            self.uno = Game(number, 3)
            self.uno.set_window()
            self.assertFalse(self.uno.card_deck, 0)

    @unittest.skip("수정 중")
    def test_print_window_estimate_time(self)-> None:
        """카드 배열이 적절한 시간 내에 나눠지는지 확인"""
        for number in self.player_num:
            for difficulty in self.difficulties:
                self.uno = Game(number, difficulty)
                start = time.time()
                self.uno.print_window()
                end = time.time()
                if end - start >= 1.0:
                    self.fail()

    @unittest.skip("테스트하는데 오래걸림")
    def test_set_window_player_card(self) -> None:
        """카드 배열이 성공적으로 나눠지는지 확인, 카드가 개수 및 정확한 카드인지 확인"""
        for number in self.player_num:
            for difficulty in self.difficulties:
                self.uno = Game(number, difficulty)
                card_deck_len = len(self.uno.set_deck())
                self.uno.set_window()
                self.assertEqual(len(self.uno.player), number)
                for num in range(number):
                    card = set(self.uno.player[num]) & set(self.test_card_deck)
                    self.assertSetEqual(set(self.uno.player[num]), card)
                    if difficulty == 3:
                        print(self.uno.player[num])
                        pass
                        # 일단 보류
                        self.assertEqual(len(self.uno.player[num]), card_deck_len // number)
                    else:
                        pass
                        self.assertEqual(len(self.uno.player[num]), 7)
                del self.uno

    def test_set_window_card_loading(self) -> None:
        pass

    def test_next_turn(self) -> None:
        """현재 턴 표시하는 테스트"""
        pass

    def test_get_next_turn(self) -> None:
        """난이도 4에서 그 다음 턴 표시하는 테스트"""
        pass

    def test_get_next_player(self) -> None:
        """그 다음 턴으로 넘어가게 하는 테스트"""
        pass

    def test_select_player(self) -> None:
        """현재 턴인 플레이어 표시하는 테스트"""
        pass

    def test_print_window(self) -> None:
        """창 업데이트 하는 함수 테스트"""
        pass

    def test_probability_skill_card_difficulty_two(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class TestUNOGame(TestCase):
    def setUp(self) -> None:
        """우노 클래스를 테스트"""
        self.uno = UNOGame()
        self.mouse_pos = []
        for x in range(self.uno.screen_height):
            for y in range(self.uno.screen_width):
                self.mouse_pos.append((x, y))
        self.key_event = []

    def test_main_menu(self):
        pass

    def test_lobby_screen(self):
        pass

    @unittest.skip("마우스 버튼 너무 복잡해서 독립적이지 못함")
    def test_setting_screen(self):
        start = time.time()
        for mouse in self.mouse_pos:
            pygame.mouse.set_pos(mouse)
            self.uno.setting_screen()
        end = time.time()
        print(end - start)

    def test_story(self):
        pass

    def tearDown(self) -> None:
        pass


# class TestPlayer(unittest.TestCase):
#     """직접 플레이어가 되어 실행해보는 테스트"""
#
#     def setUp(self):
#         self.mock_screen = Mock()
#         self.player = Player(0, 0, 5)
#         self.player.screen = self.mock_screen
#
#     def test_move_left(self):
#         self.player.move('left')
#         self.assertEqual(self.player.rect.x, -5)
#
#     def test_move_right(self):
#         self.player.move('right')
#         self.assertEqual(self.player.rect.x, 5)
#
#     def test_draw(self):
#         self.player.draw()
#         self.mock_screen.assert_called_with(pygame.draw.rect(self.mock_screen, (255, 255, 255), self.player.rect))


class TestButton(TestCase):
    def setUp(self) -> None:
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(self.screen, 100, 100, "./image/setting image/169.jpg", 100, 100)
        self.mouse_pos = []
        for x in range(101, 200):
            for y in range(101, 200):
                self.mouse_pos.append((x, y))

    def test_show_button(self):
        pass

    def test_cliked(self):
        pass

    def test_check_cliked_num(self):
        pass

    def test_get_rect(self):
        for mouse in self.mouse_pos:
            self.assertTrue(self.button.get_rect().collidepoint(mouse))


class TestSlider(TestCase):
    def setUp(self) -> None:
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        self.slider = Slider(self.screen, self.screen_width / 2,
                             (self.screen_width * (3 / 10), self.screen_height * (6 / 15)), (0, 100))
        self.length = self.screen_width / 2
        self.poses = [(self.screen_width * (3 / 10), self.screen_height * (4 / 13)), \
                      (self.screen_width * (3 / 10), self.screen_height * (6 / 15))]

    # 비기능 요구사항
    def test_set_value_time_estimate(self):
        for pos in self.poses:
            start = time.time()
            self.slider.set_value(self.length, pos)
            end = time.time()
            if end - start >= 1.0:
                self.fail()

    def test_draw(self):
        pass

    def test_operate(self):
        pass

    def test_draw_value(self):
        pass


if __name__ == '__main__':
    unittest.main()
