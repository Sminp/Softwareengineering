import pygame
from game_functions import *
from constant import *
from settings import *
import math


# 시작 화면
def start_screen():
    start = True

    # 선택된 버튼의 인덱스 저장
    selected_button_index = 0

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # 방향키로 메뉴 선택 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_button_index >= 2:
                        selected_button_index = 0
                    else:
                        selected_button_index += 1
                elif event.key == pygame.K_UP:
                    if selected_button_index <= 0:
                        selected_button_index = 2
                    else:
                        selected_button_index -= 1
                elif event.key == pygame.K_RETURN:
                    buttons[selected_button_index].action()

        screen.fill(WHITE)

        # 게임 제목
        # 이미지....

        # 메뉴 버튼 생성 및 그리기
        single_player_button = Button(screen, SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Single Player",action=game_screen)
        setting_button = Button(screen, SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Settings", action=setting_screen)
        quit_button = Button(screen, SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Quit", action=quit_game)

        buttons = [single_player_button, setting_button, quit_button]

        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen, GRAY, buttons[selected_button_index].rect)

        # 여기 고쳐야해 text_surf, text_rect 이게 사라져서 안떠
        # screen.blit(buttons[selected_button_index].text_surf, buttons[selected_button_index].text_rect)
        screen.blit(buttons[selected_button_index].text_surf,buttons[selected_button_index].text_rect)

        pygame.display.update()


# 게임 화면
def game_screen():
    game_exit = False
    player_rect = [(10, 100 * j + (j + 1) * ((SCREEN_HEIGHT - 500) / 6), 180, 100) for j in range(5)]
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
    clicked = False
    tmr = 0

    # 카드 생성, 반환값 리스트
    uno_deck = build_deck()
    uno_deck_dic = make_dict(uno_deck, CARD_IMAGE_LIST)
    # uno_deck_dict는 순서가 없기에 list 따로 만든다.
    # 카드 무작위 셔플, 반환값 리스트
    uno_deck_li = shuffle_deck(uno_deck)
    # 게임 카드
    discards = []

    # 0 player, 1 ~ 5 computers
    players = draw_card(uno_deck_li, 5)
    # colors = ["Red", "Green", "Yellow", "Blue"]                       # 이건 왜 있지..?
    # 아마 2차 과제
    # num_players = int(input("player의 수를 입력하세요: "))
    # while num_players < 2 or num_players > 4:
    #     num_players = int(input("2~4 명의 player만 가능합니다. 다시 입력하세요:"))

    # 아마 인원수에 따라 바꿀 듯
    # for player in range(num_players):
    # for player in range(2):
    #     players.append(draw_card(uno_deck_li, 5))

    # 0 나, 1 컴퓨터 - 게임 차례
    player_turn = 0
    # reverse 방향 전환
    player_direction = 1
    playing = True
    discards.append(uno_deck_li.pop(0))

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                # 강제 종료
                if event.key == pygame.K_ESCAPE:
                    # 일시정지 함수 적기
                    pause()

        screen.fill(GREEN)
        for x in range(len(player_rect)):
            pygame.draw.rect(screen, WHITE, player_rect[x], width=0)

        for x in range(len(player_rect)):
            sur = font.render("player {}".format(x + 1), True, BLACK)
            screen.blit(sur, (player_rect[x][0], player_rect[x][1]))

        # 마우스 위치
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 마우스 누르는 버튼
        mBtn1, mBtn2, mBtn3 = pygame.mouse.get_pressed()

        # 이미지 올리기
        # 엎어져 있는 카드
        img_load(screen, CARD_IMAGE_LIST[-1], CARD_SIZE, [350, 200])
        # 게임 카드
        img_load(screen, uno_deck_dic[discards[-1]], CARD_SIZE, [350 + 100, 200])

        # 플레이어 카드
        for x in range(len(players)):
            img_load(screen, uno_deck_dic[players[x]], CARD_SIZE, [350 + (x - 1) * 100, 400])

        # 클래스로 다시 구현해야해 그래야 전환도 잘 되고 move도 잘해 아니면 함수가 너무 길어져
        # 클래스로 하면 우리 다시 얘기해야 해 리스트가 너무 많아져서 줄여야해 그래도 일단 보류

        # 타이머 설정
        tmr += 1
        if tmr == 90:
            tmr = 0
        # 타이머 계산도 다시
        txt = font.render(str(10-tmr // 10-1), True, WHITE)
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

        # 좌표 설정해서 노가다 - 이거 버튼으로 구현해도 되지 않을까? - 채령아 해줘... 헤줘.... 해줘.....
        if 350 <= mouse_x <= 350 + CARD_WIDTH and 400 <= mouse_y <= 400 + CARD_HEIGHT and mBtn1 == 1:
            clicked = True
        if clicked:
            pygame.draw.rect(screen, YELLOW, [50 - 2, 400 - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4], 4)
        if tmr % 10 == 0:
            clicked = False

        pygame.display.update()


# 설정 화면 
def setting_screen():
    game_exit = False

    # 배경음, 효과음 slider
    backgroundsound_slider = Slider(screen, 300, (250, 180), (0, 100))
    soundeffect_slider = Slider(screen, 300, (250, 250), (0, 100))

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            backgroundsound_slider.operate(event)
            soundeffect_slider.operate(event)

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


# 카드 객체 생성
class Cards:
    def __init__(self, screen, num, pos, filename, size=CARD_SIZE) -> None:
        self.screen = screen
        self.num = num
        self.filename = filename
        self.x, self.y = pos
        self.w, self.h = size
        self.img = pygame.image.load(filename)
        self.img_trans = pygame.transform.scale(self.img, size)

    def show(self):
        screen.blit(self.img_trans, self.pos)

    def move(self, moved):
        self.x += moved[0]
        self.y += moved[1]

    def flipping(self):
        pass


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
        screen.blit(buttons[selected_button_index].text_surf,buttons[selected_button_index].text_rect)

        draw_text(screen, "일시 정지", (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 3), 50)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    # 화면 설정
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UNO Game")
    start_screen()
