from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
import pygame
import sys
import UNO


class TestUnoGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = UNO.UNOGame()

    def test_text_format(self):
        # 텍스트 형식이 제대로 렌더링되는지 테스트
        text = UNO.text_format("Hello", "Arial", 24, UNO.c.BLACK)
        self.assertIsInstance(text, pygame.Surface)
        self.assertEqual(text.get_width(), 44)
        self.assertEqual(text.get_height(), 28)

    def test_terminate(self):
        # 종료 함수가 예외 없이 실행되는지 테스트
        with self.assertRaises(SystemExit):
            UNO.terminate()


class TestUNOGame(TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((255, 255, 255))
        self.game_screen = UNO.UNOGame()

    def tearDown(self):
        pygame.quit()

    def test_screen_size(self):
        self.assertEqual(self.game_screen.size, [800, 600])

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


class TestTitleMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.title_menu = UNO.TitleMenu()

    def test_init(self):
        self.assertIsInstance(self.title_menu.screen, pygame.Surface)
        self.assertEqual(
            self.title_menu.screen.get_size()[0], self.title_menu.settings['screen'][0])
        self.assertEqual(
            self.title_menu.screen.get_size()[1], self.title_menu.settings['screen'][1])
        self.assertEqual(self.title_menu.x, self.title_menu.settings['screen'][0] * (1 / 4))
        self.assertEqual(self.title_menu.y, self.title_menu.settings['screen'][1] * (5 / 8))
        self.assertEqual(self.title_menu.width, self.title_menu.settings['screen'][0] * (1 / 8))
        self.assertEqual(self.title_menu.height, self.title_menu.settings['screen'][1] * (3 / 8))
        self.assertIsInstance(self.title_menu.button_li, list)

    def test_object_init(self):
        self.assertIsInstance(self.title_menu.object_init(), list)
        self.assertIsInstance(self.title_menu.object_init()[0], UNO.rf.Button)

    def test_object_show(self):
        self.assertIsNone(self.title_menu.object_show(*self.title_menu.button_li))

    def test_sound(self):
        self.assertIsNone(self.title_menu.sound())

    @unittest.skip("수정중")
    def test_handle_event(self):
        event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(event)
        with self.assertRaises(SystemExit):
            self.title_menu.handle_event()
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pygame.init()
        pygame.event.post(event)
        self.assertIsNone(self.title_menu.handle_event())
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        pygame.event.post(event)
        self.assertIsNone(self.title_menu.handle_event())
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        pygame.event.post(event)
        self.assertIsNone(self.title_menu.handle_event())
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_0)
        pygame.event.post(event)
        self.assertIsNone(self.title_menu.handle_event())
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(100, 100))
        pygame.event.post(event)
        self.assertIsNone(self.title_menu.handle_event())

    @unittest.skip
    def test_menu(self):
        with self.assertRaises(SystemExit):
            self.title_menu.menu()


class TestLobbyScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.lobby = UNO.LobbyScreen()

    def test_object_init(self):
        self.assertEqual(len(self.lobby.computer_rect), 5)
        self.assertIsInstance(self.lobby.computer_rect[0][0], pygame.Rect)
        self.assertIsInstance(self.lobby.computer_rect[0][1], str)

    @unittest.skip("수정")
    def test_object_show(self):
        with patch('pygame.display.update') as mock_update:
            self.lobby.object_show()
            mock_update.assert_called_once()

    @unittest.skip("수정")
    def test_handle_event(self):
        # Test for QUIT event
        mock_quit_event = Mock()
        mock_quit_event.type = pygame.QUIT
        with patch('pygame.event.get', return_value=[mock_quit_event]):
            with self.assertRaises(SystemExit):
                self.lobby.handle_event()

        # Test for MOUSEBUTTONDOWN event
        mock_button_down_event = Mock()
        mock_button_down_event.type = pygame.MOUSEBUTTONDOWN
        mock_button_down_event.pos = (320, 240)
        with patch('pygame.event.get', return_value=[mock_button_down_event]):
            with patch('UNO.gf.Game.startgame') as mock_startgame:
                self.lobby.handle_event()
                mock_startgame.assert_called_once_with()

        # Test for KEYDOWN event
        mock_keydown_event = Mock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.unicode = 'a'
        with patch('pygame.event.get', return_value=[mock_keydown_event]):
            self.lobby.handle_event()
            self.assertEqual(self.lobby.user_name, 'playera')

    def tearDown(self):
        pygame.quit()
