"""게임 기본 설정 저장하는 공간. 버튼 클래스나 setting 클래스가 들어가면 좋지
시작화면 및 설정화면"""
from constant import *
import sys
import pygame


# Rect를 빼고 모두다 좌표로 설정.

# 이미지 로드 및 크기 변경 함수 (사이즈, 좌표)
def img_load(screen, filename, size, pos):
    img = pygame.image.load(filename)
    img_trans = pygame.transform.scale(img, size)
    screen.blit(img_trans, pos)


# 텍스트 설정 -> 고치기
def draw_text(screen, text, pos, size, font="malgungothic"):
    Font = pygame.font.SysFont(font, size)
    text1 = Font.render(text,True,BLACK)
    screen.blit(text1, (pos))


"""설정화면"""


# 화면 설정 -> 사이즈마다 구현해야 함
def screen_size(size: int):
    pass

# 조작키 설정
def control_button_setting():
    pass


# 설정 초기화
def setting_init():
    pass


# 설정 저장
def setting_save():
    pass


# Slider 클래스 배경음, 효과음 조절
class Slider:

    def __init__(self, screen, length, pos, slider_range, main_color=BLACK, button_color=RED):

        self.drag = False  # 버튼을 드래그하기 위한 초기 변수
        self.offset_x = 0

        self.screen = screen
        self.length = length  # 슬라이더 크기
        self.x, self.y = pos  # 슬라이더 위치
        self.min, self.max = slider_range  # 슬라이더 값의 범위
        self.color1 = main_color  # 선 색
        self.color2 = button_color  # 버튼색

        self.button = pygame.rect.Rect(int(self.x + 18 / 40 * self.length), int(self.y - 1 / 40 * self.length),
                                  int(self.length * 1 / 20), int(self.length * 1 / 20))

        self.value = (self.max + self.min) / 2  # 값의 초기값
        self.button_rect = self.button
        
    def set_value(self, length, pos):
        self.length = length
        self.x, self.y = pos
        self.button.x = int(self.x + 18 / 40 * self.length)
        self.button.y = int(self.y - 1 / 40 * self.length)
        self.button.width =  int(self.length * 1 / 20)
        self.button.height =  int(self.length * 1 / 20)

    def draw(self):  # 선, 버튼을 스크린에 그림
        pygame.draw.line(self.screen, self.color1, (self.x, self.y), (self.x + self.length, self.y), 5)
        pygame.draw.rect(self.screen, self.color2, self.button_rect)

    def operate(self, Event):  # pygame 메인 루프에서 event를 받아 드래그 하기 위한 함수
        if Event.type == pygame.MOUSEBUTTONDOWN:
            if Event.button == 1:
                if self.button_rect.collidepoint(Event.pos):
                    self.drag = True

                    mouse_x, mouse_y = Event.pos
                    self.offset_x = self.button_rect.x - mouse_x

        elif Event.type == pygame.MOUSEBUTTONUP:
            if Event.button == 1:
                self.drag = False

        elif Event.type == pygame.MOUSEMOTION:
            if self.drag:
                mouse_x, mouse_y = Event.pos
                self.button_rect.x = mouse_x + self.offset_x
                if self.button_rect.x <= self.x:  # 드래그 제한
                    self.button_rect.x = self.x

                elif self.button_rect.x >= (self.x + self.length) - 1 / 10 * self.length:
                    self.button_rect.x = int((self.x + self.length) - 1 / 10 * self.length)

        self.value = self.max + (self.min - self.max) * (
                1 - (self.button_rect.x - self.x) / (9 / 10 * self.length))  # value 수정

    # value을 text로 출력 
    def draw_value(self, name, pos, color=BLACK, size=20):
        FONT = pygame.font.SysFont("malgungothic", size)
        text1 = FONT.render("{} : {}".format(name, int(self.value)), True, color)
        # text_rect = text1.get_rect()
        # text_rect.center = pos

        self.screen.blit(text1, pos)
        
    def get_value(self):
        return self.value

    # 버튼 클래스


# class Button:
#     def __init__(self, screen, x, y, width, height, text, font_size=30, font_name='malgungothic', color=WHITE,
#                  hover_color=GRAY, action=None):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.color = color
#         self.hover_color = hover_color
#         self.action = action
#         self.screen = screen

#         mouse = pygame.mouse.get_pos()
#         click = pygame.mouse.get_pressed()

#         if x + width > mouse[0] > x and y + height > mouse[1] > y:
#             # 마우스를 버튼위에 올렸을 때 색깔 변함
#             pygame.draw.rect(screen, self.hover_color, self.rect)
#             if click[0] == 1 and action != None:
#                 # 클릭하면 해당 버튼 기능 수행
#                 action()
#         else:
#             pygame.draw.rect(screen, self.color, self.rect)

#         # 버튼의 text 설정
#         font = pygame.font.SysFont(font_name, font_size)
#         self.text_surf = font.render(self.text, True, BLACK)
#         self.text_rect = self.text_surf.get_rect()
#         self.text_rect.center = ((x + width / 2), (y + height / 2))
#         screen.blit(self.text_surf, self.text_rect)
