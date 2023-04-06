import pygame
import sys
from game_functions import *
from constant import *
from settings import *

img_basic_address = './image/'


# 텍스트 구현
def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.SysFont(text_font, text_size)
    new_text = new_font.render(message, pygame.K_0, text_color)  # pygame.K_0가 의미하는 것은?
    return new_text


def background_img_load(filename: str, size=(SCREEN_WIDTH, SCREEN_HEIGHT)) -> object:
    background_img = pygame.image.load(filename)
    return pygame.transform.scale(background_img, (size[0], size[1]))


def terminate():
    pygame.quit()
    sys.exit()


class UNOGame():
    """UNOGame 시작화면 밑 설정화면을 나타냅니다."""

    def __init__(self):
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background_color = WHITE
        self.font = MALGUNGOTHIC
        self.player_num = 2
        self.difficulty = 1
        self.screen.fill(self.background_color)
        self.mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()

    # 시작 화면
    def main_menu(self):
        pygame.init()
        self.screen.blit(background_img_load("./image/TitleImage/TitleBackground.jpg"), (0, 0))

        selected = 0

        menu = True

        while menu:
            # 안정적으로 소리가 나오기 위한 코드 - 이해하면 지우기
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # 효과음 넣기 - 해결하면 지우기
            # sound = pygame.mixer.Sound('./sound/menu.wav')
            self.screen.blit(background_img_load("./image/TitleImage/TitleBackground.jpg"), (0, 0))
            start_button = Button(self.screen, 400 - 200, 400, "./image/TitleImage/StartButton.png", 200, 200)
            menu_button = Button(self.screen, 400 - 100, 400 - 30, "./image/TitleImage/MenuButton.png", 200, 200)
            end_button = Button(self.screen, 400, 400, "./image/TitleImage/EndButton.png", 200, 200)
            button_list = [start_button, menu_button, end_button]
            start_button.show_botton()
            menu_button.show_botton()
            end_button.show_botton()
            self.mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, YELLOW,
                             [button_list[selected].x, button_list[selected].y, button_list[selected].width,
                              button_list[selected].height], 5)

            # 이벤트를 발생시키는 입력
            for event in pygame.event.get():
                # 창 버튼
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
                        if selected >= 2:
                            selected = 2
                        else:
                            selected += 1
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            # self.lobby_screen()
                            self.story()
                        elif selected == 1:
                            self.setting_screen()
                        else:
                            pygame.quit()
                            sys.exit()
                # 마우스 입력
                if event.type == pygame.MOUSEBUTTONUP:
                    if button_list[0].x <= self.mouse_pos[0] <= button_list[0].width + button_list[0].x and \
                            button_list[
                                0].y <= self.mouse_pos[1] <= button_list[0].y + button_list[0].height:
                        self.lobby_screen()
                    if button_list[1].x <= self.mouse_pos[0] <= button_list[1].width + button_list[1].x and \
                            button_list[
                                1].y <= self.mouse_pos[1] <= button_list[1].y + button_list[1].height:
                        self.setting_screen()
                    if button_list[2].x <= self.mouse_pos[0] <= button_list[2].width + button_list[2].x and \
                            button_list[
                                2].y <= self.mouse_pos[1] <= button_list[2].y + button_list[2].height:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            pygame.display.set_caption("UNO!")

    def lobby_screen(self):

        pygame.init()

        self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))

        font = pygame.font.SysFont(self.font, 25)
        name_text = "player"
        text_surface = font.render(name_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen_width // 2 + 70, self.screen_height // 2 + 150))

        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.screen_height - 500) / 6), 150, 110)
            if i == 0:
                label = "computer1"
            else:
                label = "add"
            computer_rect.append([rect, label])

        # 아직 게임 시작 버튼이 없어서 못 넣음 
        gamestart_button = Button(self.screen, 350, 150, "./image/button_img.png", 200, 100)
        gamestart_button.show_botton()

        input_active = False
        lobby = True

        while lobby:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if text_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False

                    if gamestart_button.x <= mouse_pos[
                        0] <= gamestart_button.width + gamestart_button.x and gamestart_button.y <= mouse_pos[
                        1] <= gamestart_button.y + gamestart_button.height:
                        result = 1
                        for rect, text in computer_rect:
                            if text != "add":
                                result += 1
                        uno_ = Game(result,player_name=name_text)
                        uno_.startgame()

                    for i in range(len(computer_rect)):
                        if i == 0:
                            continue
                        else:
                            if computer_rect[i][0].collidepoint(event.pos):
                                if computer_rect[i][1] == "add" and computer_rect[i - 1][1] != "add":
                                    computer_rect[i][1] = "computer{}".format(i + 1)
                                else:
                                    if i == 4:
                                        computer_rect[i][1] = "add"
                                    else:
                                        if computer_rect[i + 1][1] == "add":
                                            computer_rect[i][1] = "add"

                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            name_text = name_text[:-1]
                        else:
                            name_text += event.unicode
                        text_surface = font.render(name_text, True, BLACK)
                        text_rect.size = text_surface.get_size()

            self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
            self.screen.blit(text_surface, text_rect)
            gamestart_button.show_botton()

            for rect, label in computer_rect:
                pygame.draw.rect(self.screen, WHITE, rect)
                label_surface = font.render(label, True, BLACK)
                self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

            if input_active:
                pygame.draw.line(self.screen, BLACK, (text_rect.x + text_rect.w, text_rect.y),
                                 (text_rect.x + text_rect.w, text_rect.y + text_rect.h), 2)
            else:
                self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
                self.screen.blit(text_surface, text_rect)
                gamestart_button.show_botton()
                for rect, label in computer_rect:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    label_surface = font.render(label, True, BLACK)
                    self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

            pygame.display.update()

    def setting_screen(self):

        pygame.init()
        game_exit = False
        selected = 1

        # 배경음, 효과음 slider
        backgrounder_slider = Slider(self.screen, 300, (250, 180), (0, 100))
        sound_effect_slider = Slider(self.screen, 300, (250, 250), (0, 100))

        while not game_exit:
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
                            selected = selected
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

            self.screen.fill(WHITE)

            # 설정화면 텍스트 표시

            setting_text = text_format("설정 화면", MALGUNGOTHIC, 50, BLACK)
            self.screen.blit(setting_text, (80, 50))

            # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야 함
            screen_setting_text = text_format("화면설정", MALGUNGOTHIC, 50, BLACK)
            self.screen.blit(screen_setting_text, (80, 300))

            # 화면 설정 버튼 - 변수명 바꿔야 함
            gamestart_button = Button(self.screen, 600, 50, "./image/button_img.png", 100, 50)
            sizefull_button = Button(self.screen, 270, 315, "./image/button_img.png", 100, 50)
            size16_button = Button(self.screen, 420, 315, "./image/button_img.png", 100, 50)
            size4_button = Button(self.screen, 570, 315, "./image/button_img.png", 100, 50)
            gamestart_button.show_botton()
            sizefull_button.show_botton()
            size16_button.show_botton()
            size4_button.show_botton()

            # 배경음, 효과음 그림
            backgrounder_slider.draw()
            backgrounder_slider.draw_value('배경음', (130, 180))
            sound_effect_slider.draw()
            sound_effect_slider.draw_value('효과음', (130, 250))

            # 조작키 설정, 설정 초기화, 설정 저장 버튼
            control_button = Button(self.screen, 80, 400, "./image/button_img.png", 100, 50)
            settinginit_button = Button(self.screen, 80, 500, "./image/button_img.png", 100, 50)
            settingsave_button = Button(self.screen, SCREEN_WIDTH // 2 + 200, 500, "./image/button_img.png", 100, 50)
            control_button.show_botton()
            settinginit_button.show_botton()
            settingsave_button.show_botton()
            buttons = [control_button, settinginit_button, settingsave_button]

            pygame.display.update()

    def story(self):

        pygame.init()
        story = True

        font = pygame.font.SysFont(self.font, 50)
        text = "스토리 모드"
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 5, self.screen_height // 10))

        story_map = [pygame.Rect((i * 200 + 50, self.screen_height // 2 - 25, 50, 50)) for i in range(4)]

        while story:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(story_map)):
                        if story_map[i].collidepoint(event.pos):
                            if i == 0:
                                self.difficulty = 2
                                print("A 지역 : 난이도 {}".format(self.difficulty))
                                # 로비화면으로 전환 
                            elif i == 1:
                                self.difficulty = 3
                                self.player_num = 4
                                print("B 지역: 플레이어 수 {}, 난이도 {}".format(self.player_num, self.difficulty))
                                uno = Game(self.player_num, self.difficulty)
                                uno.startgame()
                            elif i == 2:
                                self.difficulty = 4
                                self.player_num = 3
                                uno = Game(self.player_num, self.difficulty)
                                uno.startgame()
                                print("C 지역 : 플레이어 수 {}, 난이도 {}".format(self.player_num, self.difficulty))
                            else:
                                self.difficulty = 5
                                pass

            self.screen.fill(WHITE)
            self.screen.blit(text_surface, text_rect)
            for rect in story_map:
                pygame.draw.rect(self.screen, BLACK, rect)

            pygame.display.update()


# 버튼 클래스 안에 하이라이트 그림 넣으면 안되려나?
# 버튼 클래스
class Button:
    def __init__(self, screen, x, y, img, width, height):
        self.screen = screen
        # self.rect = pygame.Rect(x,y, 30, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.img = pygame.transform.scale(pygame.image.load(img), [width, height])
        # self.action = action
        self.cliked_num = 0

    def show_botton(self):
        self.screen.blit(self.img, (self.x, self.y))

        # mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        # if x + width > mouse[0] > x and y + height > mouse[1] > y:
        #     # 마우스를 버튼위에 올렸을 때 색깔 변함
        #     pygame.draw.rect(screen, self.hover_color, self.rect)
        #     if click[0] == 1 and action != None:
        #         # 클릭하면 해당 버튼 기능 수행
        #         action()
        # else:
        #     pygame.draw.rect(screen, self.color, self.rect)

        # 버튼의 text 설정
        # font = pygame.font.SysFont(font_name,font_size)
        # self.textSurf = font.render(text,True,BLACK)
        # self.textRect = self.textSurf.get_rect()
        # self.textRect.center = ((x + width/2),(y + height/2))
        # screen.blit(self.textSurf, self.textRect)

    def cliked(self):
        self.screen.blit(self.img, (self.x, self.y -5))
        self.cliked_num += 1

    def check_cliked_num(self):
        pass


if __name__ == '__main__':
    uno = UNOGame()
    uno.main_menu()
