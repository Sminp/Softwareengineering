import pygame
from constant import *
from UNO import RectInit


# 오 글씨 바꾸는 기능 있었으면 좋겠다
class TextRect(RectInit):
    def __init__(self, text_size, text_color):
        super().__init__()
        self.k_font = MALGUNGOTHIC
        self.e_font = BERLIN
        self.text_size = text_size
        self.text_color = text_color

    def text_rect(self, message):
        if message[0].isalpha():
            new_font = pygame.font.SysFont(self.e_font, self.text_size)
        else:
            new_font = pygame.font.SysFont(self.k_font, self.text_size)
        new_text = new_font.render(message, True, self.text_color)
        return new_text

    def show(self):
        pass


# Rect를 빼고 모두다 좌표로 설정.
# 버튼 클래스 안에 하이라이트 그림 넣으면 안되려나? - 넣어야 함.
# 버튼 클래스
class Button(RectInit):
    def __init__(self, x, y, img, width, height):
        super().__init__()
        # self.rect = pygame.Rect(x,y, 30, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = (x, y)
        self.highlighted = False

        self.img = pygame.transform.scale(pygame.image.load(resource_path(img)), [width, height])
        self.rect = self.img.get_rect()
        self.rect.center = (self.x + self.width / 2), (self.y + self.height / 2)

    def show(self):
        self.screen.blit(self.img, (self.x, self.y))

    def highlight(self):
        self.screen.blit(self.img, (self.x, self.y - 10))

    def get_rect(self):
        return self.rect


# Slider 클래스 배경음, 효과음 조절
class Slider(RectInit):
    def __init__(self, length, pos, slider_range, main_color=BLACK, button_color=RED):
        super().__init__()
        self.drag = False  # 버튼을 드래그하기 위한 초기 변수
        self.offset_x = 0

        self.length = length  # 슬라이더 크기
        self.x, self.y = pos  # 슬라이더 위치
        self.min, self.max = slider_range  # 슬라이더 값의 범위
        self.color1 = main_color  # 선 색
        self.color2 = button_color  # 버튼색
        self.size = 20

        self.button = pygame.rect.Rect(int(self.x + 18 / 40 * self.length), int(self.y - 1 / 40 * self.length),
                                       int(self.length * 1 / 20), int(self.length * 1 / 20))

        self.value = (self.max + self.min) / 2  # 값의 초기값
        self.button_rect = self.button

    def set_value(self, length, pos):
        self.length = length
        self.x, self.y = pos
        self.button.x = int(self.x + 18 / 40 * self.length)
        self.button.y = int(self.y - 1 / 40 * self.length)
        self.button.width = int(self.length * 1 / 20)
        self.button.height = int(self.length * 1 / 20)

    def draw(self):  # 선, 버튼을 스크린에 그림
        pygame.draw.line(self.screen, self.color1, (self.x, self.y), (self.x + self.length, self.y), 5)
        pygame.draw.rect(self.screen, self.color2, self.button_rect)

    def operate(self, event):  # pygame 메인 루프에서 event를 받아 드래그 하기 위한 함수
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    self.drag = True

                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.button_rect.x - mouse_x

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False

        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                mouse_x, mouse_y = event.pos
                self.button_rect.x = mouse_x + self.offset_x
                if self.button_rect.x <= self.x:  # 드래그 제한
                    self.button_rect.x = self.x

                elif self.button_rect.x >= (self.x + self.length) - 1 / 10 * self.length:
                    self.button_rect.x = int((self.x + self.length) - 1 / 10 * self.length)

        self.value = self.max + (self.min - self.max) * (
                1 - (self.button_rect.x - self.x) / (9 / 10 * self.length))  # value 수정

    # value을 text로 출력
    def draw_value(self, name, pos, color=BLACK):
        FONT = pygame.font.SysFont("malgungothic", self.size)
        text1 = FONT.render("{} : {}".format(name, int(self.value)), True, color)
        # text_rect = text1.get_rect()
        # text_rect.center = pos

        self.screen.blit(text1, pos)
