import pickle
from settings import Settings, resource_path
import os
import sys
import tempfile
import unittest


class ResourcePathTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @unittest.skip ("_MEIPASS를 수정하려면 명령어를 다뤄야 해")
    def test_resource_path(self):
        # 임시 파일 생성
        temp_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(temp_file, "w") as f:
            f.write("test")

        # 상대 경로를 인자로 전달하여 resource_path 함수 호출
        rel_path = os.path.relpath(temp_file, sys._MEIPASS)
        abs_path = resource_path(rel_path)

        # 반환된 경로가 실제 존재하는지 확인
        self.assertTrue(os.path.exists(abs_path))


class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.init_setting = {'screen': [800, 600], 'fullscreen': 0, 'font': 'MALGUNGOTHIC',
                             'keys': {
                                "left": 276,
                                "right": 275,
                                "up": 273,
                                "down": 274,
                                "click": 13
                            },
                            'sound': {
                                "total": 1,
                                "background": 1,
                                "effect": 1
                            }, 'setting_color': False
                            }
        with open("setting.pickle", "wb") as f:
            pickle.dump(self.init_setting, f)

    def tearDown(self):
        pass

    def test_init_setting(self):
        with open("setting.pickle", "rb") as f:
            setting = pickle.load(f)

        self.assertEqual(setting, self.init_setting)

    def test_set_setting(self):
        changed_setting = {
            'screen': [1280, 720],
            'fullscreen': 1,
            'font': 'MALGUNGOTHIC',
            'keys': {
                "left": 276,
                "right": 275,
                "up": 273,
                "down": 274,
                "click": 13
            },
            'sound': {
                "total": 1,
                "background": 0.5,
                "effect": 1
            },
            'setting_color': True
        }

        self.settings.change_setting(changed_setting)

        with open("setting.pickle", "rb") as f:
            setting = pickle.load(f)

        self.assertEqual(setting, changed_setting)

    def test_window_change(self):
        self.settings.window_change(16)
        self.assertEqual(self.settings.screen_width, 1280)
        self.assertEqual(self.settings.screen_height, 720)