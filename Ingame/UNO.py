import pygame
import sys
from game_functions import *
from constant import *
from settings import *
import math

img_basic_address = './image/'


class UNOGame():
    """UNOGame 시작화면 밑 설정화면을 나타냅니다."""

    def __init__(self):
        pygame.init()
        # self.background = pygame.image.load("Ingame/image/TitleImage/TitleBackground.jpg")
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.background_Color = WHITE
        self.playernum = 2
        self.difficulty = 1
        self.font = MALGUNGOTHIC
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.background_Color)
        # self.screen.blit(self.background, (0, 0))
        self.mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()

    # 텍스트 구현
    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.SysFont(textFont, textSize)
        newText = newFont.render(message, pygame.K_0, textColor)
        return newText

    # 시작 화면
    def main_menu(self):
        pygame.init()
        self.screen_background_img = pygame.image.load("image/TitleImage/TitleBackground.jpg")
        self.background = pygame.transform.scale(self.screen_background_img, (800, 600))
        self.screen.blit(self.background, (0, 0))

        # 기본 버튼이 1 (왼쪽 시작 버튼) - 해결하면 지우기
        selected = 1

        menu = True
        while menu:
            # 안정적으로 소리가 나오기 위한 코드 - 이해하면 지우기
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # 효과음 넣기 - 해결하면 지우기
            # sound = pygame.mixer.Sound('./sound/menu.wav')

            # 이벤트를 발생시키는 입력
            for event in pygame.event.get():
                # 창 버튼
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

                # 마우스 입력
                if event.type == pygame.MOUSEBUTTONUP:
                    # 마우스 누를 때도 효과음이라면 넣기 - 해결하면 지우기
                    # 좌표로 채우기 버튼 1, 2, 3 - 해결하면 지우기
                    if button_list[0].x <= self.mouse_pos[0] <= button_list[0].width and button_list[0].y <= \
                            self.mouse_pos[1] <= button_list[0].height:
                        print("확인")
                    if button_list[1].x <= self.mouse_pos[0] <= button_list[1].width and button_list[1].y <= \
                            self.mouse_pos[1] <= button_list[1].height:
                        pass
                    if button_list[2].x <= self.mouse_pos[0] <= button_list[2].width and button_list[2].y <= \
                            self.mouse_pos[1] <= button_list[2].height:
                        pass

            # 버튼 클래스 선택
            start_button = Button(self.screen, 0, 0, "image/TitleImage/StartButton.png", 800, 600)

            menu_button = Button(self.screen, 0, 0, "image/TitleImage/MenuButton.png", 800, 600)

            end_button = Button(self.screen, 0, 0, "image/TitleImage/EndButton.png", 800, 600)
            # 버튼 클래스로  pass 대체 - 해결하면 지우기
            # if문은 선택했을 때의 변화 else문은 선택하지 않았을 때의 변화 - 해결하면 지우기

            button_list = [start_button, menu_button, end_button]
            if selected == 1:
                pass
            else:
                pass
            if selected == 2:
                pass
            else:
                pass
            if selected == 3:
                pass
            else:
                pass

            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")


# 버트 클래스
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

        self.screen.blit(self.img, (x, y))

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


# 기획이 완료된 후 수정
"""
    # 로비 화면
    def set_players(self):
        pygame.init()
        # 배경 이미지 넣기 - 해결하면 지우기
        self.background = pygame.image.load('./img/default.png')
        self.screen.blit(self.background, (-100, -70))

        # 플레이어 기본 명 수 설정 - 해결하면 지우기
        selected = 1
        menu = True
        while menu:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # 효과음 집어 넣기
            sound = pygame.mixer.Sound('./sound/menu.wav')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        sound.play()
                        if selected <= 1:
                            selected = 1
                        else:
                            selected = selected - 1
                    elif event.key == K_DOWN:
                        sound.play()
                        if selected >= 4:
                            selected = 4
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN:
                        if selected <= 1:
                            self.playernum = 2
                            self.background = pygame.image.load('./img/background.png')
                            return
                        if selected == 2:
                            self.playernum = 3
                            self.background = pygame.image.load('./img/background.png')
                            return
                        if selected == 3:
                            self.playernum = 4
                            self.background = pygame.image.load('./img/background.png')
                            return
                        if selected >= 4:
                            self.background = pygame.image.load('./img/background.png')
                            return

            if selected == 1:
                text_two = self.text_format("2 PLAYERS", self.font, 50, (255, 24, 0))
            else:
                text_two = self.text_format("2 PLAYERS", self.font, 50, (0, 0, 0))
            if selected == 2:
                text_three = self.text_format("3 PLAYERS", self.font, 50, (255, 24, 0))
            else:
                text_three = self.text_format("3 PLAYERS", self.font, 50, (0, 0, 0))
            if selected == 3:
                text_four = self.text_format("4 PLAYERS", self.font, 50, (255, 24, 0))
            else:
                text_four = self.text_format("4 PLAYERS", self.font, 50, (0, 0, 0))
            if selected == 4:
                text_quit = self.text_format("BACK", self.font, 50, (255, 24, 0))
            else:
                text_quit = self.text_format("BACK", self.font, 50, (0, 0, 0))

            two_rect = text_two.get_rect()
            three_rect = text_three.get_rect()
            four_rect = text_four.get_rect()
            quit_rect = text_quit.get_rect()

            self.screen.blit(text_two, (self.screen_width / 2 - (two_rect[2] / 2), 180))
            self.screen.blit(text_three, (self.screen_width / 2 - (three_rect[2] / 2), 240))
            self.screen.blit(text_four, (self.screen_width / 2 - (four_rect[2] / 2), 300))
            self.screen.blit(text_quit, (self.screen_width / 2 - (quit_rect[2] / 2), 360))
            pygame.display.update()
"""

# 카드 뒤집는 애니메이션 구현
"""
        # 타이머 설정
        tmr += 1
        if tmr == 90:
            tmr = 0
        # 타이머 계산도 다시
        txt = font.render(str(10 - tmr // 10 - 1), True, WHITE)
        screen.blit(txt, [400, 10])
        clock.tick(30)

        # 이거는 전환하는 거 확인하려고 만든거
        if tmr < 45:
            selected_img = pygame.image.load(CARD_IMAGE_LIST[-1])
            img_before = pygame.transform.scale(selected_img,
                                                [CARD_WIDTH * math.cos(math.radians(tmr * 2)), CARD_HEIGHT])
            img_before_rect = img_before.get_rect()
            screen.blit(img_before, [350 + tmr * 2 / 45 * 50, 200])
        else:
            up_img = pygame.image.load(uno_deck_dic[discards[-1]])
            img_after = pygame.transform.scale(up_img,
                                               [CARD_WIDTH * math.sin(math.radians(tmr * 2 - 90)), CARD_HEIGHT])
            img_after_rect = img_after.get_rect()
            # 와 계산은 나중에
            screen.blit(img_after, [450 + 20 - tmr * 2 / 45 * 10, 200])
"""


# 설정 화면
def setting_screen():
    game_exit = False

    # 배경음, 효과음 slider
    backgroundsound_slider = Slider(screen, 300, (250, 180), (0, 100))
    soundeffect_slider = Slider(screen, 300, (250, 250), (0, 100))

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            backgroundsound_slider.operate(event)
            soundeffect_slider.operate(event)

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

        screen.fill(WHITE)

        # 설정화면 텍스트 표시
        draw_text(screen, "설정 화면", (130, 50), 50)

        # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야 함
        draw_text(screen, "화면 설정", (130, 340), 20)

        # 화면 설정 버튼 - 변수명 바꿔야 함
        sizefull_button = Button(screen, 270, 315, 100, 50, "전체화면", 20, color=GRAY, hover_color=YELLOW,
                                 action=screen_size)
        size16_button = Button(screen, 420, 315, 100, 50, "16:9", 20, color=GRAY, hover_color=YELLOW,
                               action=setting_screen)
        size4_button = Button(screen, 570, 315, 100, 50, "4:3", 20, color=GRAY, hover_color=YELLOW, action=quit_game)

        # 배경음, 효과음 그림
        backgroundsound_slider.draw()
        backgroundsound_slider.draw_value('배경음', (130, 180))
        soundeffect_slider.draw()
        soundeffect_slider.draw_value('효과음', (130, 250))

        # 조작키 설정, 설정 초기화, 설정 저장 버튼
        control_button = Button(screen, 80, 400, 100, 50, "조작키 설정", 20, color=GRAY, hover_color=YELLOW,
                                action=game_screen)
        settinginit_button = Button(screen, 80, 500, 100, 50, "설정 초기화", 20, color=GRAY, hover_color=YELLOW,
                                    action=setting_screen)
        settingsave_button = Button(screen, SCREEN_WIDTH // 2 + 200, 500, 100, 50, "설정 저장", 20, color=GRAY,
                                    hover_color=YELLOW, action=quit_game)

        buttons = [control_button, settinginit_button, settingsave_button]

        pygame.display.update()


# 일시정지 함수
def pause():
    paused = True

    selected_button_index = 0

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭시 다시 시작
                paused = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_button_index >= 1:
                        selected_button_index = 0
                    else:
                        selected_button_index += 1
                elif event.key == pygame.K_UP:
                    if selected_button_index <= 0:
                        selected_button_index = 1
                    else:
                        selected_button_index -= 1
                elif event.key == pygame.K_RETURN:
                    buttons[selected_button_index].action()

        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 3 - 100, 400, 400))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 3 - 100, 400, 400), 5)

        setting_button = Button(screen, SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Settings", action=setting_screen)
        quit_button = Button(screen, SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Quit", action=quit_game)
        buttons = [setting_button, quit_button]

        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen, GRAY, buttons[selected_button_index].rect)

        # 여기 고쳐야해 text_surf, text_rect 이게 사라져서 안떠
        # screen.blit(buttons[selected_button_index].text_surf, buttons[selected_button_index].text_rect)
        screen.blit(buttons[selected_button_index].text_surf, buttons[selected_button_index].text_rect)

        draw_text(screen, "일시 정지", (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 3), 50)

        pygame.display.update()


if __name__ == '__main__':
    # uno = UNOGame()
    # uno.main_menu()
    uno = game()
    uno.set_deck()
    print(uno.card_deck)
    print(len(uno.card_deck)-76)
