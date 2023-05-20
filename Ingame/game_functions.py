import sys
import random
import pygame
from loadcard import Card, Popup
import computer
from pygame.locals import *
import constant as c
import player as pl
import settings as s
import computer as com
import loadcard as lc
import rect_functions as rf
import timer
import time
import math


class Game():
    def __init__(self, player_num=2, difficulty=1, user_name="ME"):  # 초기값 임시로 설정 - 지우기
        self.player_num = player_num
        self.difficulty = difficulty
        self.setting = s.Settings()
        self.settings = self.setting.get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        self.bg_img = pygame.transform.scale(pygame.image.load(s.resource_path(
            c.GAME_BACKGROUND)), (self.settings['screen']))
        self.size = (self.settings['screen'])
        self.rotate = 0
        self.playing_game = True
        self.game_turn = 0
        self.time_limit = 10  # -> 시간 제한 설정
        self.time = 0
        self.active = False
        self.user_name = user_name
        self.first = True
        self.now_turn = None
        self.animate_card = None
        self.animation_group = None

        self.uno_button = rf.Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                                    c.UNO_BUTTON, self.size[1] * (1 / 20),
                                    self.size[1] * (1 / 20))

        pygame.init()
        self.timer = timer.Timer()

        self.player = []
        self.card_deck = []
        self.waste = pl.Waste()
        self.player_names = []

    # 카드 생성
    def set_deck(self) -> list:
        card_deck = []
        for color_idx in range(1, 5):
            card = c.CARD_TYPE[color_idx]
            now_card = card + '_0'
            card_deck.append(now_card)
            for card_number in range(1, 10):
                now_card = card + "_" + str(card_number)
                iterate = 0
                while iterate != 2:
                    card_deck.append(now_card)
                    iterate += 1
        for color_idx in range(1, 5):
            card = c.CARD_TYPE[color_idx]
            for card_number in range(11, 14):
                now_card = card + c.CARD_SKILL[card_number]
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
            now_card = card + c.CARD_SKILL[card_number]
            iterate = 0
            while iterate != 4:
                card_deck.append(now_card)
                iterate += 1
        return card_deck

    # 객체 생성
    def player_init(self):
        for num in range(self.player_num):
            if num == 0:
                user = pl.User()
                self.player.append(user)
            else:
                computer = pl.Computer(num)
                self.player.append(computer)

    # 처음 카드 나눠준다 by 리스트
    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        for num in range(0, self.player_num):
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                self.player[num].append(temp)

    def set_name(self):  # 이름이랑 위치 리스트로 저장하는거 어때?! - 이거 json파일로 하면 훨씬 편해.
        player_names = []
        text = rf.TextRect(self.screen, self.user_name, 30, c.WHITE)
        player_names.append(
            [text, (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
        for i in range(1, self.player_num):
            text = rf.TextRect(self.screen, "COM" + str(i), 20, c.BLACK)
            player_names.append(
                [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
        return player_names

    # 플레이어 이름 표시
    def show_name(self):
        for text, pos in self.player_names:
            text.change_color(c.BLACK)
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

        settings = [1 for _ in range(self.player_num)]

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
        self.timer.reset_tmr()
        self.first = True
        if self.rotate == 0 and now_turn + 1 == self.player_num:
            turn = 0
        elif self.rotate == 1 and now_turn - 1 < 0:
            turn = self.player_num - 1
        else:
            if self.rotate == 0:
                turn = now_turn + 1
            elif self.rotate == 1:
                turn = now_turn - 1
        print("turn : ", turn)
        return turn

    # 지금 현재 턴인 플레이어 표시
    def show_now_turn(self, now_turn):

        for i, text in enumerate(self.player_names):
            if i == now_turn:
                text[0].change_color(c.YELLOW)
                text[0].show(text[1])
            else:
                text[0].change_color(c.BLACK)
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
        self.screen.blit(self.bg_img, (0, 0))
        self.draw_color_rect()
        self.timer.show_tmr(self.now_turn)
        for rect in self.print_computer_box():
            pygame.draw.rect(self.screen, c.WHITE, rect)
        if self.animation_group:
            self.animation_group.draw(self.screen)
        self.waste.draw_group.draw(self.screen)
        for i in range(self.player_num):
            self.player[i].draw_group.draw(self.screen)
        if self.animation_group:
            self.animation_group.draw(self.screen)
            self.animation_group = None
        self.uno_button.show()
        self.show_now_turn(self.now_turn)

    def draw_color_rect(self):
        rect_pos = (self.size[0] * (3 / 4), self.size[1]
                    * (1 / 3) - self.size[1] * (1 / 20))
        rect_size = (self.size[1] * (1 / 20), self.size[1] * (1 / 20))
        half_rect_pos = (self.size[0] * (3 / 4) + self.size[1] *
                         (1 / 40), self.size[1] * (1 / 3) - self.size[1] * (1 / 20))
        half_rect_size = (self.size[1] * (1 / 40), self.size[1] * (1 / 20))

        if len(self.waste.card) == 0:
            pygame.draw.rect(self.screen, c.BLACK, (rect_pos, rect_size))
        else:
            w_name = self.waste.card[-1]
            w_name = w_name.split('_')
            if w_name[0] == 'wild':
                pygame.draw.rect(self.screen, c.BLACK, (rect_pos, rect_size))
            elif w_name[0] == "red":
                if len(w_name) > 1:
                    if w_name[1] == 'yellow':
                        pygame.draw.rect(self.screen, c.RED,
                                         (rect_pos, half_rect_size))
                        pygame.draw.rect(self.screen, c.YELLOW,
                                         (half_rect_pos, half_rect_size))
                    else:
                        pygame.draw.rect(self.screen, c.RED,
                                         (rect_pos, rect_size))
                else:
                    pygame.draw.rect(self.screen, c.RED, (rect_pos, rect_size))
            elif w_name[0] == "yellow":
                pygame.draw.rect(self.screen, c.YELLOW, (rect_pos, rect_size))
            elif w_name[0] == "blue":
                if len(w_name) > 1:
                    if w_name[1] == 'green':
                        pygame.draw.rect(self.screen, c.BLUE,
                                         (rect_pos, half_rect_size))
                        pygame.draw.rect(self.screen, c.GREEN,
                                         (half_rect_pos, half_rect_size))
                    else:
                        pygame.draw.rect(self.screen, c.BLUE,
                                         (rect_pos, rect_size))
                else:
                    pygame.draw.rect(self.screen, c.BLUE,
                                     (rect_pos, rect_size))
            elif w_name[0] == "green":
                pygame.draw.rect(self.screen, c.GREEN, (rect_pos, rect_size))

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
        red = lc.Popup('red', (306, 320))
        yellow = lc.Popup('yellow', (368, 320))
        green = lc.Popup('green', (432, 320))
        blue = lc.Popup('blue', (494, 320))
        colors = [red, yellow, green, blue]
        color_group = pygame.sprite.RenderPlain(*colors)

        loop = True
        while loop:
            # popup_group.draw(self.screen)
            color_group.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
            self.first = False
        elif name[1] == 'reverse':
            if self.player_num == 2:
                pygame.time.wait(500)
                self.now_turn = self.get_next_player(self.now_turn)
                self.first = False
            else:
                if self.rotate == 0:
                    self.rotate = 1
                else:
                    self.rotate = 0
        elif name[1] == 'change':
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
                # if self.player_num == 2:
                #     self.now_turn = self.get_next_player(self.now_turn)
                #     self.first = False
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
            temp_button = rf.Button(self.screen, self.settings['screen'][0] * (1 / 2),
                                    self.settings['screen'][1] /
                                    6 * i, image_name,
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
                    pygame.quit()
                    sys.exit()
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

    # t.text_format 함수 없애야 함
    def restart(self):
        pass
        # # pygame.mixer.pre_init(44100, -16, 1, 512)
        # # win = pygame.mixer.Sound('./sound/win.wav')
        # # lose = pygame.mixer.Sound('./sound/lose.wav')
        # pygame.draw.rect(self.screen, (255, 51, 0),
        #                  pygame.Rect(200, 200, 400, 200))
        # pygame.draw.rect(self.screen, (255, 180, 0),
        #                  pygame.Rect(210, 210, 380, 180))

        # for i in range(self.player_num):
        #     if len(self.player[i].group) == 0:
        #         if i == 0:
        #             close_text = t.text_format(
        #                 "YOU WIN!", c.BERLIN, 80, (255, 51, 0))
        #             press_text = t.text_format(
        #                 "Press SPACE to REPLAY", c.BERLIN, 35, (255, 51, 0))
        #             self.screen.blit(close_text, (230, 220))
        #         else:
        #             close_text = t.text_format(
        #                 "YOU LOSE!, com{} win!".format(i), c.BERLIN, 40, (255, 51, 0))
        #             press_text = t.text_format(
        #                 "Press SPACE to REPLAY", c.BERLIN, 35, (255, 51, 0))
        #             self.screen.blit(close_text, (230, 220))

        # self.screen.blit(press_text, (228, 330))
        # pygame.display.update()
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             t.terminate()

        #         if event.type == KEYDOWN:
        #             if event.key == K_SPACE:
        #                 self.playing_game = False
        #                 # 객체를 생성해서 호출하는게 좋지않을까? - 객체를 미리 생성하고 어떤 곳은 dictionary로 가더라 이것도 좋아
        #                 # 그리고 객체를 생성하면 업적이 망가지지 않을까?
        #                 return
        # return 0

    # 리팩토링 match로 해도 될 것 같아
    def check_player(self):

        for i in range(self.player_num):
            if len(self.player[i].card) == 0:
                self.restart()

    def selected_turn(self):
        return random.randint(0, self.player_num - 1)

    def difficulty_play(self):
        ai = com.AI(self.now_turn + 1,
                    self.player[self.now_turn].card, self.waste.card)
        if self.difficulty in (1, 2, 3, 4):
            return ai.basic_play()
        else:
            return ai.special_play()

    def computer_play(self):
        temp = self.difficulty_play()
        pygame.time.wait(1000)

        if temp == 0 or temp is None:
            self.get_from_deck(self.now_turn)
            # self.print_window()
            # pygame.display.update()
            return 'Back'
            # self.now_turn = self.get_next_player(self.now_turn)
        else:
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            # card = pygame.mixer.Sound('./sound/deal_card.wav')

            # 수정중
            self.player[self.now_turn].remove(temp)
            self.player[self.now_turn].set_lastcard()

            # card.play()
            self.waste.updating(temp)
            self.set_animation('back', (self.size[0] * (1 / 30) + 10 * (self.player[self.now_turn].last_idx - 1),
                                        self.size[1] * ((2 * self.player[self.now_turn].index - 1) / 10)))
            # 안해도 될 것 같아 시간 걸려 - 확인하고 삭제해줘
            # self.print_window()
            # pygame.display.update()
            self.card_skill(temp)
            if len(self.player[self.now_turn].group) == 1:
                # 안해도 될 것 같아 시간 걸려 - 확인하고 삭제해줘
                # pygame.display.update()
                self.check_uno_button()
            else:
                pass
                # 안해도 될 것 같아 시간 걸려 - 확인하고 삭제해줘
                # self.print_window()
                # self.now_turn = self.get_next_player(self.now_turn)
            return temp
            # 안해도 될 것 같아 시간 걸려 - 확인하고 삭제해줘
            # pygame.display.update()

    def get_next_turn(self, turn=True):
        pass

    # 게임 시작 (다시 시작 )
    def startgame(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.card_deck.clear()
        self.player = []
        self.player_names = self.set_name()
        self.rotate = 0
        self.now_turn = self.selected_turn()
        self.set_window()
        self.timer.reset_tmr()
        self.playgame()
        return 0

    # 수정중
    # 게임 구현
    def playgame(self):
        selected = 0
        selected_up = 0

        while self.playing_game:
            self.check_player()
            tmr_bool = self.timer.tick_tmr()

            if len(self.card_deck) == 0:
                self.set_deck()

            if len(self.waste.card) == 0:
                temp = self.card_deck.pop()
                self.waste.updating(temp)
                self.card_skill(temp)
                self.print_window()
                pygame.display.update()

            if self.now_turn != 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                temp = self.computer_play()
            else:
                temp = self.user_play()

            if temp and type(temp) == str:
                self.animation(*temp)
            if temp or tmr_bool is False:
                self.get_next_turn(self.first)
                self.now_turn = self.get_next_player(self.now_turn)

            self.print_window()
            pygame.display.update()

        # self.animate()

    def user_play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
                        return 'Back'
                        # self.now_turn = self.get_next_player(self.now_turn)
                        # break
                    else:
                        for sprite in self.player[0].group:
                            if sprite.get_name() == self.player[0].card[selected] and self.check_card(sprite):
                                self.player[0].remove(sprite)
                                for temp in self.player[0].group:
                                    temp.move(sprite.getposition())
                                sprite.setposition(
                                    self.size[0] * (3 / 5), self.size[1] * (1 / 3))
                                self.waste.updating(sprite.get_name())
                                self.card_skill(sprite.get_name())
                                if len(self.player[0].group) == 1:  # 카드 내고 한장 남음
                                    pygame.display.update()
                                    self.check_uno_button()
                                # else:
                                # self.now_turn = self.get_next_player(self.now_turn)
                                if selected > len(self.player[0]) - 1:
                                    selected = len(self.player[0]) - 1
                                break
            if event.type == MOUSEBUTTONUP:
                select_sound = pygame.mixer.Sound('./sound/card_sound.mp3')
                select_sound.play()
                if self.now_turn == 0:
                    # self.show_now_turn(self.now_turn)
                    for sprite in self.player[0].group:
                        if sprite.get_rect().collidepoint(event.pos) and self.check_card(sprite):
                            self.set_animation(
                                sprite.get_name(), sprite.getposition())
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
                            # else:
                            # return 0      얘를 없애 볼게
                            # self.now_turn = self.get_next_player(self.now_turn)
                            return sprite.get_name()
                            # return 1
                    for sprite in self.waste.group:
                        if sprite.get_rect().collidepoint(event.pos):
                            self.get_from_deck(self.now_turn)
                            # self.show_uno()
                            # self.now_turn = self.get_next_player(self.now_turn)
                            # 수정중
                            return 'Back'
                            # break

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
        self.player[now_turn].add_card(item)
        self.set_animation('back', (self.size[0] * (2 / 5),
                                    self.size[1] * (1 / 3)))
        # self.print_window()

    def set_animation(self, name, pos):
        self.animate_card = lc.Card(name, pos, (self.settings['screen']
                                                [0] / 10, self.settings['screen'][1] / 6))

    def run_animation(self):
        if self.animation:
            ori = self.animate_card.getposition()
            self.animate_card.animate(
                (self.size[0] * (3 / 5), self.size[1] * (1 / 3)))
            self.animation_group = pygame.sprite.RenderPlain(self.animate_card)
            s = self.animate_card.getposition()
            pos = (self.size[0] * (3 / 5), self.size[1] * (1 / 3))
            if self.animate_card.getposition() == (self.size[0] * (3 / 5), self.size[1] * (1 / 3)):
                return 0
        return 1

    def get_animation(self):
        if self.animation:
            ori = (self.size[0] * (2 / 5), self.size[1] * (1 / 3))
            self.animate_card.animate(
                self.player[self.now_turn].last.getposition())
            self.animation_group = pygame.sprite.RenderPlain(self.animate_card)
            s = self.animate_card.getposition()
            if self.animate_card.getposition() == self.player[self.now_turn].last.getposition():
                return 0
        return 1

    def animation(self, *temp):
        self.playing_game = False
        setting = 1

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t.terminate()
            if temp[0] == 'B':
                setting = self.get_animation()
            else:
                setting = self.run_animation()
            self.print_window()
            pygame.display.update()

        self.playing_game = True

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
                    if achievement_button.get_rect().collidepoint(event.pos):
                        pass
                    elif setting_button.get_rect().collidepoint(event.pos):
                        pass
                    elif exit_button.get_rect().collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing_game = True
                        paused = False

            # 수정중
            pygame.draw.rect(self.screen, c.WHITE, (self.size[0] /
                                                    2 - 200, self.size[1] / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, c.BLACK, (self.size[0] / 2 - 200, self.size[1] / 3 - 100, 400, 400),
                             5)
            # t.text_format 수정 필요
            close_text = t.text_format("PAUSE", c.MALGUNGOTHIC, 60, c.BLACK)
            close_text_rect = close_text.get_rect(
                center=(self.size[0] / 2, self.size[1] / 3))
            achievement_button = rf.Button(self.screen, self.size[0] * (3 / 7), self.size[1] * (2 / 5) - 100,
                                           "./image/playing_image/pause_achv.jpg", 200, 100)
            setting_button = rf.Button(self.screen, self.size[0] * (3 / 7), self.size[1] * (2 / 5),
                                       "./image/playing_image/pause_setting.jpg", 200, 100)
            exit_button = rf.Button(self.screen, self.size[0] * (3 / 7), self.size[1] * (2 / 5) + 100,
                                    "./image/playing_image/pause_end.jpg", 200, 100)
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
                                # uno_text = t.text_format(
                                #     "uno", c.BERLIN, 30, (0, 0, 0))
                                # self.screen.blit(uno_text, (45, 100))
                                self.get_from_deck(self.now_turn)
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                            else:  # 컴퓨터 턴일때 유저가 느리게 누름
                                print("유저가 느리게 누름")
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                        else:
                            if self.now_turn == 0:  # 유저 턴일 때
                                print("빠르게 누름!")
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                            else:  # 컴퓨터 턴일 때 유저가 빠르게 누름
                                print("유저가 빠르게 누름!")
                                self.get_from_deck(self.now_turn)
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
            if (time.time() - start_time) > 3:
                if self.now_turn == 0:  # 그냥 버튼 안누르고 있을 때 5초 지나면 한 장 먹음
                    print("컴퓨터가 누름")
                    self.get_from_deck(self.now_turn)
                    # self.now_turn = self.get_next_player(self.now_turn)
                    self.first = False
                    uno = False
                else:  # 이건 컴퓨터가 1장 남았을 때 유저가 버튼을 안 누르고 있는 경우
                    if self.player_num == 2:  # 유저랑 컴퓨터 1명만 있는 경우 컴퓨터가 uno버튼 누른걸로 판단
                        print("컴퓨터가 누름")
                        # self.now_turn = self.get_next_player(self.now_turn)
                        self.first = False
                        uno = False
                    else:  # 다른 컴퓨터랑 경쟁
                        com_time = random.randint(0, 1)  # 그냥 0,1로 했어요.
                        if com_time == 1:  # 빠르게 누른 경우
                            print("컴퓨터가 누름")
                            # self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
                        else:  # 느리게 누른 경우 - 카드 뽑음
                            print("컴퓨터가 못 누름")
                            self.get_from_deck(self.now_turn)
                            # self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
            pygame.display.update()


class GameA(Game):
    def __init__(self, player_num=2, difficulty=2, user_name="ME"):
        super().__init__()
        self.player_num = player_num
        self.difficulty = difficulty
        self.user_name = user_name

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
            self.player[player].card = card
        card_deck = num_card + skill_card
        del num_card, skill_card
        return card_deck

    def hand_out_deck(self):
        self.card_deck = self.difficulty_two_deck()
        random.shuffle(self.card_deck)
        for _ in range(7):
            temp = self.card_deck.pop()
            self.player[0].append(temp)


class GameWithA(GameA):
    def __init__(self, user_name, player_list):
        super().__init__(player_num=len(player_list), user_name=user_name)
        self.player_num = len(player_list)
        self.player_list = player_list

    def difficulty_two_deck(self):
        num_card = self.card_deck[:76]
        skill_card = self.card_deck[76:]
        random.shuffle(num_card)
        random.shuffle(skill_card)
        for index, name in enumerate(self.player_list):
            if name.split(' ')[0] == 'comA':
                card = []
                for _ in range(0, 7):
                    if random.random() < 76 / 164:
                        temp = num_card.pop()
                    else:
                        temp = skill_card.pop()
                    card.append(temp)
                self.player[index].card = card
        card_deck = num_card + skill_card
        del num_card, skill_card
        return card_deck

    def set_name(self):
        player_names = []
        text = rf.TextRect(self.screen, self.user_name, 30, c.WHITE)
        player_names.append(
            [text, (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
        for index, name in enumerate(self.player_list):
            if index != 0:
                if name.split(' ')[0] == 'comA':
                    text = rf.TextRect(
                        self.screen, "COM_A" + str(index), 20, c.BLACK)
                    player_names.append(
                        [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * index - 4) / 25))])
                else:
                    text = rf.TextRect(self.screen, "COM" +
                                       str(index), 20, c.BLACK)
                    player_names.append(
                        [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * index - 4) / 25))])
        return player_names

    def hand_out_deck(self):
        self.card_deck = self.difficulty_two_deck()
        random.shuffle(self.card_deck)
        for _ in range(7):
            temp = self.card_deck.pop()
            self.player[0].append(temp)
        for index, name in enumerate(self.player_list):
            if index != 0 and name.split(' ')[0] != 'comA':
                for _ in range(7):
                    temp = self.card_deck.pop()
                    self.player[index].append(temp)


class GameB(Game):
    def __init__(self, player_num=4, difficulty=3, user_name="ME"):
        super().__init__()
        self.player_num = 4
        self.difficulty = 3

    def hand_out_deck(self):
        i = len(self.card_deck) // self.player_num
        random.shuffle(self.card_deck)
        card_temp = self.card_deck.pop()  # 첫번째 카드 미리 뽑아두기
        for num in range(0, self.player_num):
            for number in range(0, i):  # 모든 카드 같은 수 만큼 플레이어에게 분배
                if self.card_deck:
                    temp = self.card_deck.pop()
                    self.player[num].append(temp)
        self.card_deck.append(card_temp)

    def set_window(self):
        self.card_deck = self.set_deck()
        self.player_init()
        self.hand_out_deck()
        self.waste.set_card()

        for i in range(self.player_num):
            self.player[i].set_card()

        setting = True

        settings = [1 for _ in range(self.player_num)]

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            settings[0] = self.player[0].set_d()

            for num in range(1, self.player_num):
                if settings[num]:
                    settings[num] = self.player[num].set_d()

            # pygame.mixer.pre_init(44100, -16, 1, 512)
            # card = pygame.mixer.Sound('./sound/card.wav')
            # for i in range(0,7):
            #     card.play()
            if sum(settings) == 0:
                setting = False
                return 0

            self.print_window()
            pygame.display.update()

    def restart(self):
        if len(self.player[0].group) == 0:
            self.settings['achievement']['storyb_win'] = True
            self.setting.change_setting(self.settings)
        return super().restart()


class GameC(Game):
    def __init__(self, player_num=3, difficulty=4, user_name="ME"):
        super().__init__()
        self.player_num = 3
        self.difficulty = 4

    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        self.player_num = 3
        for num in range(0, self.player_num):
            card = []
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                self.player[num].append(temp)

    def get_next_turn(self, turn=True):
        if turn:
            self.change_current_color()
            self.game_turn += 1
            pygame.time.wait(1000)
            print("turn", self.game_turn)

    def change_current_color(self):
        if self.game_turn % 5 == 0 and self.game_turn != 0:
            colors = ["red", "yellow", "green", "blue"]
            random_name = colors[random.randint(0, 3)]
            self.waste.updating(random_name)
            self.print_window()

    def restart(self):
        if len(self.player[0].group) == 0:
            self.settings['achievement']['storyc_win'] = True
            self.setting.change_setting(self.settings)
        return super().restart()


class GameD(Game):
    def __init__(self, player_num=3, difficulty=5, user_name="ME"):
        super().__init__()
        self.player_num = 3
        self.difficulty = 5

    def set_deck(self):
        card_deck = []
        for color_idx in range(1, 5):
            card = c.CARD_TYPE[color_idx]
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
        for num in range(0, self.player_num):
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                self.player[num].append(temp)

    def check_card(self, sprite):
        if len(self.waste.card) == 0:
            return True
        else:
            name = sprite.get_name()
            name = name.split('_')
            w_name = self.waste.card[-1]
            w_name = w_name.split('_')
            if w_name[1] != '0' and name[1] != '0':
                if (int(w_name[1]) % int(name[1])) == 0 or (int(name[1]) % int(w_name[1])) == 0:
                    return True
            else:
                return True

    def restart(self):
        if len(self.player[0].group) == 0:
            self.settings['achievement']['storyd_win'] = True
            self.setting.change_setting(self.settings)
        return super().restart()
