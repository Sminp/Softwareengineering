import unittest
from unittest import TestCase
from unittest.mock import Mock
import pygame
import time
from constant import *
from settings import Settings
from rect_functions import Button, Slider
from UNO import UNOGame
from player import Player
import time



class TestPlayer(unittest.TestCase):
    """직접 플레이어가 되어 실행해보는 테스트"""

    @unittest.skip("수정 중")
    def setUp(self):
        self.mock_screen = Mock()
        self.player = Player(0, 0, 5)
        self.player.screen = self.mock_screen

    @unittest.skip("수정 중")
    def test_move_left(self):
        self.player.move('left')
        self.assertEqual(self.player.rect.x, -5)

    @unittest.skip("수정 중")
    def test_move_right(self):
        self.player.move('right')
        self.assertEqual(self.player.rect.x, 5)

    @unittest.skip("수정 중")
    def test_draw(self):
        self.player.draw()
        self.mock_screen.assert_called_with(pygame.draw.rect(
            self.mock_screen, (255, 255, 255), self.player.rect))


class TestButton(unittest.TestCase):
    @unittest.skip("수정 중")
    def setUp(self) -> None:
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(self.screen, 100, 100,
                             "./image/setting image/169.jpg", 100, 100)
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

    @unittest.skip("수정 중")
    def test_get_rect(self):
        for mouse in self.mouse_pos:
            self.assertTrue(self.button.get_rect().collidepoint(mouse))


class TestSlider(unittest.TestCase):
    @unittest.skip("수정 중")
    def setUp(self) -> None:
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.screen = pygame.display.set_mode(
            (self.screen_height, self.screen_width))
        self.slider = Slider(self.screen, self.screen_width / 2,
                             (self.screen_width * (3 / 10), self.screen_height * (6 / 15)), (0, 100))
        self.length = self.screen_width / 2
        self.poses = [(self.screen_width * (3 / 10), self.screen_height * (4 / 13)),
                      (self.screen_width * (3 / 10), self.screen_height * (6 / 15))]

    @unittest.skip("수정 중")
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


class TestUNOGame(TestCase):
    def test_bg_img_load(self):
        self.fail()

    def test_object_init(self):
        self.fail()

    def test_object_show(self):
        self.fail()

    def test_sound(self):
        self.fail()

    def test_handle_event(self):
        self.fail()

    def test_menu(self):
        self.fail()

    def test_key_select_screen(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
