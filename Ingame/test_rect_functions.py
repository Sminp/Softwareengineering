import unittest
import pygame
import constant as c
import rect_functions as rf


class TestTextRect(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.font = c.MALGUNGOTHIC
        self.text = "Test Text"
        self.text_size = 24
        self.text_color = c.BLACK
        self.text_rect = rf.TextRect(self.screen, self.text, self.text_size, self.text_color)

    def test_text_surface(self):
        expected_surface = pygame.Surface((0, 0))  # 예상 Surface
        font = pygame.font.SysFont(self.font, self.text_size)
        expected_surface = font.render(self.text, True, self.text_color)
        self.assertEqual(str(self.text_rect.text_surface()), str(expected_surface))

    def test_text_rect(self):
        expected_rect = pygame.Rect((0, 0, 0, 0))  # 예상 Rect
        expected_rect = self.text_rect.text_surface().get_rect()
        self.assertEqual(self.text_rect.text_rect(), expected_rect)

    @unittest.skip("물어볼게..")
    def test_change_text_surface(self):
        new_text = "New Test Text"
        self.text_rect.change_text_surface(new_text)
        self.assertEqual(self.text_rect.text, new_text)

    def test_change_color(self):
        new_color = c.BLUE
        self.text_rect.change_color(new_color)
        self.assertEqual(self.text_rect.text_color, new_color)


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.x = 100
        self.y = 100
        self.img = "./image/UnoButton.png"
        self.width = 200
        self.height = 50
        self.button = rf.Button(self.screen, self.x, self.y, self.img, self.width, self.height)

    def test_show(self):
        self.button.show()
        # TODO: Test the display of the button on the screen

    def test_highlight(self):
        self.button.highlight()
        # TODO: Test the display of the highlighted button on the screen

    def test_get_rect(self):
        expected_rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.assertEqual(self.button.get_rect(), expected_rect)


class TestSlider(unittest.TestCase):
    def test_set_value(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        slider = rf.Slider(screen, "Slider Test", 300, (100, 100), (0, 100), c.BLACK, c.RED)
        length = 400
        pos = (200, 200)
        slider.set_value(length, pos)
        self.assertEqual(slider.length, length)
        self.assertEqual(slider.x, pos[0])
        self.assertEqual(slider.y, pos[1])
        self.assertEqual(slider.button.x, int(pos[0] + 18 / 40 * length))
        self.assertEqual(slider.button.y, int(pos[1] - 1 / 40 * length))
        self.assertEqual(slider.button.width, int(length * 1 / 20))
        self.assertEqual(slider.button.height, int(length * 1 / 20))
