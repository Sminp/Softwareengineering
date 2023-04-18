import sys
import random
import pygame
import math
import loadcard
import computer
from pygame.locals import *
from constant import *
from UNO import Button, text_format, terminate
import time


class Game():
    def __init__(self, uno_game, player_num=2, difficulty=1, player_name="ME"):  # 초기값 임시로 설정 - 지우기
        self.uno_game = uno_game
        self.player_num = player_num
        self.difficulty = difficulty
        self.screen_width = self.uno_game.screen_width
        self.screen_height = self.uno_game.screen_height
        self.screen = self.uno_game.screen
        self.background_img_load = uno_game.background_img_load("./image/playing_image/playing_background.png")
        
        self.color = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'wild'}
        self.skill = {11: '_pass', 12: '_reverse', 13: '_plus_two', 14: '_basic', 15: '_plus_four', 16: '_change'}
        self.card_deck = []
        self.player = [[] for _ in range(0, self.player_num)]
        self.waste_group = pygame.sprite.RenderPlain()
        self.waste_card = []
        self.rotate = 0
        self.uno = 0
        self.playing_game = True
        self.game_turn = 0
        self.uno_button = Button(self.screen, self.screen_width * (3 / 4), self.screen_height * (1 / 3),
                                 "./image/playing_image/uno_button.png", self.screen_height * (1 / 20), self.screen_height * (1 / 20))
        self.time_limit = 10  # -> 시간 제한 설정
        # self.first_show = True
        # self.two_first_show = True
        self.time = 0
        self.active = False
        self.player_name = player_name
        self.first = True
        pygame.display.update()

        self.lastcard0 = None
        self.lastcard1 = None
        self.lastcard2 = None
        self.lastcard3 = None
        self.lastcard4 = None
        self.lastcard5 = None

    # 카드 생성
    def set_deck(self) -> list:
        card_deck = []
        if self.difficulty != 5:
            for color_idx in range(1, 5):
                card = self.color[color_idx]
                now_card = card + '_0'
                card_deck.append(now_card)
                for card_number in range(1, 10):
                    now_card = card + "_" + str(card_number)
                    iterate = 0
                    while iterate != 2:
                        card_deck.append(now_card)
                        iterate += 1
            for color_idx in range(1, 5):
                card = self.color[color_idx]
                for card_number in range(11, 14):
                    now_card = card + self.skill[card_number]
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
                now_card = card + self.skill[card_number]
                iterate = 0
                while iterate != 4:
                    card_deck.append(now_card)
                    iterate += 1
        else:  # 스토리 D구역 카드 - 기술 카드 제외
            for color_idx in range(1, 5):
                card = self.color[color_idx]
                now_card = card + '_0'
                card_deck.append(now_card)
                for card_number in range(1, 10):
                    now_card = card + "_" + str(card_number)
                    iterate = 0
                    while iterate != 2:
                        card_deck.append(now_card)
                        iterate += 1
        return card_deck

    def difficulty_two_deck(self):
        num_card = self.card_deck[:76]
        skill_card = self.card_deck[76:]
        random.shuffle(num_card)
        random.shuffle(skill_card)
        for player in range(1, self.player_num):
            card = []
            for number in range(0, 7):
                if random.random() < 76 / 164:
                    temp = num_card.pop()
                else:
                    temp = skill_card.pop()
                card.append(temp)
            self.player[player] = card
        card_deck = num_card + skill_card
        del num_card, skill_card
        return card_deck

    # 게임 시작 화면 - 덱 구성, 플레이어에게 카드 지급, 플레이어 숫자마다 카드 위치 다 다름 -> 5명까지 설정해야함
    # 함수를 나눠야 할 것 같아 test 만드는데 이 함수 돌릴 때 시간이 3초 넘게 걸려
    def set_window(self):
        self.card_deck = self.set_deck()
        if self.difficulty == 1:
            random.shuffle(self.card_deck)
            for player in range(0, self.player_num):
                card = []
                for number in range(0, 7):
                    temp = self.card_deck.pop()
                    card.append(temp)
                self.player[player] = card
        elif self.difficulty == 2:
            self.card_deck = self.difficulty_two_deck()
            random.shuffle(self.card_deck)
            card = []
            for number in range(7):
                temp = self.card_deck.pop()
                card.append(temp)
            self.player[0] = card
        elif self.difficulty == 3:
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
        elif self.difficulty == 4:
            random.shuffle(self.card_deck)
            self.player_num = 2
            for player in range(0, self.player_num):
                card = []
                for number in range(0, 7):
                    temp = self.card_deck.pop()
                    card.append(temp)
                self.player[player] = card
        elif self.difficulty == 5:
            random.shuffle(self.card_deck)
            self.player_num = 3
            for player in range(0, self.player_num):
                card = []
                for number in range(0, 7):
                    temp = self.card_deck.pop()
                    card.append(temp)
                self.player[player] = card

        deck = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                             (self.screen_width / 10, self.screen_height / 6))
        self.deck_group = pygame.sprite.RenderPlain(deck)

        # 이거 왜 있어? init? 혹시 몰라서야? -> 엥 이거 왜 있지? 지워볼까?
        player_deck = self.player[0]
        init_card = []
        for item in player_deck:
            cards = loadcard.Card(item, (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                  (self.screen_width / 10, self.screen_height / 6))
            init_card.append(cards)

        for i in range(len(self.player)):
            player_deck = self.player[i]
            if i == 0:
                user_card = []
                for item in player_deck:
                    cards = loadcard.Card(item, (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 10, self.screen_height / 6))
                    user_card.append(cards)
            elif i == 1:
                com1_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 30, self.screen_height / 18))
                    com1_card.append(cards)
            elif i == 2:
                com2_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 30, self.screen_height / 18))
                    com2_card.append(cards)
            elif i == 3:
                com3_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 30, self.screen_height / 18))
                    com3_card.append(cards)
            elif i == 4:
                com4_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 30, self.screen_height / 18))
                    com4_card.append(cards)
            else:
                com5_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                          (self.screen_width / 30, self.screen_height / 18))
                    com5_card.append(cards)

        setting = True
        setting_user = 1
        setting_com1 = 1
        setting_com2 = 1
        setting_com3 = 1
        setting_com4 = 1
        setting_com5 = 1

        # 이게 뭐지?

        if self.player_num == 5:
            setting_com5 = 0
        elif self.player_num == 4:
            setting_com5 = 0
            setting_com4 = 0
        elif self.player_num == 3:
            setting_com5 = 0
            setting_com4 = 0
            setting_com3 = 0
        elif self.player_num == 2:
            setting_com5 = 0
            setting_com4 = 0
            setting_com3 = 0
            setting_com2 = 0

        while setting:
            # tmr = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            i = 0
            temp_list = []

            if self.difficulty == 3:
                j = 0
                k = 0
                for item in user_card:
                    if 7 <= i < 14:
                        item.update((self.screen_width * (1 / 3) + 80 * j,
                                     self.screen_height * (7 / 9) + self.screen_height / 10))
                        temp_list.append(item)
                        j += 1
                        i += 1
                    elif i >= 14:
                        item.update((self.screen_width * (1 / 3) + 80 * k,
                                     self.screen_height * (7 / 9) + self.screen_height * 2 / 10))
                        temp_list.append(item)
                        k += 1
                        i += 1
                    else:
                        item.update((self.screen_width * (1 / 3) + 80 * i, self.screen_height * (7 / 9)))
                        temp_list.append(item)
                        i += 1
                self.user_group = pygame.sprite.RenderPlain(*temp_list)
                if temp_list:
                    self.lastcard0 = temp_list[-1].getposition()
                if self.lastcard0 == (
                        self.screen_width * (1 / 3) + 80 * (len(temp_list) % 7 - 1),
                        self.screen_height * (7 / 9) + self.screen_height * 2 / 10):
                    setting_user = 0
            else:
                for item in user_card:
                    item.update((self.screen_width * (1 / 3) + 80 * i, self.screen_height * (7 / 9)))
                    temp_list.append(item)
                    i += 1
                self.user_group = pygame.sprite.RenderPlain(*temp_list)
                if temp_list:
                    self.lastcard0 = temp_list[-1].getposition()
                if self.lastcard0 == (
                        self.screen_width * (1 / 3) + 80 * (len(temp_list) - 1), self.screen_height * (7 / 9)):
                    setting_user = 0

            i = 0
            temp_list = []
            setting = True
            if self.difficulty == 3:
                j = 0
                for item in com1_card:
                    if i >= 12:
                        item.update((self.screen_width * (1 / 30) + 10 * j,
                                     self.screen_height * (1 / 10) + self.screen_height * (1 / 30)))
                        j += 1
                        i += 1
                        temp_list.append(item)
                    else:
                        item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (1 / 10)))
                        temp_list.append(item)
                        i += 1
                self.com1_group = pygame.sprite.RenderPlain(*temp_list)
                if temp_list:
                    self.lastcard1 = temp_list[-1].getposition()
                if self.lastcard1 == (
                        self.screen_width * (1 / 30) + 10 * (len(temp_list) % 12 - 1),
                        self.screen_height * (1 / 10) + self.screen_height * (1 / 30)):
                    setting_com1 = 0
            else:
                for item in com1_card:
                    item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (1 / 10)))
                    temp_list.append(item)
                    i += 1
                self.com1_group = pygame.sprite.RenderPlain(*temp_list)
                if temp_list:
                    self.lastcard1 = temp_list[-1].getposition()
                if self.lastcard1 == (
                        self.screen_width * (1 / 30) + 10 * (len(temp_list) - 1), self.screen_height * (1 / 10)):
                    setting_com1 = 0

            if self.player_num >= 3:
                i = 0
                temp_list = []
                setting = True
                if self.difficulty == 3:
                    j = 0
                    for item in com2_card:
                        if i >= 12:
                            item.update((self.screen_width * (1 / 30) + 10 * j,
                                         self.screen_height * (3 / 10) + self.screen_height * (1 / 30)))
                            temp_list.append(item)
                            j += 1
                            i += 1
                        else:
                            item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (3 / 10)))
                            temp_list.append(item)
                            i += 1
                    self.com2_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard2 = temp_list[-1].getposition()
                    if self.lastcard2 == (
                            self.screen_width * (1 / 30) + 10 * (len(temp_list) % 12 - 1),
                            self.screen_height * (3 / 10) + self.screen_height * (1 / 30)):
                        setting_com2 = 0

                else:
                    for item in com2_card:
                        item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (3 / 10)))
                        temp_list.append(item)
                        i += 1
                    self.com2_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard2 = temp_list[-1].getposition()
                    if self.lastcard2 == (
                            self.screen_width * (1 / 30) + 10 * (len(temp_list) - 1), self.screen_height * (3 / 10)):
                        setting_com2 = 0

            if self.player_num >= 4:
                i = 0
                temp_list = []
                setting = True
                if self.difficulty == 3:
                    j = 0
                    for item in com3_card:
                        if i >= 12:
                            item.update((self.screen_width * (1 / 30) + 10 * j,
                                         self.screen_height * (1 / 2) + self.screen_height * (1 / 30)))
                            temp_list.append(item)
                            j += 1
                            i += 1
                        else:
                            item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (1 / 2)))
                            temp_list.append(item)
                            i += 1
                    self.com3_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard3 = temp_list[-1].getposition()
                    if self.lastcard3 == ((self.screen_width * (1 / 30) + 10 * (len(temp_list) % 12 - 1),
                                           self.screen_height * (1 / 2) + self.screen_height * (1 / 30))):
                        setting_com3 = 0

                else:
                    for item in com3_card:
                        item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (1 / 2)))
                        temp_list.append(item)
                        i += 1
                    self.com3_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard3 = temp_list[-1].getposition()
                    if self.lastcard3 == (
                            (self.screen_width * (1 / 30) + 10 * (len(temp_list) - 1), self.screen_height * (1 / 2))):
                        setting_com3 = 0

            if self.player_num >= 5:
                i = 0
                temp_list = []
                setting = True
                if self.difficulty == 3:
                    j = 0
                    for item in com4_card:
                        if i >= 12:
                            item.update((self.screen_width * (1 / 30) + 10 * j,
                                         self.screen_height * (7 / 10) + self.screen_height * (1 / 30)))
                            temp_list.append(item)
                            j += 1
                            i += 1
                        else:
                            item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (7 / 10)))
                            temp_list.append(item)
                            i += 1
                    self.com4_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard4 = temp_list[-1].getposition()
                    if self.lastcard4 == ((self.screen_width * (1 / 30) + 10 * (len(temp_list) % 12 - 1),
                                           self.screen_height * (7 / 10) + self.screen_height * (1 / 30))):
                        setting_com4 = 0
                else:
                    for item in com4_card:
                        item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (7 / 10)))
                        temp_list.append(item)
                        i += 1
                    self.com4_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard4 = temp_list[-1].getposition()
                    if self.lastcard4 == (
                            (self.screen_width * (1 / 30) + 10 * (len(temp_list) - 1), self.screen_height * (7 / 10))):
                        setting_com4 = 0

            if self.player_num == 6:
                i = 0
                temp_list = []
                setting = True
                if self.difficulty == 3:
                    j = 0
                    for item in com5_card:
                        if i >= 12:
                            item.update((self.screen_width * (1 / 30) + 10 * j,
                                         self.screen_height * (9 / 10) + self.screen_height * (1 / 30)))
                            temp_list.append(item)
                            i += 1
                            j += 1
                        else:
                            item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (9 / 10)))
                            temp_list.append(item)
                            i += 1
                    self.com5_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard5 = temp_list[-1].getposition()
                    if self.lastcard5 == ((self.screen_width * (1 / 30) + 10 * (len(temp_list) % 12 - 1),
                                           self.screen_height * (9 / 10) + self.screen_height * (1 / 30))):
                        setting_com5 = 0

                else:
                    for item in com5_card:
                        item.update((self.screen_width * (1 / 30) + 10 * i, self.screen_height * (9 / 10)))
                        temp_list.append(item)
                        i += 1
                    self.com5_group = pygame.sprite.RenderPlain(*temp_list)
                    if temp_list:
                        self.lastcard5 = temp_list[-1].getposition()
                    if self.lastcard5 == (
                            (self.screen_width * (1 / 30) + 10 * (len(temp_list) - 1), self.screen_height * (9 / 10))):
                        setting_com5 = 0

            if setting_user == 0 and setting_com1 == 0 and setting_com2 == 0 and setting_com3 == 0 and setting_com4 == 0 and setting_com5 == 0:
                setting = False

            # #pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # card = pygame.mixer.Sound('./sound/card.wav')
            # for i in range(0,7):
            #     card.play()
            self.print_window()
            pygame.display.update()

    # 플레이어 이름 표시
    def next_turn(self, now_turn: int) -> int:
        if now_turn == 0:
            user_text = text_format(self.player_name, BERLIN, 30, WHITE)
            user_text_rect = user_text.get_rect(center=(self.screen_width * (3 / 5), self.screen_height * (2 / 3)))
            self.screen.blit(user_text, user_text_rect)

        elif now_turn == 1:
            com1_text = text_format("COM1", BERLIN, 20, BLACK)
            self.screen.blit(com1_text, (self.screen_width * (1 / 45), self.screen_height * (1 / 25)))

        elif now_turn == 2:
            com2_text = text_format("COM2", BERLIN, 20, BLACK)
            self.screen.blit(com2_text, (self.screen_width * (1 / 45), self.screen_height * (6 / 25)))

        elif now_turn == 3:
            com3_text = text_format("COM3", BERLIN, 20, BLACK)
            self.screen.blit(com3_text, (self.screen_width * (1 / 45), self.screen_height * (11 / 25)))

        elif now_turn == 4:
            com4_text = text_format("COM4", BERLIN, 20, BLACK)
            self.screen.blit(com4_text, (self.screen_width * (1 / 45), self.screen_height * (16 / 25)))
        else:
            com5_text = text_format("COM5", BERLIN, 20, BLACK)
            self.screen.blit(com5_text, (self.screen_width * (1 / 45), self.screen_height * (21 / 25)))
        temp = self.get_next_player(now_turn)
        return temp

    def get_next_turn(self):
        if self.first:
            self.game_turn += 1
            self.change_color()
            pygame.time.wait(1000)
            self.first = False

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

    # 지금 현재 턴인 플레이어 표시
    def select_player(self, now_turn):
        if now_turn == 0:
            user_text = text_format(self.player_name, BERLIN, 30, YELLOW)
            user_text_rect = user_text.get_rect(center=(self.screen_width * (3 / 5), self.screen_height * (2 / 3)))
            self.screen.blit(user_text, user_text_rect)
        elif now_turn == 1:
            com1_text = text_format("COM1", BERLIN, 20, YELLOW)
            self.screen.blit(com1_text, (self.screen_width * (1 / 45), self.screen_height * (1 / 25)))
        elif now_turn == 2:
            com2_text = text_format("COM2", BERLIN, 20, YELLOW)
            self.screen.blit(com2_text, (self.screen_width * (1 / 45), self.screen_height * (6 / 25)))
        elif now_turn == 3:
            com3_text = text_format("COM3", BERLIN, 20, YELLOW)
            self.screen.blit(com3_text, (self.screen_width * (1 / 45), self.screen_height * (11 / 25)))
        elif now_turn == 4:
            com4_text = text_format("COM4", BERLIN, 20, YELLOW)
            self.screen.blit(com4_text, (self.screen_width * (1 / 45), self.screen_height * (16 / 25)))
        else:
            com5_text = text_format("COM5", BERLIN, 20, YELLOW)
            self.screen.blit(com5_text, (self.screen_width * (1 / 45), self.screen_height * (21 / 25)))
        pygame.display.update()

    # 플레이어 이름 표시 초기화
    # def print_window(self, active=1):
    def print_window(self):
        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.screen_height - 500) / 6), self.screen_width / 5,
                               self.screen_height / 6)
            computer_rect.append(rect)
        self.screen.blit(self.background_img_load, (0, 0))
        for rect in computer_rect:
            pygame.draw.rect(self.screen, WHITE, rect)

        self.deck_group.draw(self.screen)
        self.user_group.draw(self.screen)
        self.com1_group.draw(self.screen)
        self.uno_button.show_button()
        if self.player_num >= 3:
            self.com2_group.draw(self.screen)
            com2_text = text_format("COM2", BERLIN, 20, BLACK)
            self.screen.blit(com2_text, (self.screen_width * (1 / 45), self.screen_height * (6 / 25)))
        if self.player_num >= 4:
            self.com3_group.draw(self.screen)
            com3_text = text_format("COM3", BERLIN, 20, BLACK)
            self.screen.blit(com3_text, (self.screen_width * (1 / 45), self.screen_height * (11 / 25)))
        if self.player_num >= 5:
            self.com4_group.draw(self.screen)
            com4_text = text_format("COM4", BERLIN, 20, BLACK)
            self.screen.blit(com4_text, (self.screen_width * (1 / 45), self.screen_height * (16 / 25)))
        if self.player_num == 6:
            self.com5_group.draw(self.screen)
            com5_text = text_format("COM5", BERLIN, 20, BLACK)
            self.screen.blit(com5_text, (self.screen_width * (1 / 45), self.screen_height * (21 / 25)))

        # 여기도 인원수 추가 
        user_text = text_format(self.player_name, BERLIN, 30, WHITE)
        user_text_rect = user_text.get_rect(center=(self.screen_width * (3 / 5), self.screen_height * (2 / 3)))
        self.screen.blit(user_text, user_text_rect)
        com1_text = text_format("COM1", BERLIN, 20, BLACK)
        self.screen.blit(com1_text, (self.screen_width * (1 / 45), self.screen_height * (1 / 25)))
        self.waste_group.draw(self.screen)
        if len(self.waste_card) == 0:
            pygame.draw.rect(self.screen, BLACK, (
                self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
        else:
            w_name = self.waste_card[-1]
            w_name = w_name.split('_')
            if w_name[0] == 'wild':
                pygame.draw.rect(self.screen, BLACK, (
                    self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                    self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
            elif w_name[0] == "red":
                if len(w_name) > 1:
                    if w_name[1] == 'yellow':
                        pygame.draw.rect(self.screen, RED, (
                            self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                            self.screen_height * (1 / 40), self.screen_height * (1 / 20)))
                        pygame.draw.rect(self.screen, YELLOW, (
                            self.screen_width * (3 / 4) + self.screen_height * (1 / 40),
                            self.screen_height * (1 / 3) - self.screen_height * (1 / 20), self.screen_height * (1 / 40),
                            self.screen_height * (1 / 20)))
                    else:
                        pygame.draw.rect(self.screen, RED, (
                            self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                            self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
                else:
                    pygame.draw.rect(self.screen, RED, (
                        self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                        self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
            elif w_name[0] == "yellow":
                pygame.draw.rect(self.screen, YELLOW, (
                    self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                    self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
            elif w_name[0] == "blue":
                if len(w_name) > 1:
                    if w_name[1] == 'green':
                        pygame.draw.rect(self.screen, BLUE, (
                            self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                            self.screen_height * (1 / 40), self.screen_height * (1 / 20)))
                        pygame.draw.rect(self.screen, GREEN, (
                            self.screen_width * (3 / 4) + self.screen_height * (1 / 40),
                            self.screen_height * (1 / 3) - self.screen_height * (1 / 20), self.screen_height * (1 / 40),
                            self.screen_height * (1 / 20)))
                    else:
                        pygame.draw.rect(self.screen, BLUE, (
                            self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                            self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
                else:
                    pygame.draw.rect(self.screen, BLUE, (
                        self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                        self.screen_height * (1 / 20), self.screen_height * (1 / 20)))
            elif w_name[0] == "green":
                pygame.draw.rect(self.screen, GREEN, (
                    self.screen_width * (3 / 4), self.screen_height * (1 / 3) - self.screen_height * (1 / 20),
                    self.screen_height * (1 / 20), self.screen_height * (1 / 20)))

    # 낼 수 있는지 확인
    def check_card(self, sprite):
        if len(self.waste_card) == 0:
            return True
        else:
            name = sprite.get_name()
            name = name.split('_')
            w_name = self.waste_card[-1]
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
            self.pick_color()
        elif self.now_turn == 1:
            pygame.time.wait(500)
            self.most_num_color(self.player[1])
        elif self.now_turn == 2:
            pygame.time.wait(500)
            self.most_num_color(self.player[2])
        elif self.now_turn == 3:
            pygame.time.wait(500)
            self.most_num_color(self.player[3])
        elif self.now_turn == 4:
            pygame.time.wait(500)
            self.most_num_color(self.player[4])
        elif self.now_turn == 5:
            pygame.time.wait(500)
            self.most_num_color(self.player[5])

    # card_skill 중 card change 함수
    def card_change(self, now_turn, pick_turn):
        
        # 현재 턴의 플레이어 덱 임시 저장
        temp_player = self.player[now_turn][:]

        # 현재 턴의 플레이어 리스트 초기화
        self.player[now_turn].clear()

        # 현재 턴의 플레이어 덱 초기화 
        match now_turn:
            case 0:
                self.lastcard0 = (self.screen_width/3 - self.screen_width/10 , self.screen_height * (7 / 9))
                now_turn_lastcard = self.lastcard0
                for sprite in self.user_group:
                    self.user_group.remove(sprite)
            case 1:
                self.lastcard1 = (self.screen_width * (1 / 30) - 10 , self.screen_height * (1 / 10))
                now_turn_lastcard = self.lastcard1
                for sprite in self.com1_group:
                    self.com1_group.remove(sprite)
            case 2:
                self.lastcard2 = (self.screen_width * (1 / 30) - 10, self.screen_height * (3 / 10))
                now_turn_lastcard = self.lastcard2
                for sprite in self.com2_group:
                    self.com2_group.remove(sprite)
            case 3:
                self.lastcard3 = (self.screen_width * (1 / 30) - 10,self.screen_height * (1 / 2))
                now_turn_lastcard = self.lastcard3
                for sprite in self.com3_group:
                    self.com3_group.remove(sprite)
            case 4:
                self.lastcard4 = (self.screen_width * (1 / 30) - 10,self.screen_height * (7 / 10))
                now_turn_lastcard = self.lastcard4
                for sprite in self.com4_group:
                    self.com4_group.remove(sprite)
            case _:
                self.lastcard5 = (self.screen_width * (1 / 30) - 10,self.screen_height * (9 / 10))
                now_turn_lastcard = self.lastcard5
                for sprite in self.com5_group:
                    self.com5_group.remove(sprite)

        # 현재 턴의 플레이어 덱에 목표 플레이어 덱 넣기
        if now_turn == 0:
            for item in self.player[pick_turn]:
                card = loadcard.Card(item, (400, 300), (self.screen_width / 10, self.screen_height / 6))
                current_pos = now_turn_lastcard
                if current_pos[0] >= self.screen_width*(28/30):
                    y = current_pos[1] + self.screen_height / 7
                    x = self.screen_width/3
                else:
                    y = current_pos[1]
                    x = current_pos[0] + self.screen_width/ 10
                card.setposition(x, y)
                now_turn_lastcard = (x,y)
                self.lastcard0 = (x, y)
                self.user_group.add(card)
        else:
            for _ in range(len(self.player[pick_turn])):
                card = loadcard.Card('back', (400, 300), (self.screen_width / 30, self.screen_height / 18))
                current_pos = now_turn_lastcard
                if current_pos[0] >= self.screen_width/30 + 110: # 110을 화면 비율에 맞게 바꿔야함 10 (카드 겹치는 길이) X 11 (최대 12장)
                    y = current_pos[1] + self.screen_height/18
                    x = self.screen_width/ 30
                else:
                    y = current_pos[1]
                    x = current_pos[0] + 10
                card.setposition(x, y)
            
                match now_turn:
                    case 1:
                        now_turn_lastcard = (x,y)
                        self.lastcard1 = (x, y)
                        self.com1_group.add(card)
                    case 2:
                        now_turn_lastcard = (x,y)
                        self.lastcard2 = (x, y)
                        self.com2_group.add(card)
                    case 3:
                        now_turn_lastcard = (x,y)
                        self.lastcard3 = (x, y)
                        self.com3_group.add(card)
                    case 4:
                        now_turn_lastcard = (x,y)
                        self.lastcard4 = (x, y)
                        self.com4_group.add(card)
                    case _:
                        now_turn_lastcard = (x,y)
                        self.lastcard5 = (x, y)
                        self.com5_group.add(card)

        # 현재 턴인 플레이어 덱 리스트 목표 플레이어 덱 리스트로 변경
        self.player[now_turn] = self.player[pick_turn][:]

        # 목표 플레이어 덱 초기화 
        self.player[pick_turn].clear()
        match pick_turn:
            case 0:
                self.lastcard0 = (self.screen_width/3 - self.screen_width/10 , self.screen_height * (7 / 9))
                pick_turn_lastcard = self.lastcard0
                for sprite in self.user_group:
                    self.user_group.remove(sprite)
            case 1:
                self.lastcard1 = (self.screen_width * (1 / 30) - 10 , self.screen_height * (1 / 10))
                pick_turn_lastcard = self.lastcard1
                for sprite in self.com1_group:
                    self.com1_group.remove(sprite)
            case 2:
                self.lastcard2 = (self.screen_width * (1 / 30) - 10, self.screen_height * (3 / 10))
                pick_turn_lastcard = self.lastcard2
                for sprite in self.com2_group:
                    self.com2_group.remove(sprite)
            case 3:
                self.lastcard3 = (self.screen_width * (1 / 30) - 10,self.screen_height * (1 / 2))
                pick_turn_lastcard = self.lastcard3
                for sprite in self.com3_group:
                    self.com3_group.remove(sprite)
            case 4:
                self.lastcard4 = (self.screen_width * (1 / 30) - 10,self.screen_height * (7 / 10))
                pick_turn_lastcard = self.lastcard4
                for sprite in self.com4_group:
                    self.com4_group.remove(sprite)
            case _:
                self.lastcard5 = (self.screen_width * (1 / 30) - 10,self.screen_height * (9 / 10))
                pick_turn_lastcard = self.lastcard5
                for sprite in self.com5_group:
                    self.com5_group.remove(sprite)

        # 목표 플레이어 덱에 현재 턴인 플레이어 덱 넣기 
        if pick_turn == 0:
            for item in temp_player:
                card = loadcard.Card(item, (400, 300), (self.screen_width / 10, self.screen_height / 6))
                current_pos = pick_turn_lastcard
                if current_pos[0] >= self.screen_width*(28/30):
                    y = current_pos[1] + self.screen_height/6
                    x = self.screen_width/3
                else:
                    y = current_pos[1]
                    x = current_pos[0] + self.screen_width/ 10
                card.setposition(x, y)
                pick_turn_lastcard = (x,y)
                self.lastcard0 = (x, y)
                self.user_group.add(card)
        else:
            for _ in range(len(temp_player)):
                card = loadcard.Card('back', (400, 300), (self.screen_width / 30, self.screen_height / 18))
                current_pos = pick_turn_lastcard
                if current_pos[0] >= self.screen_width/30 + 110: # 110을 화면 비율에 맞게 바꿔야함 10 (카드 겹치는 길이) X 11 (최대 12장)
                    y = current_pos[1] + self.screen_height/18
                    x = self.screen_width/30
                else:
                    y = current_pos[1]
                    x = current_pos[0] + 10
                card.setposition(x, y)
            
                match pick_turn:
                    case 1:
                        pick_turn_lastcard = (x,y)
                        self.lastcard1 = (x, y)
                        self.com1_group.add(card)
                    case 2:
                        pick_turn_lastcard = (x,y)
                        self.lastcard2 = (x, y)
                        self.com2_group.add(card)
                    case 3:
                        pick_turn_lastcard = (x,y)
                        self.lastcard3 = (x, y)
                        self.com3_group.add(card)
                    case 4:
                        pick_turn_lastcard = (x,y)
                        self.lastcard4 = (x, y)
                        self.com4_group.add(card)
                    case _:
                        pick_turn_lastcard = (x,y)
                        self.lastcard5 = (x, y)
                        self.com5_group.add(card)
    
        # 목표 플레이어 덱 리스트 현재 플레이어 덱 리스트로 변경            
        self.player[pick_turn] = temp_player[:]
        self.print_window()

    # 기능 카드 수행
    # if name[0] 해서 기능 추가
    def card_skill(self, sprite):
        name = sprite.get_name()
        name = name.split('_')
        if name[1] == 'pass':
            pygame.time.wait(500)
            self.now_turn = self.next_turn(self.now_turn)
        elif name[1] == 'reverse':
            if self.player_num == 2:
                pygame.time.wait(500)
                self.now_turn = self.next_turn(self.now_turn)
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
                index = self.least_num()
                self.card_change(self.now_turn, index)
            self.print_window()

        elif name[1] == 'plus':
            if name[2] == 'two':
                pygame.time.wait(500)
                if len(self.card_deck) < 2:
                    pass
                else:
                    self.give_card(2)
                # self.now_turn = self.next_turn(self.now_turn)
            elif name[2] == 'four':
                # pygame.mixer.pre_init(44100, -16, 1, 512)
                pygame.init()
                # select = pygame.mixer.Sound('./sound/select.wav')
                # select.play()
                if len(self.card_deck) < 4:
                    pass
                else:
                    self.give_card(4)
                self.pick_color_card()
        elif name[0] == 'wild':
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # select = pygame.mixer.Sound('./sound/select.wav')
            # select.play()
            self.pick_color_card()
        # else:
        #     if self.now_turn != 0:
        #         return False
        # self.show_uno()
        # return True

    # 가장 적은 숫자 카드 나타내는 함수
    def least_num(self) -> int:
        least_player_idx = 0
        least_player_num = len(self.player[0])
        for num in range(1, self.player_num):
            if least_player_num > len(self.player[num]):
                least_player_idx = num
                least_player_num = len(self.player[num])
        return least_player_idx

    # 지금 덱 중에서 가장 숫자가 많은 색깔 구함 -> 컴퓨터가 wild 카드 사용할 때 사용 , 여기 수정해야함 그 숫자없는 카드가 없긴해 
    def most_num_color(self, card_deck):
        r = 0
        y = 0
        g = 0
        b = 0
        for item in card_deck:
            card = item.split('_')
            if card[0] == 'red':
                r += 1
            if card[0] == 'yellow':
                y += 1
            if card[0] == 'green':
                g += 1
            if card[0] == 'blue':
                b += 1
        a = [r, y, g, b]
        index = a.index(max(a))
        if index == 0:
            temp_name = 'red'
        if index == 1:
            temp_name = 'yellow'
        if index == 2:
            temp_name = 'green'
        if index == 3:
            temp_name = 'blue'
        temp = loadcard.Card(temp_name, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                             (self.screen_width / 10, self.screen_height / 6))
        self.waste_card.append(temp_name)
        self.waste_group.add(temp)
        self.print_window()

    # 변경할 색 선택
    def pick_color(self):
        # 뒤에 이미지 -> 빼거나 대체
        red = loadcard.Popup('red', (306, 320))
        yellow = loadcard.Popup('yellow', (368, 320))
        green = loadcard.Popup('green', (432, 320))
        blue = loadcard.Popup('blue', (494, 320))
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
                            temp = loadcard.Card(temp_name, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                                 (self.screen_width / 10, self.screen_height / 6))
                            self.waste_card.append(temp_name)
                            self.waste_group.add(temp)
                            self.print_window()
                            loop = False
        return 0

    # change 카드를 컴퓨터 플레이어가 선택할 때 제일 카드가 적은 플레이어 선택
    def check_card_num(self, player_deck_list):
        shortest_list = min(player_deck_list, key=len)
        return player_deck_list.index(shortest_list)

    # change 카드 사용할 때 바꿀 플레이어 선택
    def pick_player(self):

        pick_player_button = []
        for i in range(1,self.player_num):
            image_name = "./image/playing_image/deckchange_player"+str(i)+".jpg"
            temp_button = Button(self.screen, self.screen_width*(1/2), self.screen_height/6 * i, image_name, self.screen_width*(1/8), self.screen_height*(1/9))
            pick_player_button.append(temp_button)
        index = 0

        loop = True
        while loop:
            for i in range(self.player_num - 1):
                pick_player_button[i].show_button()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(self.player_num - 1):
                        if pick_player_button[i].get_rect().collidepoint(mouse_pos):
                            index = i
                            self.print_window()
                            loop = False
        
        return index + 1
    
    # 다음 차례 플레이어에게 카드 뽑게 함 -> draw 카드
    def give_card(self, card_num):
        if len(self.waste_card) == 1:  # 처음 카드가 +2,+4일때 처음 플레이어가 카드 받음
            dest_player = self.now_turn
        else:
            dest_player = self.get_next_player(self.now_turn)
        for i in range(0, card_num):
            self.get_from_deck(dest_player)

    # 게임 끝난 화면, 스페이스 버튼 누르면 다시 시작 
    def restart(self):
        # pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        # win = pygame.mixer.Sound('./sound/win.wav')
        # lose = pygame.mixer.Sound('./sound/lose.wav')
        pygame.draw.rect(self.screen, (255, 51, 0), pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(self.screen, (255, 180, 0), pygame.Rect(210, 210, 380, 180))

        if len(self.user_group) == 0:
            # win.play()
            close_text = text_format("YOU WIN!", BERLIN, 80, (255, 51, 0))
            press_text = text_format("Press SPACE to REPLAY", BERLIN, 35, (255, 51, 0))
            self.screen.blit(close_text, (230, 220))
        else:
            # lose.play()
            close_text = text_format("YOU LOSE!", BERLIN, 80, (255, 51, 0))
            press_text = text_format("Press SPACE to REPLAY", BERLIN, 35, (255, 51, 0))
            self.screen.blit(close_text, (212, 220))

        self.screen.blit(press_text, (228, 330))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.uno_game.main_menu()
                        return
        return 0

    def no_temp(self, now_turn: int):
        self.get_from_deck(now_turn)
        self.print_window()
        self.now_turn = self.next_turn(self.now_turn)
        pygame.display.update()

    def timer(self) -> bool:
        total_time = 10
        start_ticks = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer_msg = text_format(elapsed_time, MALGUNGOTHIC, 10, WHITE)
        self.screen.blit(timer_msg, (self.screen_width * (1 / 4), self.screen_height * (1 / 7)))
        if total_time <= elapsed_time:
            return False

    # 게임 시작 (다시 시작 )
    def startgame(self):
        self.card_deck.clear()
        self.player = [[0] for _ in range(0, self.player_num)]
        self.waste_group = pygame.sprite.RenderPlain()
        self.rotate = 0
        self.set_window()
        self.playgame()

    # 게임 구현
    def playgame(self):
        self.now_turn = 0
        self.waste_card = []
        tmr = 0
        selected = 0
        selected_up = 0

        while self.playing_game:
            if len(self.user_group) == 0:
                self.restart()
                return
            elif self.player_num == 6:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0 or len(self.player[3]) == 0 or len(
                        self.player[4]) == 0 or len(self.player[5]) == 0:
                    self.restart()
                    return
            elif self.player_num == 5:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0 or len(self.player[3]) == 0 or len(
                        self.player[4]) == 0:
                    self.restart()
                    return
            elif self.player_num == 4:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0 or len(self.player[3]) == 0:
                    self.restart()
                    return
            elif self.player_num == 3:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0:
                    self.restart()
                    return
            elif self.player_num == 2:
                if len(self.player[1]) == 0:
                    self.restart()
                    return
            if len(self.card_deck) == 0:
                self.set_deck()

            # self.show_uno()
            self.select_player(self.now_turn)
            if self.now_turn == 0 and len(self.waste_card) == 0:
                temp = loadcard.Card(self.card_deck.pop(), (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                     (self.screen_width / 10, self.screen_height / 6))
                self.put_waste_group(temp)
                self.card_skill(temp)
                self.print_window()
                pygame.display.update()

                # 일단 +2,+4 가 처음 카드로 나오면 첫 플레이어가 먹게 해둠

            self.get_next_turn()

            if self.now_turn == 1:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(2, self.player[1], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 3 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
                elif self.difficulty == 5:
                    temp = ai.special_play()
                if temp == 0 or temp is None:
                    self.no_temp(1)
                else:
                    # pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    # card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com1_group:
                        if sprite.getposition() == self.lastcard1:
                            self.com1_group.remove(sprite)
                    self.player[1].remove(temp)
                    self.set_lastcard(self.lastcard1, (0, 0))
                    # card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                           (self.screen_width / 10, self.screen_height / 6))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    # 이거 왜 있는거지? 이거 있어서 4장 먹는게 아니라 8장 먹어져
                    # if self.difficulty == 2 and self.card_skill(t_card): 
                    #     self.print_window()
                    #     pygame.display.update()
                    #     continue
                    self.card_skill(t_card)
                    if len(self.com1_group) == 1:
                        pygame.display.update()
                        self.check_uno_button()
                    else:
                        self.print_window()
                        self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()

            elif self.now_turn == 2:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(3, self.player[2], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 3 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
                elif self.difficulty == 5:
                    temp = ai.special_play()
                if temp == 0 or temp is None:
                    self.no_temp(2)
                else:
                    # pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    # card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com2_group:
                        if sprite.getposition() == self.lastcard2:
                            self.com2_group.remove(sprite)
                    self.player[2].remove(temp)
                    self.set_lastcard(self.lastcard2, (0, 0))
                    # card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                           (self.screen_width / 10, self.screen_height / 6))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    if self.difficulty == 2 and self.card_skill(t_card):
                        self.print_window()
                        pygame.display.update()
                        continue
                    self.card_skill(t_card)
                    self.print_window()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()
            elif self.now_turn == 3:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(4, self.player[3], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 3 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
                elif self.difficulty == 5:
                    temp = ai.special_play()
                if temp == 0 or temp is None:
                    self.no_temp(3)
                else:
                    # pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    # card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com3_group:
                        if sprite.getposition() == self.lastcard3:
                            self.com3_group.remove(sprite)
                    self.player[3].remove(temp)
                    self.set_lastcard(self.lastcard3, (0, 0))
                    # card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                           (self.screen_width / 10, self.screen_height / 6))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    if self.difficulty == 2 and self.card_skill(t_card):
                        self.print_window()
                        pygame.display.update()
                        continue
                    self.card_skill(t_card)
                    self.print_window()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()

            elif self.now_turn == 4:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(5, self.player[4], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 3 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
                elif self.difficulty == 5:
                    temp = ai.special_play()
                if temp == 0 or temp is None:
                    self.no_temp(4)
                else:
                    # pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    # card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com4_group:
                        if sprite.getposition() == self.lastcard4:
                            self.com4_group.remove(sprite)
                    self.player[4].remove(temp)
                    self.set_lastcard(self.lastcard4, (0, 0))
                    # card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                           (self.screen_width / 10, self.screen_height / 6))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    if self.difficulty == 2 and self.card_skill(t_card):
                        self.print_window()
                        pygame.display.update()
                        continue
                    self.card_skill(t_card)
                    self.print_window()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()

            elif self.now_turn == 5:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(6, self.player[5], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 3 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
                elif self.difficulty == 5:
                    temp = ai.special_play()
                if temp == 0 or temp is None:
                    self.no_temp(5)
                else:
                    # pygame.mixer.pre_init(44100, -16, 1, 512)
                    pygame.init()
                    # card = pygame.mixer.Sound('./sound/deal_card.wav')
                    for sprite in self.com5_group:
                        if sprite.getposition() == self.lastcard5:
                            self.com5_group.remove(sprite)
                    self.player[5].remove(temp)
                    self.set_lastcard(self.lastcard5, (0, 0))
                    # card.play()
                    self.waste_card.append(temp)
                    t_card = loadcard.Card(temp, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),
                                           (self.screen_width / 10, self.screen_height / 6))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    if self.difficulty == 2 and self.card_skill(t_card):
                        self.print_window()
                        pygame.display.update()
                        continue
                    self.card_skill(t_card)
                    self.print_window()
                    self.now_turn = self.next_turn(self.now_turn)
                    pygame.display.update()

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
                            self.now_turn = self.next_turn(self.now_turn)
                            break
                        else:
                            for sprite in self.user_group:
                                if sprite.get_name() == self.player[0][selected] and self.check_card(sprite):
                                    pygame.init()
                                    self.user_group.remove(sprite)
                                    self.player[0].remove(sprite.get_name())
                                    for temp in self.user_group:
                                        temp.move(sprite.getposition())
                                    sprite.setposition(self.screen_width * (3 / 5), self.screen_height * (1 / 3))
                                    self.put_waste_group(sprite)
                                    self.card_skill(sprite)
                                    if len(self.user_group) == 1:  # 카드 내고 한장 남음
                                        pygame.display.update()
                                        self.check_uno_button()
                                    else:
                                        self.now_turn = self.next_turn(self.now_turn)
                                    if selected > len(self.player[0]) - 1:
                                        selected = len(self.player[0]) - 1
                                    break
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    self.select_sound = pygame.mixer.Sound('./sound/card_sound.mp3')
                    self.select_sound.play()
                    if self.now_turn == 0:
                        self.select_player(self.now_turn)
                        for sprite in self.user_group:
                            if sprite.get_rect().collidepoint(mouse_pos) and self.check_card(sprite):
                                # pygame.mixer.pre_init(44100, -16, 1, 512)
                                pygame.init()
                                # card = pygame.mixer.Sound('./sound/deal_card.wav')
                                self.user_group.remove(sprite)
                                self.player[0].remove(sprite.get_name())
                                for temp in self.user_group:
                                    temp.move(sprite.getposition())
                                # 다시 보기
                                sprite.setposition(self.screen_width * (3 / 5), self.screen_height * (1 / 3))
                                # card.play()
                                self.put_waste_group(sprite)
                                self.card_skill(sprite)
                                if len(self.user_group) == 1:  # 카드 내고 한장 남음
                                    pygame.display.update()
                                    self.check_uno_button()
                                    # self.uno_click[0] = True
                                else:
                                    self.now_turn = self.next_turn(self.now_turn)
                                break
                        for sprite in self.deck_group:
                            if sprite.get_rect().collidepoint(mouse_pos):
                                self.get_from_deck(self.now_turn)
                                # self.show_uno()
                                self.now_turn = self.next_turn(self.now_turn)
                                break

            pygame.display.update()

    # 카드 뽑음
    def get_from_deck(self, now_turn):
        # pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        # deck = pygame.mixer.Sound('./sound/from_deck.wav')
        if self.card_deck:
            item = self.card_deck.pop(0)
        else:
            random.shuffle(self.waste_card)
            self.card_deck = self.waste_card[:-1]
            item = self.card_deck.pop()
        # deck.play()
        if now_turn == 0:
            temp = loadcard.Card(item, (self.screen_width * (2 / 5), self.screen_height * (1 / 3)),
                                 (self.screen_width / 10, self.screen_height / 6))
            current_pos = self.lastcard0
            if current_pos[0] >= self.screen_width*(28/30):
                y = current_pos[1] + self.screen_height/10
                x = self.screen_width*(1/3)
            else:
                y = current_pos[1]
                x = current_pos[0] + self.screen_width / 10
            temp.setposition(x, y)
            self.lastcard0 = (x, y)
            self.user_group.add(temp)
            self.player[0].append(item)
        elif now_turn == 1:
            temp = loadcard.Card('back', (350, 300), (self.screen_width / 30, self.screen_height / 18))
            current_pos = self.lastcard1
            if current_pos[0] >= self.screen_width * (1 / 6):
                y = current_pos[1] + self.screen_height / 30
                x = self.screen_width * (1 / 30)
            else:
                y = current_pos[1]
                x = current_pos[0] + 10
            temp.setposition(x, y)
            self.lastcard1 = (x, y)
            self.com1_group.add(temp)
            self.player[1].append(item)
        elif now_turn == 2:
            temp = loadcard.Card('back', (350, 300), (self.screen_width / 30, self.screen_height / 18))
            current_pos = self.lastcard2
            if current_pos[0] >= self.screen_width * (1 / 6):
                y = current_pos[1] + self.screen_height / 30
                x = self.screen_width * (1 / 30)
            else:
                y = current_pos[1]
                x = current_pos[0] + 10
            temp.setposition(x, y)
            self.lastcard2 = (x, y)
            self.com2_group.add(temp)
            self.player[2].append(item)
        elif now_turn == 3:
            temp = loadcard.Card('back', (350, 300), (self.screen_width / 30, self.screen_height / 18))
            current_pos = self.lastcard3
            if current_pos[0] >= self.screen_width * (1 / 6):
                y = current_pos[1] + self.screen_height / 30
                x = self.screen_width * (1 / 30)
            else:
                y = current_pos[1]
                x = current_pos[0] + 10
            temp.setposition(x, y)
            self.lastcard3 = (x, y)
            self.com3_group.add(temp)
            self.player[3].append(item)
        elif now_turn == 4:
            temp = loadcard.Card('back', (350, 300), (self.screen_width / 30, self.screen_height / 18))
            current_pos = self.lastcard4
            if current_pos[0] >= self.screen_width * (1 / 6):
                y = current_pos[1] + self.screen_height / 30
                x = self.screen_width * (1 / 30)
            else:
                y = current_pos[1]
                x = current_pos[0] + 10
            temp.setposition(x, y)
            self.lastcard4 = (x, y)
            self.com4_group.add(temp)
            self.player[4].append(item)

        elif now_turn == 5:
            temp = loadcard.Card('back', (350, 300), (self.screen_width / 30, self.screen_height / 18))
            current_pos = self.lastcard5
            if current_pos[0] >= self.screen_width * (1 / 6):
                y = current_pos[1] + self.screen_height / 30
                x = self.screen_width * (1 / 30)
            else:
                y = current_pos[1]
                x = current_pos[0] + 10
            temp.setposition(x, y)
            self.lastcard5 = (x, y)
            self.com5_group.add(temp)
            self.player[5].append(item)
        self.print_window()

    def set_lastcard(self, lastcard, compare_pos):
        x = lastcard[0]
        y = lastcard[1]

        i_x = compare_pos[0]
        i_y = compare_pos[1]

        if self.now_turn == 0:
            if x >= i_x + self.screen_width / 10 and y == i_y:
                x -= self.screen_width / 10

            elif y > i_y:
                if x <= self.screen_width / 3:
                    x = self.screen_width * (28 / 30)
                    y = y - self.screen_height / 10 
                else:
                    x -= self.screen_width / 10
            self.lastcard0 = (x, y)
        elif self.now_turn == 1:
            if x == self.screen_width * (1 / 6) and y > self.screen_height * (1 / 10):
                y -= self.screen_height * (1 / 30)
                x = self.screen_width * (1 / 6)
            else:
                x -= 10
            self.lastcard1 = (x, y)
        elif self.now_turn == 2:
            if x == self.screen_width * (1 / 6) and y > self.screen_height * (3 / 10):
                y -= self.screen_height * (1 / 30)
                x = self.screen_width * (1 / 6)
            else:
                x -= 10
            self.lastcard2 = (x, y)
        elif self.now_turn == 3:
            if x == self.screen_width * (1 / 6) and y > self.screen_height * (1 / 2):
                y -= self.screen_height * (1 / 30)
                x = self.screen_width * (1 / 6)
            else:
                x -= 10
            self.lastcard3 = (x, y)
        elif self.now_turn == 4:
            if x == self.screen_width * (1 / 6) and y > self.screen_height * (7 / 10):
                y -= self.screen_height * (1 / 30)
                x = self.screen_width * (1 / 6)
            else:
                x -= 10
            self.lastcard4 = (x, y)
        elif self.now_turn == 5:
            if x == self.screen_width * (1 / 6) and y > self.screen_height * (9 / 10):
                y -= self.screen_height * (1 / 30)
                x = self.screen_width * (1 / 6)
            else:
                x -= 10
            self.lastcard5 = (x, y)

    def put_waste_group(self, sprite):
        self.waste_group.add(sprite)
        self.waste_card.append(sprite.get_name())
        if len(self.waste_card) != 1:
            self.set_lastcard(self.lastcard0, sprite.getposition())
        self.print_window()

    def pause(self):

        paused = True
        self.playing_game = False

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭시 다시 시작
                    mouse_pos = pygame.mouse.get_pos()
                    self.playing_game = True
                    paused = False
                    if setting_button.get_rect().collidepoint(mouse_pos):
                        pass
                    elif exit_button.get_rect().collidepoint(mouse_pos):
                        terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing_game = True
                        paused = False

            pygame.draw.rect(self.screen, WHITE, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, BLACK, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400), 5)
            close_text = text_format("PAUSE", MALGUNGOTHIC, 60, BLACK)
            close_text_rect = close_text.get_rect(center=(self.screen_width/2,self.screen_height/3))
            setting_button = Button(self.screen, self.screen_width*(4/10), self.screen_height*(3/7), "image/playing_image/pause_setting.jpg", 150, 80)
            exit_button = Button(self.screen, self.screen_width*(4/10), self.screen_height*(3/7)+100, "image/playing_image/pause_end.jpg", 150, 80)
            setting_button.show_button()
            exit_button.show_button()
            self.screen.blit(close_text, close_text_rect)

            pygame.display.update()

    def change_color(self):
        if self.difficulty == 4 and self.game_turn % 5 == 0 and self.game_turn != 0:
            colors = ["red", "yellow", "green", "blue"]
            random_name = colors[random.randint(0, 3)]
            random_card = loadcard.Card(random_name, (self.screen_width * (3 / 5), self.screen_height * (1 / 3)),(self.screen_width/10,self.screen_height/6))
            self.waste_card.append(random_name)
            self.waste_group.add(random_card)
            self.print_window()

    def check_uno_button(self):
        uno = True
        start_time = time.time()
        while uno:  # 여기
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONUP or event.type == KEYDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # tnwjdgodigo
                    if self.uno_button.get_rect().collidepoint(mouse_pos) or event.type == K_SPACE:
                        end_time = time.time()
                        com_time = random.randint(1, 3)
                        if (end_time - start_time) > com_time:
                            if self.now_turn == 0:  # 유저 턴일 때
                                uno_text = text_format("uno", BERLIN, 30, (0, 0, 0))
                                self.screen.blit(uno_text, (45, 100))
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.next_turn(self.now_turn)
                                uno = False
                            else:  # 컴퓨터 턴일때 유저가 느리게 누름
                                self.now_turn = self.next_turn(self.now_turn)
                                uno = False
                        else:
                            if self.now_turn == 0:  # 유저 턴일 때
                                self.now_turn = self.next_turn(self.now_turn)
                                uno = False
                            else:  # 컴퓨터 턴일 때 유저가 빠르게 누름
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.next_turn(self.now_turn)
                                uno = False
            if (time.time() - start_time) > 3:
                if self.now_turn == 0:  # 그냥 버튼 안누르고 있을 때 5초 지나면 한 장 먹음
                    self.get_from_deck(self.now_turn)
                    self.now_turn = self.next_turn(self.now_turn)
                    uno = False
                else:  # 이건 컴퓨터가 1장 남았을 때 유저가 버튼을 안 누르고 있는 경우
                    if self.player_num == 2:  # 유저랑 컴퓨터 1명만 있는 경우 컴퓨터가 uno버튼 누른걸로 판단
                        self.now_turn = self.next_turn(self.now_turn)
                        uno = False
                    else:  # 다른 컴퓨터랑 경쟁
                        com_time = random.randint(0, 1)  # 그냥 0,1로 했어요..
                        if com_time == 1:  # 빠르게 누른 경우
                            self.now_turn = self.next_turn(self.now_turn)
                            uno = False
                        else:  # 느리게 누른 경우 - 카드 뽑음
                            self.get_from_deck(self.now_turn)
                            self.now_turn = self.next_turn(self.now_turn)
                            uno = False
            pygame.display.update()
