from unittest import TestCase
import unittest
import timer
import pygame


class TestTimer(TestCase):

    def test_reset_tmr(self):
        pygame.init()
        t = timer.Timer()
        t.reset_tmr()
        self.assertNotEqual(t.start_time, 0)

    def test_tick_tmr(self):
        pygame.init()
        t = timer.Timer()
        t.reset_tmr()
        self.assertFalse(t.tick_tmr())
        t.current_time = 11
        self.assertIsNone(t.tick_tmr())


if __name__ == '__main__':
    unittest.main()