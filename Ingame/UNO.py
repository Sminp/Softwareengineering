import pygame
import sys
from game_functions import *
from constant import *
from settings import Settings, resource_path
from rect_functions import Button, Slider, TextRect
import os

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
        self.setting = Settings()
        self.settings = self.setting.get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        # self.screen.fill(self.settings.bg_color)
        pygame.display.set_caption("UNO!")
        pygame.display.update()
        # self.keysetting = 1
        # self.menu = True

    def bg_img_load(self, filename: str) -> object:
        bg_img = pygame.image.load(resource_path(filename))
        bg_img = pygame.transform.scale(bg_img,
                                        (self.settings['screen']))
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

        setting_key1 = Button(self.screen, self.size[0] * (1 / 5), self.size[1] * (4 / 9),
                              "./image/setting_image/settingkey_wasd.png", 150, 100)
        setting_key2 = Button(self.screen, self.size[0] * (3 / 5), self.size[1] * (4 / 9),
                              "./image/setting_image/settingkey_arrow.png", 150, 100)

        while key_select:
            pygame.draw.rect(self.screen, WHITE, (
                self.size[0] * (1 / 9), self.size[1] *
                (2 / 8), self.size[0] * (7 / 9),
                self.size[1] * (6 / 10)))

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
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])

        # 버튼 속성
        self.x = self.size[0] * (1 / 4)
        self.y = self.size[1] * (5 / 8)
        self.width = self.size[0] * (1 / 8)
        self.height = self.size[1] * (3 / 8)
        self.button_li = self.object_init()

    def object_init(self):
        i = 0
        button_li = []
        for button in TITLE_MENU_BUTTONS:
            button = Button(self.screen, self.x + self.width * i,
                            self.y, button, self.width, self.height)
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
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        # 버튼 속성
        self.x = self.size[0] * (3 / 7)
        self.y = self.size[0] * (1 / 6)
        self.width = self.size[0] * (1 / 3)
        self.height = self.size[1] * (1 / 4)
        self.font = pygame.font.SysFont(self.settings['font'], 30)
        self.user_name = "player"
        self.button, self.computer_rect = self.object_init()
        self.user_name_text = TextRect(self.screen, self.user_name, 30, BLACK)
        self.input_active = False

    def object_init(self):
        button = Button(self.screen, self.x, self.y,
                        GAMESTART_BUTTON, self.width, self.height)

        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.size[1] - 500) / 6),
                               self.size[0] / 5, self.size[1] / 6)
            if i == 0:
                label = "computer1"
            else:
                label = "add"
            computer_rect.append([rect, label])

        return button, computer_rect

    def object_show(self):
        self.button.show()

        self.user_name_text.show(
            (self.size[0] * (3 / 5), self.size[1] * (2 / 3)))

        for rect, label in self.computer_rect:
            pygame.draw.rect(self.screen, WHITE, rect)
            label_surface = self.font.render(label, True, BLACK)
            self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

        # 이름 수정할 때 커서 표시
        if self.input_active:
            pygame.draw.line(self.screen, BLACK,
                             (self.user_name_text.rect.x +
                              self.user_name_text.rect.w, self.user_name_text.rect.y),
                             (self.user_name_text.rect.x + self.user_name_text.rect.w,
                              self.user_name_text.rect.y + self.user_name_text.rect.h), 2)

    def sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./sound/playing_bgm.mp3')
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
                        if text != "add":
                            result += 1
                    uno_ = Game(self, result, user_name=self.user_name)
                    uno_.startgame()

                for i in range(len(self.computer_rect)):
                    if i == 0:
                        continue
                    else:
                        if self.computer_rect[i][0].collidepoint(event.pos):
                            if self.computer_rect[i][1] == "add" and self.computer_rect[i - 1][1] != "add":
                                self.computer_rect[i][1] = "computer{}".format(
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
            self.bg_img_load('./image/playing_image/playing_background.png')
            self.object_show()
            self.handle_event()

            pygame.display.update()


class SettingScreen(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        self.button_li, self.slider_li, self.rect = self.object_init()
        self.setting_text = TextRect(self.screen, "SETTING", 35, WHITE)
        self.screen_setting_text = TextRect(self.screen, "화면 크기", 20, BLACK)

    def object_init(self):
        i = 3
        button_li = []
        for button in SIZE_BUTTONS:
            button = Button(self.screen, self.size[0] * (i / 10), self.size[1] * (1 / 2),
                            button, 100, 50)
            button_li.append(button)
            i += 2

        # self.size[0] 이렇게 접근하는 거 너무 길지 않나?
        close_button = Button(self.screen, self.size[0] * (
            5 / 6), self.size[1] * (3 / 11), SETTING_CLOSE_BUTTON, 20, 20)
        key_button = Button(self.screen, self.size[0] * (
            1 / 8), self.size[1] * (7 / 11), SETTING_KEY_BUTTON, 100, 50)
        init_button = Button(self.screen, self.size[0] * (
            1 / 8), self.size[1] * (6 / 8), SETTING_INIT_BUTTON, 100, 50)
        save_button = Button(self.screen, self.size[0] * (
            8 / 11), self.size[1] * (6 / 8), SETTING_SAVE_BUTTON, 100, 50)
        settingcolor_button = Button(self.screen, self.size[0] * (
            8 / 11), self.size[1] * (7 / 11), SETTING_RECT, 100, 50)
        buttons = [close_button, key_button, init_button,
                   save_button, settingcolor_button]

        for button in buttons:
            button_li.append(button)

        j = 6
        sliders_li = []
        for text in SLIDER_TEXT:
            slider = Slider(self.screen, text, self.size[0] / 2, (self.size[0] * (
                3 / 10), self.size[1] * (j / 20)), (0, 100))
            sliders_li.append(slider)
            j += 1.5

        rect = pygame.Rect(
            self.size[0] * (8 / 11), self.size[1] * (7 / 11), 50, 50)

        return button_li, sliders_li, rect

    def object_show(self):
        pygame.draw.rect(self.screen, WHITE, (
            self.size[0] * (1 / 9), self.size[1] * (
                2 / 8), self.size[0] * (7 / 9),
            self.size[1] * (6 / 10)))

        self.setting_text.show(
            (self.size[0] * (1 / 5), self.size[1] * (1 / 6)))
        self.screen_setting_text.show(
            (self.size[0] * (1 / 5), self.size[1] * (6 / 11)))

        for button in self.button_li:
            button.show()

        i = 6
        for slider in self.slider_li:
            slider.show()
            slider.show_value(
                (self.size[0] * (1 / 5), self.size[1] * (i / 20)))
            i += 1.5

        pygame.draw.rect(self.screen, BLACK, self.rect)

    def sound(self):
        pass

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            for slider in self.slider_li:
                slider.operate(event)

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
                    self.settings['fullscreen'] = pygame.FULLSCREEN
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    # 테스트 할려고 화면 크기 임시로 정함 -> 나중에 수정
                    self.size[0] = 1280
                    self.size[1] = 720
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                    self.button_li, self.slider_li, self.rect = self.object_init()

                elif self.button_li[2].get_rect().collidepoint(event.pos):
                    # 테스트 할려고 화면 크기 임시로 정함 -> 나중에 수정
                    self.size[0] = 800
                    self.size[1] = 600
                    self.screen = pygame.display.set_mode(
                        (self.settings['screen']), flags=self.settings['fullscreen'])
                    self.button_li, self.slider_li, self.rect = self.object_init()

                elif self.button_li[3].get_rect().collidepoint(event.pos):
                    title = TitleMenu()
                    title.menu()

                elif self.button_li[4].get_rect().collidepoint(event.pos):
                    pass  # 키보드 설정 함수 실행
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
                    if self.rect.x == int(self.size[0] * (8 / 11)):
                        self.rect.x += 50
                    elif self.rect.x == int(self.size[0] * (8 / 11)) + 50:
                        self.rect.x -= 50

    def menu(self):
        selected = 1

        while True:
            self.bg_img_load("./image/setting_image/settingbackground.jpg")
            self.object_show()
            self.handle_event()

            pygame.display.update()


class StoryMode(UNOGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        self.width = self.size[0] * (1 / 5)
        self.height = self.size[1] * (1 / 5)
        self.button_li, self.text = self.object_init()

    def object_init(self):
        i = 1
        button_li = []
        for button in STORYMODE_MENU_BUTTONS:
            button = Button(self.screen, self.size[0] * (i / 40), self.size[1] * (2 / 5),
                            button,
                            self.width, self.height)
            button_li.append(button)
            i += 10 if i != 1 else i * 10
        text = TextRect(self.screen, "STORY MODE", 50, WHITE)
        return button_li, text

    def object_show(self):
        for button in self.button_li:
            button.show()
        self.text.show(
            (self.size[0] // 5, self.size[1] // 10))

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
                            ask_popup = YesNo(2, 2)
                            ask_popup.menu()
                        elif i == 1:
                            ask_popup = YesNo(4, 3)
                            ask_popup.menu()
                        elif i == 2:
                            ask_popup = YesNo(3, 4)
                            ask_popup.menu()
                        else:
                            ask_popup = YesNo(3, 5)
                            ask_popup.menu()

    def menu(self):
        self.sound()

        while True:
            self.bg_img_load("./image/map_image/map_back.jpg")
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
    def __init__(self, player_num, difficulty):
        super().__init__()
        self.yes_no = True
        self.player_num = player_num
        self.difficulty = difficulty
        self.size = self.settings['screen']
        self.width = self.size[0] * (3 / 7)
        self.height = self.size[1] * (2 / 5)
        self.button_li, self.text = self.object_init()

    def object_init(self):
        i = 0
        button_li = []
        for button in YESNO_BUTTONS:
            button = Button(self.screen, self.width,
                            self.height + i, button, 100, 50)
            button_li.append(button)
            i += 100
        text = TextRect(self.screen, "대전을 시작하겠습니까?", 30, BLACK)
        return button_li, text

    def object_show(self):
        pygame.draw.rect(self.screen, WHITE, (
            self.size[0] / 2 - 200, self.size[1] / 3 - 100, 400, 400))
        for button in self.button_li:
            button.show()
        self.text.show(
            (self.size[0] / 2, self.size[1] / 3))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_li[0].get_rect().collidepoint(event.pos):
                    # 여기 생성자에 uno_game을 넘겨줘야 함 ...
                    uno = Game(self, self.player_num, self.difficulty)
                    uno.startgame()
                    self.yes_no = False
                elif self.button_li[1].get_rect().collidepoint(event.pos):
                    self.yes_no = False

    def menu(self):
        while self.yes_no:
            self.object_show()
            self.handle_event()

            pygame.display.update()


if __name__ == '__main__':
    uno = TitleMenu()
    uno.menu()
