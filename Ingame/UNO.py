import pygame
import sys
from pygame.locals import *
import os
from datetime import datetime
import socket
import threading
import constant as c
import game_functions as gf
import settings as s
import client as cl
import network as net
import server as sv
import rect_functions as rf
from loadcard import *
import time

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)


img_basic_address = './image/'


# 지울 예정
# 텍스트 구현
def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.SysFont(text_font, text_size)
    new_text = new_font.render(
        message, True, text_color)
    return new_text


# 끝내는 함수
def terminate():
    pygame.quit()
    sys.exit()


class UNOGame:
    """UNOGame 화면"""

    def __init__(self):
        pygame.init()
        self.settings = s.Settings().get_setting()
        self.setting = s.Settings()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = (self.settings['screen'])
        # self.screen.fill(self.settings.bg_color)
        pygame.display.set_caption("UNO!")
        pygame.display.update()
        # self.keysetting = 1
        # self.menu = True

        self.key_setting_text = rf.TextRect(
            self.screen, "KEY SETTING", 35, c.WHITE)

        self.keys = self.settings['keys']
        self.up_text = rf.TextRect(self.screen, "UP", 30, c.BLACK)
        self.down_text = rf.TextRect(self.screen, "DOWN", 30, c.BLACK)
        self.left_text = rf.TextRect(self.screen, "LEFT", 30, c.BLACK)
        self.right_text = rf.TextRect(self.screen, "RIGHT", 30, c.BLACK)
        self.click_text = rf.TextRect(self.screen, "CLICK", 30, c.BLACK)

        self.move_up_text = rf.TextRect(
            self.screen, pygame.key.name(self.keys["up"]), 30, c.BLACK)
        self.move_down_text = rf.TextRect(
            self.screen, pygame.key.name(self.keys["down"]), 30, c.BLACK)
        self.move_left_text = rf.TextRect(
            self.screen, pygame.key.name(self.keys["left"]), 30, c.BLACK)
        self.move_right_text = rf.TextRect(
            self.screen, pygame.key.name(self.keys["right"]), 30, c.BLACK)
        self.move_click_text = rf.TextRect(
            self.screen, pygame.key.name(self.keys["click"]), 30, c.BLACK)

    def bg_img_load(self, filename: str) -> object:
        bg_img = pygame.image.load(s.resource_path(filename))
        bg_img = pygame.transform.scale(bg_img,
                                        (self.settings['screen']))
        return self.screen.blit(bg_img, (0, 0))

    def object_init(self):
        pass

    def object_show(self):
        pass

    def sound(self):
        pass

    def handle_event(self, key_name):
        """조작키 속성값 설정"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.keys[key_name] = event.key

    def menu(self):
        pass

    # 설정 클래스로 이동
    def key_select_screen(self):
        key_select = True
        self.bg_img_load("./image/setting_image/settingbackground.jpg")
        close_button = rf.Button(self.screen, self.settings['screen'][0] * (5 / 6), self.settings['screen'][1] * (3 / 11),
                                 c.SETTING_CLOSE_BUTTON, 20, 20)
        save_button = rf.Button(self.screen, self.settings['screen'][0] * (8 / 11), self.settings['screen'][1] * (6 / 8),
                                c.SETTING_SAVE_BUTTON, 100, 50)

        pygame.draw.rect(self.screen, c.WHITE, (
            self.settings['screen'][0] *
            (1 / 9), self.settings['screen'][1] * (2 / 8),
            self.settings['screen'][0] * (7 / 9),
            self.settings['screen'][1] * (6 / 10)))

        while key_select:

            self.up_text.show(
                (self.settings['screen'][0] * (2 / 5), self.settings['screen'][1] * (6 / 18)))
            self.down_text.show(
                (self.settings['screen'][0] * (2 / 5), self.settings['screen'][1] * (8 / 18)))
            self.left_text.show(
                (self.settings['screen'][0] * (2 / 5), self.settings['screen'][1] * (10 / 18)))
            self.right_text.show(
                (self.settings['screen'][0] * (2 / 5), self.settings['screen'][1] * (12 / 18)))
            self.click_text.show(
                (self.settings['screen'][0] * (2 / 5), self.settings['screen'][1] * (14 / 18)))

            self.key_setting_text.show(
                (self.settings['screen'][0] * (1 / 4), self.settings['screen'][1] * (1 / 6)))
            self.move_up_text.show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (6 / 18)))
            self.move_down_text.show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (8 / 18)))
            self.move_left_text.show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (10 / 18)))
            self.move_right_text.show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (12 / 18)))
            self.move_click_text.show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (14 / 18)))

            close_button.show()
            save_button.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.move_up_text.rect.collidepoint(event.pos):
                        key_change = True
                        while key_change:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                                # print(key)
                                self.keys["up"] = key
                                # print(self.keys)
                                pygame.draw.rect(
                                    self.screen, c.WHITE, self.move_up_text.rect)
                                self.move_up_text.change_text_surface(
                                    pygame.key.name(self.keys["up"]))
                                key_change = False

                    elif self.move_down_text.rect.collidepoint(event.pos):
                        key_change = True
                        while key_change:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                                # print(key)
                                self.keys["down"] = key
                                # print(self.keys)
                                pygame.draw.rect(
                                    self.screen, c.WHITE, self.move_down_text.rect)
                                self.move_down_text.change_text_surface(
                                    pygame.key.name(self.keys["down"]))
                                key_change = False

                    elif self.move_left_text.rect.collidepoint(event.pos):
                        key_change = True
                        while key_change:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                                # print(key)
                                self.keys["left"] = key
                                # print(self.keys)
                                pygame.draw.rect(
                                    self.screen, c.WHITE, self.move_left_text.rect)
                                self.move_left_text.change_text_surface(
                                    pygame.key.name(self.keys["left"]))
                                key_change = False

                    elif self.move_right_text.rect.collidepoint(event.pos):
                        key_change = True
                        while key_change:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                                # print(key)
                                self.keys["right"] = key
                                # print(self.keys)
                                pygame.draw.rect(
                                    self.screen, c.WHITE, self.move_right_text.rect)
                                self.move_right_text.change_text_surface(
                                    pygame.key.name(self.keys["right"]))
                                key_change = False

                    elif self.move_click_text.rect.collidepoint(event.pos):
                        key_change = True
                        while key_change:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                                # print(key)
                                self.keys["click"] = key
                                # print(self.keys)
                                pygame.draw.rect(
                                    self.screen, c.WHITE, self.move_click_text.rect)
                                self.move_click_text.change_text_surface(
                                    pygame.key.name(self.keys["click"]))
                                key_change = False

                    elif close_button.get_rect().collidepoint(event.pos):
                        # key_select = False
                        setting = SettingScreen()
                        setting.menu()

                    elif save_button.get_rect().collidepoint(event.pos):
                        self.setting.change_setting(self.settings)

            pygame.display.update()


class TitleMenu(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])

        # 버튼 속성
        self.x = self.settings['screen'][0] * (1 / 5)
        self.y = self.settings['screen'][1] * (9 / 13)
        self.width = self.settings['screen'][0] * (1 / 10)
        self.height = self.settings['screen'][1] * (4 / 13)
        self.button_li = self.object_init()

        self.selected = 0

    def object_init(self):
        i = 0
        button_li = []
        for button in c.TITLE_MENU_BUTTONS:
            button = rf.Button(self.screen, self.x + self.width * i,
                               self.y, button, self.width, self.height)
            button_li.append(button)
            i += 1
        return button_li

    def object_show(self, *button_li):
        for button in button_li:
            button.show()

    # 수정중
    def sound(self):
        pygame.mixer.music.load(c.TITLE_BGM)
        pygame.mixer.music.play(-1)

    # keysetting 하이라이트 따로 변수 만들어서 저장.
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == self.keys["left"]:
                    # sound.play()
                    if self.selected <= 0:
                        self.selected = 0
                    else:
                        self.selected = self.selected - 1

                elif event.key == self.keys["right"]:
                    if self.selected >= 5:
                        self.selected = 5
                    else:
                        self.selected = self.selected + 1
                elif event.key == self.keys["click"]:
                    if self.selected == 0:
                        LobbyScreen().menu()
                    elif self.selected == 1:
                        SelectRole().menu()
                    elif self.selected == 2:
                        StoryMode().menu()
                    elif self.selected == 3:
                        AchievementScreen().menu()
                    elif self.selected == 4:
                        SettingScreen().menu()
                    else:
                        terminate()

            if event.type == pygame.MOUSEBUTTONUP:
                select_sound = pygame.mixer.Sound(c.SELECT_BGM)
                select_sound.play()
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    LobbyScreen().menu()
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    SelectRole().menu()
                elif self.button_li[2].get_rect().collidepoint(event.pos):
                    StoryMode().menu()
                elif self.button_li[3].get_rect().collidepoint(event.pos):
                    AchievementScreen().menu()
                elif self.button_li[4].get_rect().collidepoint(event.pos):
                    SettingScreen().menu()
                elif self.button_li[5].get_rect().collidepoint(event.pos):
                    terminate()

        # 버튼 크기 조정
        for i, button in enumerate(self.button_li):
            if i == self.selected:
                button.highlight()  # 선택된 메뉴 크기 조정
            else:
                button.show()  # 나머지 메뉴 그리기

    def menu(self):
        self.sound()

        while True:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            self.bg_img_load(c.TITLE_BACKGROUND)
            self.object_show(*self.button_li)
            self.handle_event()
            pygame.display.update()


class LobbyScreen(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        # 버튼 속성
        self.x = self.settings['screen'][0] * (3 / 7)
        self.y = self.settings['screen'][0] * (1 / 6)
        self.width = self.settings['screen'][0] * (1 / 3)
        self.height = self.settings['screen'][1] * (1 / 4)
        self.font = pygame.font.SysFont(self.settings['font'], 30)
        self.user_name = "player"
        self.button, self.computer_rect = self.object_init()
        self.user_name_text = rf.TextRect(
            self.screen, self.user_name, 30, c.BLACK)
        self.input_active = False
        self.play_with_a = False

    def object_init(self):
        button = rf.Button(self.screen, self.x, self.y,
                           c.GAMESTART_BUTTON, self.width, self.height)

        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.settings['screen'][1] - 500) / 6),
                               self.settings['screen'][0] / 5, self.settings['screen'][1] / 6)
            if i == 0:
                label = "com 1"
            else:
                label = "add"
            computer_rect.append([rect, label])

        return button, computer_rect

    def object_show(self):
        self.button.show()

        self.user_name_text.show(
            (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (2 / 3)))

        for rect, label in self.computer_rect:
            pygame.draw.rect(self.screen, c.WHITE, rect)
            label_surface = self.font.render(label, True, c.BLACK)
            self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

        # 이름 수정할 때 커서 표시
        if self.input_active:
            pygame.draw.line(self.screen, c.BLACK,
                             (self.user_name_text.rect.x +
                              self.user_name_text.rect.w, self.user_name_text.rect.y),
                             (self.user_name_text.rect.x + self.user_name_text.rect.w,
                              self.user_name_text.rect.y + self.user_name_text.rect.h), 2)

    def sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(c.PLAYING_BGM)
        pygame.mixer.music.play(-1)

    # 버튼 누르는 이벤트 처리 , 창 닫는 이벤트 처리
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.user_name_text.rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False

                if self.button.get_rect().collidepoint(event.pos):
                    result = 1
                    for rect, text in self.computer_rect:
                        if text.split(' ')[0] == 'comA':
                            self.play_with_a = True
                        if text != "add":
                            result += 1
                    if self.play_with_a:
                        player_list = []
                        player_list.append(self.user_name)
                        for i in range(len(self.computer_rect)):
                            if self.computer_rect[i][1] != 'add':
                                player_list.append(self.computer_rect[i][1])
                        uno_ = gf.GameWithA(
                            user_name=self.user_name, player_list=player_list)
                        uno_.startgame()
                    else:
                        uno_ = gf.Game(result, user_name=self.user_name)
                        uno_.startgame()

                for i in range(len(self.computer_rect)):
                    if i == 0:
                        continue
                    else:
                        if self.computer_rect[i][0].collidepoint(event.pos):
                            if self.computer_rect[i][1] == "add" and self.computer_rect[i - 1][1] != "add":
                                ask_popup = YesNo('스토리 A 플레이어를 추가하시겠습니까?')
                                ask_popup.menu()
                                if ask_popup.y == True:
                                    self.computer_rect[i][1] = "comA {}".format(
                                        i + 1)
                                else:
                                    self.computer_rect[i][1] = "com {}".format(
                                        i + 1)
                            else:
                                if i == 4:
                                    self.computer_rect[i][1] = "add"
                                else:
                                    if self.computer_rect[i + 1][1] == "add":
                                        self.computer_rect[i][1] = "add"

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        self.user_name += event.unicode
                    self.user_name_text.change_text_surface(self.user_name)

    def menu(self):
        self.sound()

        self.input_active = False

        while True:
            self.bg_img_load(c.GAME_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()


class SettingScreen(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.settings = s.Settings().get_setting()
        self.setting = s.Settings()

        self.button_li, self.slider_li, self.rect = self.object_init()
        self.setting_text = rf.TextRect(self.screen, "SETTING", 35, c.WHITE)
        self.screen_setting_text = rf.TextRect(
            self.screen, "화면 크기", 20, c.BLACK)
        self.volume = 0.0

        self.selected = 0
        self.current_slider = 0

    def object_init(self):
        i = 3
        button_li = []
        for button in c.SIZE_BUTTONS:
            button = rf.Button(self.screen, self.settings['screen'][0] * (i / 10), self.settings['screen'][1] * (1 / 2),
                               button, 100, 50)
            button_li.append(button)
            i += 2

        # self.settings['screen'][0] 이렇게 접근하는 거 너무 길지 않나?
        close_button = rf.Button(self.screen, self.settings['screen'][0] * (
            5 / 6), self.settings['screen'][1] * (3 / 11), c.SETTING_CLOSE_BUTTON, 20, 20)
        key_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 8), self.settings['screen'][1] * (7 / 11), c.SETTING_KEY_BUTTON, 100, 50)
        init_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 8), self.settings['screen'][1] * (6 / 8), c.SETTING_INIT_BUTTON, 100, 50)
        save_button = rf.Button(self.screen, self.settings['screen'][0] * (
            8 / 11), self.settings['screen'][1] * (6 / 8), c.SETTING_SAVE_BUTTON, 100, 50)
        settingcolor_button = rf.Button(self.screen, self.settings['screen'][0] * (
            8 / 11), self.settings['screen'][1] * (7 / 11), c.SETTING_RECT, 100, 50)
        buttons = [close_button, key_button, init_button,
                   save_button, settingcolor_button]

        for button in buttons:
            button_li.append(button)

        j = 6
        sliders_li = []
        for text in c.SLIDER_TEXT:
            slider = rf.Slider(self.screen, text, self.settings['screen'][0] / 2, (self.settings['screen'][0] * (
                3 / 10), self.settings['screen'][1] * (j / 20)), (0, 100))
            sliders_li.append(slider)
            j += 1.5

        if self.settings['setting_color'] == True:
            rect = pygame.Rect(
                self.settings['screen'][0] * (8 / 11)+50, self.settings['screen'][1] * (7 / 11), 50, 50)
        elif self.settings['setting_color'] == False:
            rect = pygame.Rect(
                self.settings['screen'][0] * (8 / 11), self.settings['screen'][1] * (7 / 11), 50, 50)

        return button_li, sliders_li, rect

    def object_show(self):
        pygame.draw.rect(self.screen, c.WHITE, (
            self.settings['screen'][0] * (1 / 9), self.settings['screen'][1] * (
                2 / 8), self.settings['screen'][0] * (7 / 9),
            self.settings['screen'][1] * (6 / 10)))

        self.setting_text.show(
            (self.settings['screen'][0] * (1 / 5), self.settings['screen'][1] * (1 / 6)))
        self.screen_setting_text.show(
            (self.settings['screen'][0] * (1 / 5), self.settings['screen'][1] * (6 / 11)))

        for button in self.button_li:
            button.show()

        i = 6
        for slider in self.slider_li:
            slider.show()
            slider.show_value(
                (self.settings['screen'][0] * (1 / 5), self.settings['screen'][1] * (i / 20)))
            i += 1.5

        pygame.draw.rect(self.screen, c.BLACK, self.rect)

        pygame.display.update()

    def sound(self):
        pass

    def calculate_volume(self):
        # 슬라이더 값을 기반으로 음량을 계산
        total_value = 0
        for slider in self.slider_li:
            total_value += slider.value
        average_value = total_value / len(self.slider_li)
        if average_value == 0:
            volume = 0  # 음량을 0으로 설정
        else:
            volume_percentage = average_value / 100  # 음량의 비율 계산
            volume = volume_percentage * 1  # 최대 음량 설정

        return volume

    def set_volume(self):
        volume = self.calculate_volume()
        pygame.mixer.music.set_volume(volume)

    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            for slider in self.slider_li:
                slider.mouse_operate(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.volume = self.calculate_volume()
                    self.set_volume()

            # 키보드 버튼
            if event.type == pygame.KEYDOWN:
                if event.key == self.keys["left"]:
                    # sound.play()
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == self.keys["right"]:
                    # sound.play()
                    if selected >= 3:
                        selected = 3
                    else:
                        selected = selected + 1
                if event.key == self.keys["click"]:
                    if selected <= 1:
                        # 버튼 입력 후 시작 함수 실행 - 해결하면 지우기
                        pass
                    if selected == 2:
                        # 버튼 입력 후 설정 함수 실행 - 해결하면 지우기
                        pass
                    if selected >= 3:
                        # 버튼 입력 후 시작 함수 실행 - 해결하면 지우기
                        pass

            if event.type == pygame.MOUSEBUTTONUP:
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    self.settings['fullscreen'] = pygame.FULLSCREEN
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    # 테스트 할려고 화면 크기 임시로 정함 -> 나중에 수정
                    self.settings['screen'][0] = 1280
                    self.settings['screen'][1] = 720
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                    self.button_li, self.slider_li, self.rect = self.object_init()

                elif self.button_li[2].get_rect().collidepoint(event.pos):
                    # 테스트 할려고 화면 크기 임시로 정함 -> 나중에 수정
                    self.settings['screen'][0] = 800
                    self.settings['screen'][1] = 600
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                    self.button_li, self.slider_li, self.rect = self.object_init()

                elif self.button_li[3].get_rect().collidepoint(event.pos):
                    title = TitleMenu()
                    title.menu()

                elif self.button_li[4].get_rect().collidepoint(event.pos):
                    key_select = UNOGame()
                    key_select.key_select_screen()  # 키보드 설정 함수 실행
                elif self.button_li[5].get_rect().collidepoint(event.pos):
                    # 방법 1
                    # self.settings = { 'screen' : [800,600] , 'font' : MALGUNGOTHIC,
                    #                 'keys': {
                    #                     "left": pygame.K_LEFT,
                    #                     "right": pygame.K_RIGHT,
                    #                     "up": pygame.K_UP,
                    #                     "down": pygame.K_DOWN,
                    #                     "click": pygame.K_KP_ENTER
                    #                 },
                    #                 'sound' : {
                    #                     "total" : 1,
                    #                     "background" : 1,
                    #                     "effect" : 1
                    #                 }
                    #                 , 'setting_color' : False
                    #             }
                    # self.screen = pygame.display.set_mode((self.settings['screen']), flags = self.settings['fullscreen'])
                    # self.button_li, self.slider_li, self.rect = self.object_init()
                    # self.setting.set_setting(self.settings)
                    # 방법 2 => 이걸로 하면 설정 초기화가 바로 보이지는 않음. 다시 메뉴로 돌아가야 보임 -> 선택해주세욤
                    self.setting.init_setting()
                elif self.button_li[6].get_rect().collidepoint(event.pos):
                    self.setting.change_setting(self.settings)  # 현재 값을 파일에 저장

                elif self.rect.collidepoint(event.pos):
                    if self.rect.x == int(self.settings['screen'][0] * (8 / 11)):
                        self.rect.x += 50
                        self.settings['setting_color'] = True
                    elif self.rect.x == int(self.settings['screen'][0] * (8 / 11)) + 50:
                        self.rect.x -= 50
                        self.settings['setting_color'] = False

        for i, button in enumerate(self.button_li):
            if i == self.selected:
                button.highlight()  # 선택된 메뉴 크기 조정

    def menu(self):
        selected = 1

        while True:
            self.bg_img_load(c.SETTING_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()


class StoryMode(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.width = self.settings['screen'][0] * (1 / 5)
        self.height = self.settings['screen'][1] * (1 / 5)
        self.storywin = [self.settings['achievement']['storya_win'], self.settings['achievement']['storyb_win'],
                         self.settings['achievement']['storyc_win'], self.settings['achievement']['storyd_win']]
        self.button_li, self.text = self.object_init()

        self.selected = 0

    def object_init(self):
        i = 1
        j = 0
        button_li = []
        for button in c.STORYMODE_MENU_BUTTONS:
            if j == 0:
                button = rf.Button(self.screen, self.settings['screen'][0] * (i / 40), self.settings['screen'][1] * (2 / 5),
                                   button,
                                   self.width, self.height)
                button.lock = False
            else:
                if self.storywin[j-1] == False:
                    button = rf.Button(self.screen, self.settings['screen'][0] * (i / 40), self.settings['screen'][1] * (2 / 5),
                                       button[1],
                                       self.width, self.height)
                    button.lock = True
                else:
                    print(button[0])
                    button = rf.Button(self.screen, self.settings['screen'][0] * (i / 40), self.settings['screen'][1] * (2 / 5),
                                       button[0],
                                       self.width, self.height)
                    button.lock = False

            button_li.append(button)
            j += 1
            i += 10 if i != 1 else i * 10

        text = rf.TextRect(self.screen, "STORY MODE", 50, c.WHITE)
        return button_li, text

    def object_show(self):
        for button in self.button_li:
            button.show()
        self.text.show(
            (self.settings['screen'][0] // 5, self.settings['screen'][1] // 10))

        for i, button in enumerate(self.button_li):
            if i == self.selected:
                button.highlight()  # 선택된 메뉴 크기 조정
            else:
                button.show()

    def sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(c.STOTYMODE_BGM)
        pygame.mixer.music.play(-1)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.button_li)):
                    if self.button_li[i].get_rect().collidepoint(event.pos):
                        if self.button_li[i].lock == False:
                            if i == 0:
                                ask_popup = YesNoStory(2, 2, gf.GameA)
                                ask_popup.menu()
                            elif i == 1:
                                ask_popup = YesNoStory(4, 3, gf.GameB)
                                ask_popup.menu()
                            elif i == 2:
                                ask_popup = YesNoStory(3, 4, gf.GameC)
                                ask_popup.menu()
                            else:
                                ask_popup = YesNoStory(3, 5, gf.GameD)
                                ask_popup.menu()

            if event.type == pygame.KEYDOWN:
                if event.key == self.keys["left"]:
                    if self.selected <= 0:
                        self.selected = 0
                    else:
                        self.selected = self.selected - 1
                elif event.key == self.keys["right"]:
                    if self.selected >= 3:
                        self.selected = 3
                    else:
                        self.selected = self.selected + 1
                elif event.key == self.keys["click"]:
                    if self.button_li[self.selected].lock == False:
                        if self.selected == 0:
                            ask_popup = YesNoStory(2, 2, gf.GameA)
                            ask_popup.menu()
                        elif self.selected == 1:
                            ask_popup = YesNoStory(4, 3, gf.GameB)
                            ask_popup.menu()
                        elif self.selected == 2:
                            ask_popup = YesNoStory(3, 4, gf.GameC)
                            ask_popup.menu()
                        elif self.selected == 3:
                            ask_popup = YesNoStory(3, 5, gf.GameD)
                            ask_popup.menu()

    def menu(self):
        self.sound()

        while True:
            self.bg_img_load(c.MAP_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()


class UnoGame(UNOGame):
    def __init__(self):
        super().__init__()
        pass

    def object_init(self):
        pass

    def object_show(self):
        pass

    def sound(self):
        pass

    def handle_event(self):
        pass

    def menu(self):
        pass


class YesNo(UnoGame):
    def __init__(self, ask_text):
        super().__init__()
        self.yes_no = True
        self.ask_text = ask_text
        self.width = self.settings['screen'][0] * (3 / 7)
        self.height = self.settings['screen'][1] * (3 / 5)
        self.button_li, self.text = self.object_init()
        self.y = False

    def object_init(self):
        i = 0
        button_li = []
        for button in c.YESNO_BUTTONS:
            button = rf.Button(self.screen, self.width,
                               self.height + i, button, 100, 50)
            button_li.append(button)
            i += 70
        text = rf.TextRect(self.screen, self.ask_text, 20, c.BLACK)
        return button_li, text

    def object_show(self):
        pygame.draw.rect(self.screen, c.WHITE, (
            self.settings['screen'][0] / 2 - 200, self.settings['screen'][1] / 3 - 100, 400, 400))
        for button in self.button_li:
            button.show()
        self.text.show(
            (self.settings['screen'][0] / 2, self.settings['screen'][1] / 4))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    self.y = True
                    self.yes_no = False
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    self.y = False
                    self.yes_no = False

    def menu(self):
        while self.yes_no:
            self.object_show()
            self.handle_event()

            pygame.display.update()


class YesNoStory(YesNo):
    def __init__(self, player_num, difficulty, class_name):
        if difficulty == 2:
            self.info = ["A 지역을 선택하시겠습니까?", "첫 분배시 컴퓨터에게 기술 카드를",
                         "50% 더 높은 확률로 지급합니다.", "컴퓨터 플레이어가 콤보를 사용합니다.", "인원수 : 2"]
        elif difficulty == 3:
            self.info = ["B 지역을 선택하시겠습니까?", "첫 카드를 제외하고 모든 카드를 같은 ",
                         "수만큼 모든 플레이어들에게 분배합니다.", "인원수 : 4"]
        elif difficulty == 4:
            self.info = ["C 지역을 선택하시겠습니까?", "매 5턴마다 낼 수 있는 카드의",
                         "색상이 무작위로 변경됩니다.", "인원수 : 3"]
        else:
            self.info = ["D 지역을 선택하시겠습니까?", "현재 카드의 배수나 약수의 값을 ",
                         "가지는 카드만 낼 수 있습니다.", "인원수 : 3"]
        super().__init__(self.info[0])
        self.player_num = player_num
        self.difficulty = difficulty
        self.class_name = class_name

        self.info_list = []
        for i in range(1, len(self.info)):
            self.info_list.append(rf.TextRect(
                self.screen, self.info[i], 20, c.BLACK))

        self.selected = 0

    def object_show(self):
        super().object_show()
        for i in range(len(self.info_list)):
            self.info_list[i].show(
                (self.settings['screen'][0] / 2, self.settings['screen'][1] / 3 + 40 * i))

        for i, button in enumerate(self.button_li):
            if i == self.selected:
                button.highlight()  # 선택된 메뉴 크기 조정
            else:
                button.show()  # 나머지 메뉴 그리기

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    uno = self.class_name()
                    uno.startgame()
                    self.yes_no = False
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    self.yes_no = False

            if event.type == pygame.KEYDOWN:
                if event.key == self.keys["up"]:
                    # sound.play()
                    if self.selected <= 0:
                        self.selected = 0
                    else:
                        self.selected = self.selected - 1

                elif event.key == self.keys["down"]:
                    if self.selected >= 1:
                        self.selected = 1
                    else:
                        self.selected = self.selected + 1
                elif event.key == self.keys["click"]:
                    if self.selected == 0:
                        uno = self.class_name()
                        uno.startgame()
                        self.yes_no = False
                    elif self.selected == 1:
                        self.yes_no = False

    def menu(self):
        while self.yes_no:
            self.object_show()
            self.handle_event()

            pygame.display.update()


class SelectRole(UnoGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.text, self.button_li = self.object_init()

    def object_init(self):
        text = rf.TextRect(self.screen, "멀티 플레이어", 50, c.BLACK)
        button = []
        server_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 5), self.settings['screen'][1] * (2 / 5), c.MAKEROOM_BUTTON, 200, 100)
        client_button = rf.Button(self.screen, self.settings['screen'][0] * (
            3 / 5), self.settings['screen'][1] * (2 / 5), c.ROOMENTER_BUTTON, 200, 100)
        button.append(server_button)
        button.append(client_button)

        return text, button

    def object_show(self):
        self.text.show(
            (self.settings['screen'][0] * (1 / 2), self.settings['screen'][1] * (1 / 5)))
        for button in self.button_li:
            button.show()

    def sound(self):
        pass

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == gf.QUIT:
                pygame.quit()
                return

            # 버튼 클릭 이벤트 처리
            elif event.type == gf.MOUSEBUTTONDOWN:
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    ServerScreen().menu()
                    # 비번 설정, 로비화면으로 넘어감
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    ClientScreen().menu()
                    pass  # 접속할 게임의 IP주소를 입력하는 창으로 넘어감

    def menu(self):
        while True:
            self.screen.fill(c.WHITE)
            self.object_show()
            self.handle_event()

            pygame.display.update()


class ClientScreen(UnoGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.password = ''
        self.ipaddress = ''
        self.username = ''

    def menu(self):
        self.set_ipaddress()
        self.set_password()
        self.set_username()
        print(self.ipaddress, self.password, self.username)
        client = cl.Client(self.screen, self.password,
                           self.username, self.ipaddress)
        # client.connect()
        client.lobby()
        # 로비에 접속하는 코드

    def set_ipaddress(self):
        get_input_screen = GetInput("IP주소를 입력하세요", self.ipaddress, SelectRole)
        get_input_screen.run()
        self.ipaddress = get_input_screen.input
        localhost = socket.gethostbyname(socket.gethostname())
        if self.ipaddress != localhost:
            self.show_error_msg(c.IP_FALSE_MSG)
            self.set_ipaddress()

    def set_password(self):
        get_input_screen = GetInput("비밀번호를 입력하세요", self.password, ClientScreen)
        get_input_screen.run()
        self.password = get_input_screen.input

    def set_username(self):
        get_input_screen = GetInput(
            "사용자 이름을 입력하세요", self.username, ClientScreen)
        get_input_screen.run()
        self.username = get_input_screen.input

    def show_error_msg(self, image_path):
        image = pygame.transform.scale(pygame.image.load(resource_path(image_path)), [
                                       self.settings['screen'][0] / 2, self.settings['screen'][1] / 2])
        rect = image.get_rect()
        rect.center = (self.settings['screen'][0] / 2,
                       self.settings['screen'][1] / 2)
        self.screen.blit(image, rect)
        pygame.display.update()
        time.sleep(2)
        self.screen.fill(c.WHITE)
        pygame.display.update()


class ServerScreen(UnoGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.password = ''

    def object_init(self):
        pass

    def object_show(self):
        pass

    def sound(self):
        pass

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

    def menu(self):
        self.set_password()
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
        # 로비화면으로 전환
        localhost = socket.gethostbyname(socket.gethostname())
        client = cl.Client(self.screen, self.password, 'player1', localhost)
        client.lobby()

    def run_server(self):
        # 서버를 생성합니다.
        localhost = socket.gethostbyname(socket.gethostname())
        port = 10000
        server = sv.Server(localhost, self.password)
        # 서버를 실행합니다.
        server.run()

    def set_password(self):
        get_input_screen = GetInput("비밀번호 설정", self.password, SelectRole)
        get_input_screen.run()
        self.password = get_input_screen.input


class GetInput(UnoGame):
    """
    password, ipaddress, user_name등을 입력받는 화면
    """

    def __init__(self, text, input, class_name):
        super().__init__()
        self.input_box = pygame.Rect(0, 0, 220, 32)
        self.input_box.center = (
            self.settings['screen'][0] * (1 / 2), self.settings['screen'][1] * (1 / 2))
        self.color_inactive = c.BLACK
        self.color_active = c.RED
        self.color = self.color_inactive
        self.text = rf.TextRect(self.screen, text, 50, c.BLACK)
        self.input = input
        self.input_text = rf.TextRect(self.screen, self.input, 30, c.BLACK)
        self.yes_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 4), self.settings['screen'][1] * (3 / 4), c.YES_BUTTON, 100, 50)
        self.no_button = rf.Button(self.screen, self.settings['screen'][0] * (
            3 / 4), self.settings['screen'][1] * (3 / 4), c.NO_BUTTON, 100, 50)
        self.active = False
        self.done = False
        self.clock = pygame.time.Clock()
        self.class_name = class_name

    def object_show(self):
        self.text.show(
            (self.settings['screen'][0] * (1 / 2), self.settings['screen'][1] * (1 / 3)))
        self.yes_button.show()
        self.no_button.show()

        self.input_text.show(self.input_box.center)
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

        if self.input_text.text_surface().get_width() >= 220:
            self.input_box.w = self.input_text.text_surface().get_width()+10
            self.input_box.center = (
                self.settings['screen'][0] * (1 / 2), self.settings['screen'][1] * (1 / 2))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.input_box.collidepoint(mouse_pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
                if self.yes_button.get_rect().collidepoint(mouse_pos):
                    self.done = True
                elif self.no_button.get_rect().collidepoint(mouse_pos):
                    self.class_name().menu()

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
                    else:
                        self.input += event.unicode
                    self.input_text.change_text_surface(self.input)
                    self.color = self.color_active if self.active else self.color_inactive

    def run(self):
        while not self.done:
            self.screen.fill(c.WHITE)
            self.object_show()
            self.handle_event()
            pygame.display.update()


class AchievementScreen(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.setting = s.Settings()

        self.achv_text = rf.TextRect(self.screen, "업적", 35, c.WHITE)

        self.x = self.settings['screen'][0] * (1 / 8)
        self.y = self.settings['screen'][1] * (1 / 5)
        self.width = self.settings['screen'][0] * (6 / 8)
        self.height = self.settings['screen'][1] * (1 / 6)
        self.achievement_li, self.close_button = self.object_init()

        self.achv_completed_img = pygame.transform.scale(pygame.image.load(c.ACHV_COMPLETED),
                                                         (self.settings['screen'][0]*(1/9), self.settings['screen'][1]*(1/9)))
        self.achv_completed_rect = self.achv_completed_img.get_rect()

    def object_init(self):
        close_button = rf.Button(self.screen, self.settings['screen'][0] * (7 / 8), self.settings['screen'][1] * (1 / 7),
                                 c.SETTING_CLOSE_BUTTON, 20, 20)

        i = 1
        achievement_li = []
        for achievement in c.ACHV_LIST:
            achievement = rf.Button(self.screen, self.x, self.y * i,
                                    achievement, self.width, self.height)
            achievement_li.append(achievement)
            i += 1

        return achievement_li, close_button

    def object_show(self):
        self.achv_text.show(
            (self.settings['screen'][0] * (1 / 5), self.settings['screen'][1] * (1 / 7)))
        self.close_button.show()

        for achievement in self.achievement_li:
            achievement.show()

        font = pygame.font.SysFont(c.MALGUNGOTHIC, 20)
        if self.settings['achievement']['single_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[0].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            single_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['single_win']", 20, c.WHITE)
            single_win_date_rect.x = self.achievement_li[0].midright
            single_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                single_win_date_rect, (single_win_date_rect.midright, single_win_date_rect.y))

        if self.settings['achievement']['storya_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[1].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            storya_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['storya_win']", 20, c.WHITE)
            storya_win_date_rect.x = self.achievement_li[1].midright
            storya_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                storya_win_date_rect, (storya_win_date_rect.midright, storya_win_date_rect.y))

        if self.settings['achievement']['storyb_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[2].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            storyb_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['storyb_win']", 20, c.WHITE)
            storyb_win_date_rect.x = self.achievement_li[2].midright
            storyb_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                storyb_win_date_rect, (storyb_win_date_rect.midright, storyb_win_date_rect.y))

        if self.settings['achievement']['storyc_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[3].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            storyc_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['storyc_win']", 20, c.WHITE)
            storyc_win_date_rect.x = self.achievement_li[2].midright
            storyc_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                storyc_win_date_rect, (storyc_win_date_rect.midright, storyc_win_date_rect.y))

        if self.settings['achievement']['storyd_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[4].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            storyd_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['storyd_win']", 20, c.WHITE)
            storyd_win_date_rect.x = self.achievement_li[4].midright
            storyd_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                storyd_win_date_rect, (storyd_win_date_rect.midright, storyd_win_date_rect.y))

        if self.settings['achievement']['speed_master'] == True:
            self.achv_completed_rect.center = self.achievement_li[5].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            speed_master_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['speed_master']", 20, c.WHITE)
            speed_master_date_rect.x = self.achievement_li[5].midright
            speed_master_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                speed_master_date_rect, (speed_master_date_rect.midright, speed_master_date_rect.y))

        if self.settings['achievement']['no_skill_card'] == True:
            self.achv_completed_rect.center = self.achievement_li[6].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            no_skill_card_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['no_skill_card']", 20, c.WHITE)
            no_skill_card_date_rect.x = self.achievement_li[6].midright
            no_skill_card_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                no_skill_card_date_rect, (no_skill_card_date_rect.midright, no_skill_card_date_rect.y))

        if self.settings['achievement']['turtle_win'] == True:
            self.achv_completed_rect.center = self.achievement_li[7].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            turtle_win_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['turtle_win']", 20, c.WHITE)
            turtle_win_date_rect.x = self.achievement_li[7].midright
            turtle_win_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                turtle_win_date_rect, (turtle_win_date_rect.midright, turtle_win_date_rect.y))

        if self.settings['achievement']['first_play'] == True:
            self.achv_completed_rect.center = self.achievement_li[8].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            first_play_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['first_play']", 20, c.WHITE)
            first_play_date_rect.x = self.achievement_li[8].midright
            first_play_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                first_play_date_rect, (first_play_date_rect.midright, first_play_date_rect.y))

        if self.settings['achievement']['card_collector'] == True:
            self.achv_completed_rect.center = self.achievement_li[9].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            card_collector_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['card_collector']", 20, c.WHITE)
            card_collector_date_rect.x = self.achievement_li[9].midright
            card_collector_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(card_collector_date_rect,
                             (card_collector_date_rect.midright, card_collector_date_rect.y))

        if self.settings['achievement']['skill_master'] == True:
            self.achv_completed_rect.center = self.achievement_li[10].midright
            self.screen.blit(self.achv_completed_img, self.achv_completed_rect)

            skill_master_date_rect = rf.TextRect(
                self.screen, "self.settings['achievement_date']['skill_master']", 20, c.WHITE)
            skill_master_date_rect.x = self.achievement_li[10].midright
            skill_master_date_rect.y = self.achv_completed_rect.y + achievement.rect.height
            self.screen.blit(
                skill_master_date_rect, (skill_master_date_rect.midright, skill_master_date_rect.y))

    def sound(self):
        pass

    def handle_event(self):

        scroll_speed = 5
        scroll_pos = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                achievement_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_pos += scroll_speed
                elif event.button == 5:
                    scroll_pos -= scroll_speed

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.close_button.get_rect().collidepoint(event.pos):
                    title = TitleMenu()
                    title.menu()

        for achievement in self.achievement_li:
            achievement.y += scroll_pos

    def menu(self):
        while True:
            self.bg_img_load(c.SETTING_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()


if __name__ == '__main__':
    uno = TitleMenu()
    uno.menu()
