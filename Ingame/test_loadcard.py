import pygame
import unittest
from unittest.mock import Mock
import loadcard as lc


class TestCard(unittest.TestCase):
    def test_init(self):
        name = 'back'
        position = (100, 100)
        size = (50, 50)

        card = lc.Card(name, position, size)

        self.assertEqual(card.name, name)
        self.assertEqual(card.size, size)
        self.assertEqual(card.orig_pos, position)
        self.assertEqual(card.position, position)
        self.assertEqual(card.user_rotation, 30)
        self.assertEqual(card.get_name(), name)
        self.assertEqual(card.getposition(), position)
        self.assertEqual(card.get_rect().center, position)

    def test_update(self):
        name = 'back'
        position = (100, 100)
        size = (50, 50)

        card = lc.Card(name, position, size)
        card.image = Mock()
        card.image.get_rect = Mock(return_value=Mock(center=position))

        # 애니메이션 확인
        dest_loc = (107.07106781186548, 107.07106781186548)
        card.update(dest_loc)

        self.assertEqual(card.position, dest_loc)
        card.image.get_rect.assert_called_once_with()


class TestPopup(unittest.TestCase):

    def test_init(self):
        name = 'back'
        position = (100, 100)
        sprite = pygame.sprite.Sprite()
        sprite.image = Mock()
        sprite.rect = Mock(name='sprite.rect')
        pygame.image.load = Mock(return_value=sprite.image)

        popup = lc.Popup(name, position)

        pygame.image.load.assert_called_once_with('../image/card_img/back.png')
        self.assertEqual(popup.name, name)
        self.assertEqual(popup.position, position)
        self.assertEqual(popup.image, sprite.image)

    def test_get_name(self):
        name = 'back'
        position = (100, 100)
        popup = lc.Popup(name, position)

        self.assertEqual(popup.get_name(), name)

    def test_get_rect(self):
        name = 'blue'
        position = (100, 100)
        popup = lc.Popup(name, position)

        rect = popup.get_rect()

        self.assertEqual(rect, popup.rect)