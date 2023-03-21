"""게임 기본 설정 저장하는 공간. 버튼 클래스나 setting 클래스가 들어가면 좋지"""
from constant import *

# 게임 기본 설정 저장하는 클래스
class Settings():
    def __init__(self):
        # 게임 설정 초기화
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.bg_color = WHITE

    