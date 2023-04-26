import pygame
import sys
from game_functions import *
from constant import *
from settings import Settings
from rect_functions import Button, Slider, TextRect
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


img_basic_address = './image/'


# 지울 예정
# 텍스트 구현
def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.SysFont(text_font, text_size)
    new_text = new_font.render(message, pygame.K_0, text_color)  # pygame.K_0가 의미하는 것은?
    return new_text


# 끝내는 함수
def terminate():
    pygame.quit()
    sys.exit()


class UNOGame:
    """UNOGame 화면"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()  # 다른 방법은 없을까? 클래스 컴포지션
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen.fill(self.settings.bg_color)
        pygame.display.set_caption("UNO!")
        pygame.display.update()
        # self.keysetting = 1
        # self.menu = True
        # self.story_screen = False

    def bg_img_load(self, filename: str) -> object:
        bg_img = pygame.image.load(resource_path(filename))
        bg_img = pygame.transform.scale(bg_img,
                                        (self.settings.screen_width, self.settings.screen_height))
        return self.screen.blit(bg_img, (0, 0))

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

    # 설정 클래스로 이동
    def key_select_screen(self):
        key_select = True

        setting_key1 = Button(self.screen_width * (1 / 5), self.screen_height * (4 / 9),
                              "./image/setting_image/settingkey_wasd.png", 150, 100)
        setting_key2 = Button(self.screen_width * (3 / 5), self.screen_height * (4 / 9),
                              "./image/setting_image/settingkey_arrow.png", 150, 100)

        while key_select:
            pygame.draw.rect(self.screen, WHITE, (
                self.screen_width * (1 / 9), self.screen_height * (2 / 8), self.screen_width * (7 / 9),
                self.screen_height * (6 / 10)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if setting_key1.get_rect().collidepoint(event.pos):
                        self.keysetting = 1
                        key_select = False

            setting_key1.show()
            setting_key2.show()

            pygame.display.update()


class TitleMenu(UNOGame):
    def __init__(self):
        super().__init__()
        # 버튼 속성
        self.x = 1 / 4
        self.y = 5 / 8
        self.width = 100
        self.height = 230
        self.button_li = self.object_init()

    def object_init(self):
        i = 0
        button_li = []
        for button in TITLE_MENU_BUTTONS:
            button = Button(self.settings.screen_width * self.x + self.width * i,
                            self.settings.screen_height * self.y, button, self.width, self.height)
            button_li.append(button)
            i += 1
        return button_li

    def object_show(self, *button_li):
        for button in button_li:
            button.show()

    def sound(self):
        pygame.mixer.music.load('./sound/title_bgm.mp3')
        pygame.mixer.music.play(-1)

    # keysetting 하이라이트 따로 변수 만들어서 저장.
    def handle_event(self):
        selected = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # sound.play()
                    if selected <= 0:
                        selected = 0
                    else:
                        selected = selected - 1
                elif event.key == pygame.K_RIGHT:
                    if selected >= 3:
                        selected = 3
                    else:
                        selected += 1
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        LobbyScreen().menu()
                    elif selected == 1:
                        StoryMode().menu()
                    elif selected == 2:
                        SettingScreen().menu()
                    else:
                        terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                select_sound = pygame.mixer.Sound('./sound/select_sound.mp3')
                select_sound.play()
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    LobbyScreen().menu()
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    StoryMode().menu()
                elif self.button_li[2].get_rect().collidepoint(event.pos):
                    SettingScreen().menu()
                elif self.button_li[3].get_rect().collidepoint(event.pos):
                    terminate()

    def menu(self):
        self.sound()

        while True:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            self.bg_img_load("./image/title_image/title_background.jpg")
            self.object_show(*self.button_li)
            self.handle_event()
            pygame.display.update()


class LobbyScreen(UNOGame):
    def __init__(self):
        super().__init__()
        # 버튼 속성
        self.x = 1 / 4
        self.y = 5 / 8
        self.width = 100
        self.height = 230
        self.font = pygame.font.SysFont(self.settings.font, 30)
        self.button_li = self.object_init()
        self.computer_rect = self.computer_rect_init()

    def object_init(self):
        button_li = Button(self.settings.screen_width * (2 / 5),
                           self.settings.screen_height * (1 / 4), GAMESTART_BUTTON,
                           300, 150)
        return button_li

    def object_show(self, *button):
        button[0].show()

    def sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./sound/playing_bgm.mp3')
        pygame.mixer.music.play(-1)

    def computer_rect_init(self):
        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.settings.screen_height - 500) / 6),
                               self.settings.screen_width / 5, self.settings.screen_height / 6)
            if i == 0:
                label = "computer1"
            else:
                label = "add"
            computer_rect.append([rect, label])
        return computer_rect

    def computer_modify(self):
        pass

    def text_rect_init(self):
        pass

    def handle_event(self):
        pass

    def menu(self):
        self.sound()

        input_active = False
        lobby = True

        while lobby:

            name_text = "player"
            text_surface = self.font.render(name_text, True, WHITE)
            text_rect = text_surface.get_rect(
                center=(self.settings.screen_width * (3 / 5), self.settings.screen_height * (2 / 3)))

            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False

                    if self.button_li.get_rect().collidepoint(event.pos):
                        result = 1
                        for rect, text in self.computer_rect:
                            if text != "add":
                                result += 1
                        uno_ = Game(self, result, player_name=name_text)
                        uno_.startgame()

                    for i in range(len(self.computer_rect)):
                        if i == 0:
                            continue
                        else:
                            if self.computer_rect[i][0].collidepoint(event.pos):
                                if self.computer_rect[i][1] == "add" and self.computer_rect[i - 1][1] != "add":
                                    self.computer_rect[i][1] = "computer{}".format(i + 1)
                                else:
                                    if i == 4:
                                        self.computer_rect[i][1] = "add"
                                    else:
                                        if self.computer_rect[i + 1][1] == "add":
                                            self.computer_rect[i][1] = "add"

                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            name_text = name_text[:-1]
                        else:
                            name_text += event.unicode
                        text_surface = self.font.render(name_text, True, WHITE)
                        text_rect.size = text_surface.get_size()
                        # 나중에 옮기기

            for rect, label in self.computer_rect:
                pygame.draw.rect(self.screen, WHITE, rect)
                label_surface = self.font.render(label, True, BLACK)
                self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

            if input_active:
                pygame.draw.line(self.screen, WHITE, (text_rect.x + text_rect.w, text_rect.y),
                                 (text_rect.x + text_rect.w, text_rect.y + text_rect.h), 2)
            else:
                self.screen.blit(text_surface, text_rect)
                for rect, label in self.computer_rect:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    label_surface = self.font.render(label, True, BLACK)
                    self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))
            self.bg_img_load('./image/playing_image/playing_background.png')
            self.object_show(self.button_li)

            pygame.display.update()


class SettingScreen(UNOGame):
    def __init__(self):
        super().__init__()
        self.button_li = self.object_init()

    def object_init(self):
        i = 3
        button_li = []
        for button in SIZE_BUTTONS:
            button = Button(self.settings.screen_width * (i / 10), self.settings.screen_height * (1 / 2),
                            button, 100, 50)
            button_li.append(button)
            i += 2
        return button_li

    def object_show(self, *button_li):
        for button in button_li:
            button.show()

    def sound(self):
        pass

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            backgrounder_slider.operate(event)
            sound_effect_slider.operate(event)

            # 키보드 버튼
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # sound.play()
                    if selected <= 1:
                        selected = 1
                    else:
                        selected = selected - 1
                elif event.key == pygame.K_RIGHT:
                    # sound.play()
                    if selected >= 3:
                        selected = 3
                    else:
                        selected = selected + 1
                if event.key == pygame.K_RETURN:
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
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                          pygame.FULLSCREEN)
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    # 여기 손대기
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                    backgrounder_slider.set_value(self.screen_width / 2,
                                                  (self.screen_width * (3 / 10), self.screen_height * (4 / 13)))
                    sound_effect_slider.set_value(self.screen_width / 2,
                                                  (self.screen_width * (3 / 10), self.screen_height * (6 / 15)))
                    rect.x = self.screen_width * (8 / 11)
                    rect.y = self.screen_height * (7 / 11)
                elif self.button_li[2].get_rect().collidepoint(event.pos):
                    self.screen_width = 800
                    self.screen_height = 600
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                    backgrounder_slider.set_value(self.screen_width / 2,
                                                  (self.screen_width * (3 / 10), self.screen_height * (4 / 13)))
                    sound_effect_slider.set_value(self.screen_width / 2,
                                                  (self.screen_width * (3 / 10), self.screen_height * (6 / 15)))
                    rect.x = self.screen_width * (8 / 11)
                    rect.y = self.screen_height * (7 / 11)
                elif control_button.get_rect().collidepoint(event.pos):
                    self.key_select_screen()
                elif close_button.get_rect().collidepoint(event.pos):
                    self.title_menu()

                elif rect.collidepoint(event.pos):
                    if rect.x == int(self.screen_width * (8 / 11)):
                        rect.x += 50
                        rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                    elif rect.x == int(self.screen_width * (8 / 11)) + 50:
                        rect.x -= 50
                        rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)

    def menu(self):
        selected = 1

        rect = pygame.Rect(self.screen_width * (8 / 11), self.screen_height * (7 / 11), 50, 50)

        # 배경음, 효과음 slider

        backgrounder_slider = Slider(self.screen, self.screen_width / 2,
                                     (self.screen_width * (3 / 10), self.screen_height * (4 / 13)), (0, 100))
        sound_effect_slider = Slider(self.screen, self.screen_width / 2,
                                     (self.screen_width * (3 / 10), self.screen_height * (6 / 15)), (0, 100))

        while True:
            self.bg_img_load("./image/setting_image/settingbackground.jpg")
            self.object_show(*self.button_li)
            self.handle_event()
            pygame.draw.rect(self.screen, WHITE, (
                self.screen_width * (1 / 9), self.screen_height * (2 / 8), self.screen_width * (7 / 9),
                self.screen_height * (6 / 10)))

            # 설정화면 텍스트 표시
            setting_text = text_format("SETTING", MALGUNGOTHIC, 35, WHITE)
            self.screen.blit(setting_text, (self.screen_width * (1 / 8), self.screen_height * (1 / 7)))

            # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야 함
            screen_setting_text = text_format("화면크기", MALGUNGOTHIC, 20, BLACK)
            self.screen.blit(screen_setting_text, (self.screen_width * (1 / 8), self.screen_height * (8 / 15)))

            # 배경음, 효과음 그림
            backgrounder_slider.draw()
            backgrounder_slider.draw_value('배경음', (self.screen_width * (1 / 8), self.screen_height * (2 / 7)))
            sound_effect_slider.draw()
            sound_effect_slider.draw_value('효과음', (self.screen_width * (1 / 8), self.screen_height * (3 / 8)))

            # 조작키 설정, 설정 초기화, 설정 저장 버튼
            control_button = Button(self.screen_width * (1 / 8), self.screen_height * (7 / 11),
                                    "./image/setting_image/key_setting.jpg", 100, 50)
            settinginit_button = Button(self.screen_width * (1 / 8), self.screen_height * (6 / 8),
                                        "./image/setting_image/settinginit.jpg", 100, 50)
            settingsave_button = Button(self.screen_width * (8 / 11), self.screen_height * (6 / 8),
                                        "./image/setting_image/settingsave.jpg", 100, 50)
            control_button.show()
            settinginit_button.show()
            settingsave_button.show()
            buttons = [control_button, settinginit_button, settingsave_button]

            settingcolor_button = Button(self.screen_width * (8 / 11), self.screen_height * (7 / 11),
                                         "./image/setting_image/rect.jpg", 100, 50)
            settingcolor_button.show()
            pygame.draw.rect(self.screen, BLACK, rect)

            pygame.display.update()


class StoryMode(UNOGame):
    def __init__(self):
        super().__init__()
        self.width = self.settings.screen_width * (1 / 5)
        self.height = self.settings.screen_height(1 / 5)
        self.button_li = self.object_init()

    def object_init(self):
        i = 1
        button_li = []
        for button in STORYMODE_MENU_BUTTONS:
            button = Button(self.settings.screen_width * (i / 40), self.settings.screen_height(2 / 5),
                            button,
                            self.width, self.height)
            button_li.append(button)
            i += 10 if i != 1 else i * 10
        return button_li

    def object_show(self, *button_li):
        for button in button_li:
            button.show()

    def sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./sound/storymode_bgm.mp3')
        pygame.mixer.music.play(-1)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.button_li)):
                    if self.button_li[i].get_rect().collidepoint(event.pos):
                        if i == 0:
                            self.yes_no(2, 2)
                        elif i == 1:
                            self.yes_no(6, 3)
                        elif i == 2:
                            self.yes_no(2, 4)
                        else:
                            self.yes_no(3, 5)

    def menu(self):
        self.sound()

        self.bg_img_load("./image/map_image/map_back.jpg")
        font = pygame.font.SysFont(self.font, 50)
        text = "STORY MODE"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.screen_width // 5, self.screen_height // 10))

        while self.story:
            self.object_show(*self.button_li)
            self.handle_event()
            self.screen.blit(text_surface, text_rect)
            pygame.display.update()

    # 지역 선택하면 플레이할 건지 물어보는 창
    def yes_no(self, player_num, difficulty):
        yes_no = True
        self.story_screen = False

        yes_button = Button(self.screen_width * (3 / 7), self.screen_height * (2 / 5),
                            "./image/map_image/story_yes.jpg", 100, 50)
        no_button = Button(self.screen_width * (3 / 7), self.screen_height * (2 / 5) + 100,
                           "./image/map_image/story_no.jpg", 100, 50)

        while yes_no:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭시 다시 시작
                    if yes_button.get_rect().collidepoint(event.pos):
                        self.player_num = player_num
                        self.difficulty = difficulty
                        uno = Game(self, self.player_num, self.difficulty)
                        uno.startgame()
                        yes_no = False
                    elif no_button.get_rect().collidepoint(event.pos):
                        self.story_screen = True
                        yes_no = False
            pygame.draw.rect(self.screen, WHITE, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, BLACK, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400),
                             5)
            ask_text = text_format("대전을 시작하겠습니까?", MALGUNGOTHIC, 30, BLACK)
            ask_text_rect = ask_text.get_rect(center=(self.screen_width / 2, self.screen_height / 3))
            yes_button.show()
            no_button.show()
            self.screen.blit(ask_text, ask_text_rect)

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


# 이거는 굳이 추상클래스로 구현 안해도 될 것 같다. _Mix_in
class RectInit(UNOGame):
    """화면에 직사각형을 그리는 클래스"""

    def __init__(self):
        super().__init__()

    def show(self):
        pass

    def get_rect(self):
        return self.rect


if __name__ == '__main__':
    uno = TitleMenu()
    uno.menu()
