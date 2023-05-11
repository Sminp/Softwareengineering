import sys
import random
import pygame
import math
from loadcard import Card, Popup
import computer
from pygame.locals import *
from constant import *
from UNO import Button, text_format, terminate
from rect_functions import TextRect
from player import User, Computer, Waste
import time
from settings import Settings , resource_path



class Game():
    def __init__(self, player_num=2, difficulty=1, user_name="ME"):  # 초기값 임시로 설정 - 지우기
        # super().__init__()
        # self.uno = uno
        self.player_num = player_num
        self.difficulty = difficulty
        self.settings = Settings().get_setting()
        self.screen = pygame.display.set_mode((self.settings['screen']), flags=self.settings['fullscreen'])
        self.bg_img = pygame.transform.scale(pygame.image.load(resource_path("./image/playing_image/playing_background.png")), (self.settings['screen']))
        self.size = (self.settings['screen'])
        self.rotate = 0
        self.playing_game = True
        self.game_turn = 0
        self.time_limit = 10  # -> 시간 제한 설정
        self.time = 0
        self.active = False
        self.user_name = user_name
        self.first = True
        self.animation_group = None

        self.uno_button = Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                                 UNO_BUTTON, self.size[1] * (1 / 20),
                                 self.size[1] * (1 / 20))

        self.player = []
        self.card_deck = []
        self.waste = Waste()
        self.player_names = []

    # 카드 생성
    # TDD 가능
    def set_deck(self) -> list:
        card_deck = []
        for color_idx in range(1, 5):
            card = CARD_TYPE[color_idx]
            now_card = card + '_0'
            card_deck.append(now_card)
            for card_number in range(1, 10):
                now_card = card + "_" + str(card_number)
                iterate = 0
                while iterate != 2:
                    card_deck.append(now_card)
                    iterate += 1
        for color_idx in range(1, 5):
            card = CARD_TYPE[color_idx]
            for card_number in range(11, 14):
                now_card = card + CARD_SKILL[card_number]
                iterate = 0
                while iterate != 2:
                    card_deck.append(now_card)
                    iterate += 1
        # 짧게 바꿔도 됨
        card_deck.append("red_yellow")
        card_deck.append("red_yellow")
        card_deck.append("blue_green")
        card_deck.append("blue_green")
        card = 'wild'
        for card_number in range(14, 17):
            now_card = card + CARD_SKILL[card_number]
            iterate = 0
            while iterate != 4:
                card_deck.append(now_card)
                iterate += 1
        return card_deck

    # 객체 생성
    def player_init(self):
        for num in range(self.player_num):
            if num == 0:
                user = User()
                self.player.append(user)
            else:
                com = Computer(num)
                self.player.append(com)

    # 처음 카드 나눠준다 by 리스트
    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        for num in range(0, self.player_num):
            for number in range(0, 7):
                temp = self.card_deck.pop()
                self.player[num].append(temp)

    def set_name(self): # 이름이랑 위치 리스트로 저장하는거 어때?!
        player_names = []
        text = TextRect(self.screen, self.user_name, 30, WHITE)
        player_names.append([text , (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
        for i in range(1, self.player_num):
            text = TextRect(self.screen, "COM" + str(i), 20, BLACK)
            player_names.append([text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
        return player_names

    # 플레이어 이름 표시
    def show_name(self):
        for text, pos in self.player_names:
            text.change_color(BLACK)
            text.show(pos)

        pygame.display.update()

    # 함수를 나눠야 할 것 같아 test 만드는데 이 함수 돌릴 때 시간이 3초 넘게 걸려
    def set_window(self):
        self.card_deck = self.set_deck()
        self.player_init()
        self.hand_out_deck()
        self.waste.set_card()

        for i in range(self.player_num):
            self.player[i].set_card()
        setting = True

        settings = [1 for _ in range(self.player_num)] #

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            for num in range(self.player_num):
                settings[num] = self.player[num].set()

            # pygame.mixer.pre_init(44100, -16, 1, 512)
            # card = pygame.mixer.Sound('./sound/card.wav')
            # for i in range(0,7):
            #     card.play()
            if sum(settings) == 0:
                setting = False
                return 0
            self.print_window()
            pygame.display.update()
        
    # 플레이어 턴 인덱스 넘어가지 않도록 함
    def get_next_player(self, now_turn):
        self.first = True
        if self.rotate == 0 and now_turn + 1 == self.player_num:
            return 0
        elif self.rotate == 1 and now_turn - 1 < 0:
            return self.player_num - 1
        else:
            if self.rotate == 0:
                return now_turn + 1
            elif self.rotate == 1:
                return now_turn - 1
        return 0

    # 지금 현재 턴인 플레이어 표시 - print_window에 있어야 하지 않을까
    def show_now_turn(self, now_turn):

        for i, text in enumerate(self.player_names):
            if i == now_turn:
                text[0].change_color(YELLOW)
                text[0].show(text[1])
            else:
                text[0].change_color(BLACK)
                text[0].show(text[1])

        pygame.display.update()

    def print_computer_box(self) -> list:
        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.size[1] - 500) / 6), self.size[0] / 5,
                               self.size[1] / 6)
            computer_rect.append(rect)
        return computer_rect

    # 플레이어 이름 표시 초기화
    def print_window(self):
        # bg_img = self.uno.bg_img_load("./image/playing_image/playing_background.png")
        self.screen.blit(self.bg_img, (0, 0))
        for rect in self.print_computer_box():
            pygame.draw.rect(self.screen, WHITE, rect)
        self.waste.draw_group.draw(self.screen)
        for i in range(self.player_num):
            self.player[i].draw_group.draw(self.screen)
        self.uno_button.show()
        self.show_now_turn(self.now_turn)
        self.waste.draw_group.draw(self.screen)
        self.draw_color_rect()
        if self.animation_group:
            self.animation_group.draw(self.screen)
        
    def draw_color_rect(self):
        rect_pos = (self.size[0] * (3 / 4), self.size[1] * (1 / 3) - self.size[1] * (1 / 20))
        rect_size = (self.size[1] * (1 / 20), self.size[1] * (1 / 20))
        half_rect_pos = (self.size[0] * (3 / 4) + self.size[1] * (1 / 40), self.size[1] * (1 / 3) - self.size[1] * (1 / 20))
        half_rect_size = (self.size[1] * (1 / 40), self.size[1] * (1 / 20))

        if len(self.waste.card) == 0:
            pygame.draw.rect(self.screen, BLACK, (rect_pos, rect_size))
        else:
            w_name = self.waste.card[-1]
            w_name = w_name.split('_')
            if w_name[0] == 'wild':
                pygame.draw.rect(self.screen, BLACK, (rect_pos, rect_size))
            elif w_name[0] == "red":
                if len(w_name) > 1:
                    if w_name[1] == 'yellow':
                        pygame.draw.rect(self.screen, RED, (rect_pos, half_rect_size))
                        pygame.draw.rect(self.screen, YELLOW, (half_rect_pos, half_rect_size))
                    else:
                        pygame.draw.rect(self.screen, RED, (rect_pos, rect_size))
                else:
                    pygame.draw.rect(self.screen, RED, (rect_pos, rect_size))
            elif w_name[0] == "yellow":
                pygame.draw.rect(self.screen, YELLOW, (rect_pos, rect_size))
            elif w_name[0] == "blue":
                if len(w_name) > 1:
                    if w_name[1] == 'green':
                        pygame.draw.rect(self.screen, BLUE, (rect_pos, half_rect_size))
                        pygame.draw.rect(self.screen, GREEN, (half_rect_pos, half_rect_size))
                    else:
                        pygame.draw.rect(self.screen, BLUE, (rect_pos, rect_size))
                else:
                    pygame.draw.rect(self.screen, BLUE, (rect_pos, rect_size))
            elif w_name[0] == "green":
                pygame.draw.rect(self.screen, GREEN, (rect_pos, rect_size))

    # 낼 수 있는지 확인
    def check_card(self, sprite):
        if len(self.waste.card) == 0:
            return True
        else:
            name = sprite.get_name()
            name = name.split('_')
            w_name = self.waste.card[-1]
            w_name = w_name.split('_')
            if self.difficulty == 5:
                if w_name[1] != '0' and name[1] != '0':
                    if (int(w_name[1]) % int(name[1])) == 0 or (int(name[1]) % int(w_name[1])) == 0:
                        return True
                else:
                    return True

            else:
                if w_name[0] == 'wild':
                    return True
                if name[0] == 'wild':
                    return True
                if len(name) < 3 or len(w_name) < 3:
                    if w_name[0] == name[0]:
                        return True
                    if len(name) > 1:
                        if len(w_name) < 2:  # 여기 수정 해야함
                            if w_name[0] == name[0] or w_name[0] == name[1]:
                                return True
                        else:
                            if w_name[1] == name[1]:
                                return True
                            if w_name[1] == name[0] or w_name[0] == name[1]:
                                return True
                else:
                    if w_name[0] == name[0]:
                        return True
                    if w_name[2] == name[2]:
                        return True
        return False

    def pick_color_card(self):
        if self.now_turn == 0:
            temp = self.pick_color()
        else:
            pygame.time.wait(500)
            temp = self.player[self.now_turn].most_num_color()
        self.waste.updating(temp)
        self.print_window()

    def pick_color(self):
        # 뒤에 이미지 -> 빼거나 대체
        red = Popup('red', (306, 320))
        yellow = Popup('yellow', (368, 320))
        green = Popup('green', (432, 320))
        blue = Popup('blue', (494, 320))
        colors = [red, yellow, green, blue]
        color_group = pygame.sprite.RenderPlain(*colors)

        loop = True
        while loop:
            # popup_group.draw(self.screen)
            color_group.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in color_group:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            temp_name = sprite.get_name()
                            self.print_window()
                            loop = False
        return temp_name
    

# card_skill 중 card change 함수
    def card_change(self, now_turn, pick_turn):
        # 현재 턴의 플레이어 덱 임시 저장
        temp_player = self.player[now_turn].card
        # 현재 턴의 플레이어 리스트 초기화
        self.player[now_turn].clear()
        for item in self.player[pick_turn].card:
                self.player[now_turn].add_card(item)
        # 목표 플레이어 덱 초기화
        self.player[pick_turn].clear()
        for item in temp_player:
                self.player[pick_turn].add_card(item)

        self.print_window()

    # 수정중
    # 기능 카드 수행
    # if name[0] 해서 기능 추가
    def card_skill(self, name):
        name = name.split('_')
        if name[1] == 'pass':
            pygame.time.wait(500)
            self.now_turn = self.get_next_player(self.now_turn)
        elif name[1] == 'reverse':
            if self.player_num == 2:
                pygame.time.wait(500)
                self.now_turn = self.get_next_player(self.now_turn)
            else:
                if self.rotate == 0:
                    self.rotate = 1
                else:
                    self.rotate = 0
        elif name[1] == 'change':  # change 구현   - 지금 상태 바뀌기는 하는데 화면에 카드 표시가 안뜸
            if self.now_turn == 0:
                index = self.pick_player()
                self.card_change(self.now_turn, index)
            else:
                index = self.least_num(self.now_turn)
                self.card_change(self.now_turn, index)
            self.print_window()

        elif name[1] == 'plus':
            if name[2] == 'two':
                pygame.time.wait(500)
                if len(self.card_deck) < 2:
                    pass
                else:
                    self.give_card(2)
                # self.now_turn = self.get_next_player(self.now_turn)
            elif name[2] == 'four':
                # pygame.mixer.pre_init(44100, -16, 1, 512)
                # select = pygame.mixer.Sound('./sound/select.wav')
                # select.play()
                if len(self.card_deck) < 4:
                    pass
                else:
                    self.give_card(4)
                self.pick_color_card()
        elif name[0] == 'wild':
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            # select = pygame.mixer.Sound('./sound/select.wav')
            # select.play()
            self.pick_color_card()

    def pick_player(self):

        pick_player_button = []
        for i in range(1, self.player_num):
            image_name = "./image/playing_image/deckchange_player" + \
                         str(i) + ".jpg"
            # 이거 약간 애매해 - 밖으로 꺼내자.
            temp_button = Button(self.screen, self.settings['screen'][0] * (1 / 2), self.settings['screen'][1] / 6 * i, image_name,
                                 self.settings['screen'][0] * (1 / 8), self.settings['screen'][1] * (1 / 9))
            pick_player_button.append(temp_button)
        index = 0

        loop = True
        while loop:
            for i in range(self.player_num - 1):
                pick_player_button[i].show()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(self.player_num - 1):
                        if pick_player_button[i].get_rect().collidepoint(event.pos):
                            # 수정중
                            return i + 1
                            # loop = False

        return index + 1
    
    # 가장 적은 숫자 카드 나타내는 함수
    def least_num(self, my_index) -> int:
        least_player_idx = 0
        least_player_num = len(self.player[0].card)
        for num in range(1, self.player_num):
            if least_player_num > len(self.player[num].card):
                if num != my_index:
                    least_player_idx = num
                    least_player_num = len(self.player[num].card)
        return least_player_idx
    
    # 다음 차례 플레이어에게 카드 뽑게 함 -> draw 카드
    def give_card(self, card_num):
        if len(self.waste.card) == 1:  # 처음 카드가 +2,+4일때 처음 플레이어가 카드 받음
            dest_player = self.now_turn
        else:
            dest_player = self.get_next_player(self.now_turn)
        for i in range(0, card_num):
            self.get_from_deck(dest_player)

    # 게임 끝난 화면, 스페이스 버튼 누르면 다시 시작
    def restart(self):
        # pygame.mixer.pre_init(44100, -16, 1, 512)
        # win = pygame.mixer.Sound('./sound/win.wav')
        # lose = pygame.mixer.Sound('./sound/lose.wav')
        pygame.draw.rect(self.screen, (255, 51, 0),
                         pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(self.screen, (255, 180, 0),
                         pygame.Rect(210, 210, 380, 180))

        for i in range(self.player_num):
            if len(self.player[i].group) == 0 :
                if i == 0:
                    close_text = text_format("YOU WIN!", BERLIN, 80, (255, 51, 0))
                    press_text = text_format(
                        "Press SPACE to REPLAY", BERLIN, 35, (255, 51, 0))
                    self.screen.blit(close_text, (230, 220))
                else: 
                    close_text = text_format("YOU LOSE!, com{} win!".format(i), BERLIN, 40, (255, 51, 0))
                    press_text = text_format(
                        "Press SPACE to REPLAY", BERLIN, 35, (255, 51, 0))
                    self.screen.blit(close_text, (230, 220))

        self.screen.blit(press_text, (228, 330))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.uno_game.main_menu()
                        # 객체를 생성해서 호출하는게 좋지않을까?
                        return
        return 0

    # 이거 합쳐서 다시 리팩토링 (지울 예정)
    def no_temp(self, now_turn: int):
        self.get_from_deck(now_turn)
        self.print_window()
        self.now_turn = self.get_next_player(self.now_turn)
        pygame.display.update()

    # 타이머 클래스로 만들 예정 (지울 예정)
    def timer(self) -> bool:
        total_time = 10
        start_ticks = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer_msg = text_format(elapsed_time, MALGUNGOTHIC, 10, WHITE)
        self.screen.blit(timer_msg, (self.size[0] *
                                     (1 / 4), self.size[1] * (1 / 7)))
        if total_time <= elapsed_time:
            return False

    # 리팩토링 match로 해도 될 것 같아
    def check_player(self):
        
        for i in range(self.player_num):
            if len(self.player[i].card) == 0:
                self.restart()

        # if len(self.player[0].card) == 0:
        #     self.restart()
        #     return
        # elif self.player_num == 6:
        #     if len(self.player[1].card) == 0 or len(self.player[2].card) == 0 or len(
        #             self.player[3].card) == 0 or len(
        #         self.player[4].card) == 0 or len(self.player[5].card) == 0:
        #         self.restart()
        #         return
        # elif self.player_num == 5:
        #     if len(self.player[1].card) == 0 or len(self.player[2].card) == 0 or len(
        #             self.player[3].card) == 0 or len(self.player[4].card) == 0:
        #         self.restart()
        #         return
        # elif self.player_num == 4:
        #     if len(self.player[1].card) == 0 or len(self.player[2].card) == 0 or len(self.player[3].card) == 0:
        #         self.restart()
        #         return
        # elif self.player_num == 3:
        #     if len(self.player[1].card) == 0 or len(self.player[2].card) == 0:
        #         self.restart()
        #         return
        # elif self.player_num == 2:
        #     if len(self.player[1].card) == 0:
        #         self.restart()
        #         return

    def selected_turn(self):
        return random.randint(0, self.player_num -1)

    def computer_play(self):
        ai = computer.AI(self.now_turn + 1, self.player[self.now_turn].card, self.waste.card)
        temp = ai.basic_play()

        if temp == 0 or temp is None:
            self.no_temp(self.now_turn)
        else:
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            # card = pygame.mixer.Sound('./sound/deal_card.wav')

            # 수정중
            self.player[self.now_turn].remove(temp)
            self.player[self.now_turn].set_lastcard()

            # card.play()
            self.waste.updating(temp)
            self.print_window()
            pygame.display.update()
            self.card_skill(temp)
            if len(self.player[self.now_turn].group) == 1:
                pygame.display.update()
                self.check_uno_button()
            else:
                self.print_window()
                self.now_turn = self.get_next_player(self.now_turn)
            pygame.display.update()

    # 게임 시작 (다시 시작 )
    def startgame(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.card_deck.clear()
        self.player = []
        self.player_names = self.set_name()
        self.rotate = 0
        self.now_turn = self.selected_turn()
        self.set_window()
        # self.show_name()
        self.playgame()

    # 수정중
    # 게임 구현
    def playgame(self):
        tmr = 0
        selected = 0
        selected_up = 0

        while self.playing_game:
            self.check_player()
            if len(self.card_deck) == 0:
                self.set_deck()

            if len(self.waste.card) == 0:
                temp = self.card_deck.pop()
                self.waste.updating(temp)
                self.card_skill(temp)
                self.print_window()
                pygame.display.update()

            pygame.time.wait(2000)

            if self.now_turn != 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                self.computer_play()
            else:
                self.user_play()

            self.print_window()
            pygame.display.update()

    def user_play(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    # if event.key == K_ESCAPE:
                    #     return
                    if event.key == K_ESCAPE:
                        self.pause()
                        self.print_window()
                    if event.key == K_LEFT:
                        if selected <= 0:
                            selected = 0
                        else:
                            selected = selected - 1
                    elif event.key == K_RIGHT:
                        if selected >= len(self.player[0]) - 1:
                            selected = len(self.player[0]) - 1
                        else:
                            selected = selected + 1
                    elif event.key == K_UP:
                        if selected_up == 0:
                            selected_up = 1
                        else:
                            selected_up = 1
                    elif event.key == K_DOWN:
                        if selected_up == 1:
                            selected_up = 0
                        else:
                            selected_up = 0

                    if event.key == K_RETURN:
                        if selected_up == 1:
                            self.get_from_deck(self.now_turn)
                            self.now_turn = self.get_next_player(self.now_turn)
                            break
                        else:
                            for sprite in self.player[0].group:
                                if sprite.get_name() == self.player[0].card[selected] and self.check_card(sprite):
                                    # 수정중
                                    self.player[0].remove(sprite)
                                    for temp in self.player[0].group:
                                        temp.move(sprite.getposition())
                                    sprite.setposition(self.size[0] * (3 / 5), self.size[1] * (1 / 3))
                                    self.waste.updating(sprite.get_name())
                                    # 수정중
                                    self.card_skill(sprite.get_name())
                                    if len(self.player[0].group) == 1:  # 카드 내고 한장 남음
                                        pygame.display.update()
                                        self.check_uno_button()
                                    else:
                                        self.now_turn = self.get_next_player(self.now_turn)
                                    if selected > len(self.player[0]) - 1:
                                        selected = len(self.player[0]) - 1
                                    break
                if event.type == MOUSEBUTTONUP:
                    self.select_sound = pygame.mixer.Sound('./sound/card_sound.mp3')
                    self.select_sound.play()
                    if self.now_turn == 0:
                        # self.show_now_turn(self.now_turn)
                        for sprite in self.player[0].group:
                            if sprite.get_rect().collidepoint(event.pos) and self.check_card(sprite):
                                # pygame.mixer.pre_init(44100, -16, 1, 512)
                                # card = pygame.mixer.Sound('./sound/deal_card.wav')
                                self.player[0].remove(sprite)
                                # card.play()
                                self.waste.updating(sprite.get_name())
                                # 수정중
                                self.card_skill(sprite.get_name())
                                if len(self.player[0].group) == 1:  # 카드 내고 한장 남음
                                    pygame.display.update()
                                    self.check_uno_button()
                                else:
                                    self.now_turn = self.get_next_player(self.now_turn)
                                break
                        for sprite in self.waste.group:
                            if sprite.get_rect().collidepoint(event.pos):
                                self.get_from_deck(self.now_turn)
                                # self.show_uno()
                                self.now_turn = self.get_next_player(self.now_turn)
                                break

    # 수정중
    # 카드 뽑음
    def get_from_deck(self, now_turn):
        # pygame.mixer.pre_init(44100, -16, 1, 512)
        # deck = pygame.mixer.Sound('./sound/from_deck.wav')
        if self.card_deck:
            item = self.card_deck.pop()
        else:
            random.shuffle(self.waste.card)
            self.card_deck = self.waste.card[:-1]
            item = self.card_deck.pop()

        # 애니메이션 
        # animation = True
        # while animation:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             terminate()
        #     card = Card('back', (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.player[self.now_turn].card_size)
        #     card.animation((self.player[self.now_turn].get_lastcard()))
        #     self.animation_group = pygame.sprite.RenderPlain(card)
        #     if not self.animation_group:
        #         animation = False
        #     self.print_window()
        #     pygame.display.update()

        self.player[now_turn].add_card(item)
        self.print_window()

    def pause(self):

        paused = True
        self.playing_game = False

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭시 다시 시작
                    self.playing_game = True
                    paused = False
                    if setting_button.get_rect().collidepoint(event.pos):
                        pass
                    elif exit_button.get_rect().collidepoint(event.pos):
                        terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing_game = True
                        paused = False

            pygame.draw.rect(self.screen, WHITE, (self.size[0] /
                                                  2 - 200, self.size[1] / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, BLACK, (self.size[0] / 2 - 200, self.size[1] / 3 - 100, 400, 400),
                             5)
            close_text = text_format("PAUSE", MALGUNGOTHIC, 60, BLACK)
            close_text_rect = close_text.get_rect(
                center=(self.size[0] / 2, self.size[1] / 3))
            setting_button = Button(self.screen, self.size[0] * (3 / 7), self.size[1] * (2 / 5),
                                    "./image/button_img.png", 200, 100)
            exit_button = Button(self.screen, self.size[0] * (3 / 7), self.size[1] * (2 / 5) + 100,
                                 "./image/button_img.png", 200, 100)
            setting_button.show_button()
            exit_button.show_button()
            self.screen.blit(close_text, close_text_rect)

            pygame.display.update()

    def check_uno_button(self):
        self.print_window()
        print("한장 남음!")
        uno = True
        start_time = time.time()
        while uno:  # 여기
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONUP or event.type == KEYDOWN:
                    if self.uno_button.get_rect().collidepoint(event.pos) or event.type == K_SPACE:
                        print("버튼 누름!")
                        end_time = time.time()
                        com_time = random.randint(1, 3)
                        if (end_time - start_time) > com_time:
                            if self.now_turn == 0:  # 유저 턴일 때
                                print("느리게 누름!")
                                uno_text = text_format(
                                    "uno", BERLIN, 30, (0, 0, 0))
                                self.screen.blit(uno_text, (45, 100))
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.get_next_player(self.now_turn)
                                uno = False
                            else:  # 컴퓨터 턴일때 유저가 느리게 누름
                                print("유저가 느리게 누름")
                                self.now_turn = self.get_next_player(self.now_turn)
                                uno = False
                        else:
                            if self.now_turn == 0:  # 유저 턴일 때
                                print("빠르게 누름!")
                                self.now_turn = self.get_next_player(self.now_turn)
                                uno = False
                            else:  # 컴퓨터 턴일 때 유저가 빠르게 누름
                                print("유저가 빠르게 누름!")
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.get_next_player(self.now_turn)
                                uno = False
            if (time.time() - start_time) > 3:
                if self.now_turn == 0:  # 그냥 버튼 안누르고 있을 때 5초 지나면 한 장 먹음
                    print("컴퓨터가 누름")
                    self.get_from_deck(self.now_turn)
                    self.now_turn = self.get_next_player(self.now_turn)
                    uno = False
                else:  # 이건 컴퓨터가 1장 남았을 때 유저가 버튼을 안 누르고 있는 경우
                    if self.player_num == 2:  # 유저랑 컴퓨터 1명만 있는 경우 컴퓨터가 uno버튼 누른걸로 판단
                        print("컴퓨터가 누름")
                        self.now_turn = self.get_next_player(self.now_turn)
                        uno = False
                    else:  # 다른 컴퓨터랑 경쟁
                        com_time = random.randint(0, 1)  # 그냥 0,1로 했어요..
                        if com_time == 1:  # 빠르게 누른 경우
                            print("컴퓨터가 누름")
                            self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
                        else:  # 느리게 누른 경우 - 카드 뽑음
                            print("컴퓨터가 못 누름")
                            self.get_from_deck(self.now_turn)
                            self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
            pygame.display.update()


class GameA(Game):
    def __init__(self):
        super().__init__()
        pass

    def difficulty_two_deck(self):
        num_card = self.card_deck[:76]
        skill_card = self.card_deck[76:]
        random.shuffle(num_card)
        random.shuffle(skill_card)
        for player in range(1, self.player_num):
            card = []
            for _ in range(0, 7):
                if random.random() < 76 / 164:
                    temp = num_card.pop()
                else:
                    temp = skill_card.pop()
                card.append(temp)
            self.player[player] = card
        card_deck = num_card + skill_card
        del num_card, skill_card
        return card_deck

    def hand_out_deck(self):
        self.card_deck = self.difficulty_two_deck()
        random.shuffle(self.card_deck)
        card = []
        for _ in range(7):
            temp = self.card_deck.pop()
            card.append(temp)
        self.player[0] = card

    def playgame(self):

        while True:

            next = self.get_next_player(self.now_turn)

            if next == 0:
                next_ = self.player[0].group
            else:
                next_ = self.player[next]

            temp = ai.advanced_play(next_)

            if self.difficulty == 2 and self.card_skill(temp):
                self.print_window()
                pygame.display.update()
                continue


class GameB(Game):
    def __init__(self):
        super().__init__()
        pass

    def hand_out_deck(self):
        i = len(self.card_deck) // self.player_num
        random.shuffle(self.card_deck)
        card_temp = self.card_deck.pop()  # 첫번째 카드 미리 뽑아두기
        for player in range(0, self.player_num):
            card = []
            for number in range(0, i):  # 모든 카드 같은 수 만큼 플레이어에게 분배
                if self.card_deck:
                    temp = self.card_deck.pop()
                card.append(temp)
            self.player[player] = card
        self.card_deck.append(card_temp)

    def set_player(self):
        i = 0
        temp_list = []
        j = 0
        k = 0
        for item in self.player[0]:
            if 7 <= i < 14:
                item.update((self.size[0] * (1 / 3) + 80 * j,
                             self.size[1] * (7 / 9) + self.size[1] / 10))
                temp_list.append(item)
                j += 1
                i += 1
            elif i >= 14:
                item.update((self.size[0] * (1 / 3) + 80 * k,
                             self.size[1] * (7 / 9) + self.size[1] * 2 / 10))
                temp_list.append(item)
                k += 1
                i += 1
            else:
                item.update((self.size[0] * (1 / 3) + 80 *
                             i, self.size[1] * (7 / 9)))
                temp_list.append(item)
                i += 1
        self.player[0].group = pygame.sprite.RenderPlain(*temp_list)
        if temp_list:
            self.player_group[0][-1] = temp_list[-1].getposition()
        if self.player_group[0][-1] == (
                self.size[0] * (1 / 3) + 80 * (len(temp_list) % 7 - 1),
                self.size[1] * (7 / 9) + self.size[1] * 2 / 10):
            setting_user = 0

    def set_computer(self, player_num):
        i = 0
        temp_list = []
        setting = True
        for num in range(1, player_num):
            j = 0
            for item in self.player[num]:
                if i >= 12:
                    item.update((self.size[0] * (1 / 30) + 10 * j,
                                 self.size[1] * (2 * num - 1 / 10) + self.size[1] * (1 / 30)))
                    j += 1
                    i += 1
                    temp_list.append(item)
                else:
                    item.update((self.size[0] * (1 / 30) + 10 * i,
                                 self.size[1] * (2 * num - 1 / 10)))
                    temp_list.append(item)
                    i += 1
            self.computer_group[num] = pygame.sprite.RenderPlain(*temp_list)
            if temp_list:
                self.computer_group[num][-1] = temp_list[-1].getposition()
            if self.computer_group[num][-1] == (
                    self.size[0] * (1 / 30) + 10 *
                    (len(temp_list) % 12 - 1),
                    self.size[1] * (2 * num - 1 / 10) + self.size[1] * (1 / 30)):
                setting_com1 = 0  # 얘만 고치면 돼
                """이거 버그 때문에 이렇게 설정했는데 이렇게 하니까 3초가 넘어서 일단은 한번만 하기로 했어 그리고 수정하자."""

    def playgame(self):

        while True:
            temp = ai.basic_play()


class GameC(Game):
    def __init__(self):
        super().__init__()
        pass

    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        self.player_num = 2
        for player in range(0, self.player_num):
            card = []
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                card.append(temp)
            self.player[player] = card

    # 지역 C
    def get_next_turn(self):
        if self.first:
            self.game_turn += 1
            self.change_color()
            pygame.time.wait(1000)
            print("turn", self.game_turn)
            self.first = False

    # 지역 C

    def change_color(self):
        if self.difficulty == 4 and self.game_turn % 5 == 0 and self.game_turn != 0:
            print("실행")
            colors = ["red", "yellow", "green", "blue"]
            random_name = colors[random.randint(0, 3)]
            random_card = Card(random_name, (self.size[0] * (3 / 5), self.size[1] * (1 / 3)),
                               (self.size[0] / 10, self.size[1] / 6))
            # 수정 중
            self.waste.card.append(random_name)
            self.waste.group.append(random_card)
            self.waste.draw_group.add()
            print("바뀐 색:" + random_name)
            self.print_window()

    def playgame(self):

        while True:
            self.get_next_turn()

            temp = ai.basic_play()


class GameD(Game):
    def __init__(self):
        super().__init__()
        pass

    def set_deck(self):
        card_deck = []
        for color_idx in range(1, 5):
            card = CARD_TYPE[color_idx]
            now_card = card + '_0'
            card_deck.append(now_card)
            for card_number in range(1, 10):
                now_card = card + "_" + str(card_number)
                iterate = 0
                while iterate != 2:
                    card_deck.append(now_card)
                    iterate += 1
        return card_deck

    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        self.player_num = 3
        for player in range(0, self.player_num):
            card = []
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                card.append(temp)
            self.player[player] = card

    def playgame(self):

        while True:
            temp = ai.special_play()
