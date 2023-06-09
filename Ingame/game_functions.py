import sys
import random
import pygame
import math
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
from datetime import datetime
import UNO


def terminate():
    pygame.quit()
    sys.exit()


def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.SysFont(text_font, text_size)
    new_text = new_font.render(
        message, True, text_color)
    return new_text


class Game():
    def __init__(self, player_num=2, difficulty=1, user_name="ME"):  # 초기값 임시로 설정 - 지우기
        self.player_num = player_num
        self.difficulty = difficulty
        self.settings = s.Settings().get_setting()
        self.setting = s.Settings()
        self.keys = self.settings['keys']
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

        self.card_limit = [self.size[1] * (7 / 9), self.size[1] * (7 / 9) + self.size[1] / 10, self.size[1] * (
            7 / 9) + self.size[1] * 2 / 10, self.size[1] * (7 / 9) + self.size[1] * 3 / 10]

        self.uno_button = self.button_init()

        pygame.init()
        self.timer = timer.Timer()

        self.player = []
        self.card_deck = []
        self.waste = pl.Waste()
        self.player_names = []

        self.achv_alarm_li = []
        for achv_alarm in c.ACHV_ALARM_LIST:
            achv_alarm = rf.Button(self.screen, self.size[0] * (4 / 5), self.size[1] * (6 / 7),
                                   achv_alarm, self.size[0] * (1 / 5),
                                   self.size[1] * (1 / 7))
            self.achv_alarm_li.append(achv_alarm)

        self.selected = 0
        self.selected_up = 0

    def button_init(self):
        self.uno = 0
        button = rf.Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                           c.UNO_BUTTON, self.size[1] * (1 / 20),
                           self.size[1] * (1 / 20))
        button_highlight = rf.Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                                     c.UNO_BUTTON_HIGHLIGHT, self.size[1] * (
            1 / 20),
            self.size[1] * (1 / 20))
        return button, button_highlight

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
        self.uno_button[self.uno].show()
        self.show_now_turn(self.now_turn)

    def draw_color_rect(self):
        rect_pos = (self.size[0] * (3 / 4), self.size[1]
                    * (1 / 3) - self.size[1] * (1 / 20))
        rect_size = (self.size[1] * (1 / 20), self.size[1] * (1 / 20))
        half_rect_pos = (self.size[0] * (3 / 4) + self.size[1] *
                         (1 / 40), self.size[1] * (1 / 3) - self.size[1] * (1 / 20))
        half_rect_size = (self.size[1] * (1 / 40), self.size[1] * (1 / 20))

        if self.settings['setting_color'] == False:
            if len(self.waste.card) == 0:
                pygame.draw.rect(self.screen, c.BLACK, (rect_pos, rect_size))
            else:
                w_name = self.waste.card[-1]
                w_name = w_name.split('_')
                if w_name[0] == 'wild':
                    pygame.draw.rect(self.screen, c.BLACK,
                                     (rect_pos, rect_size))
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
                        pygame.draw.rect(self.screen, c.RED,
                                         (rect_pos, rect_size))
                elif w_name[0] == "yellow":
                    pygame.draw.rect(self.screen, c.YELLOW,
                                     (rect_pos, rect_size))
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
                    pygame.draw.rect(self.screen, c.GREEN,
                                     (rect_pos, rect_size))

        elif self.settings['setting_color'] == True:
            if len(self.waste.card) == 0:
                pygame.draw.rect(self.screen, c.BLACK, (rect_pos, rect_size))
            else:
                w_name = self.waste.card[-1]
                w_name = w_name.split('_')
                if w_name[0] == 'wild':
                    pygame.draw.rect(self.screen, c.BLACK,
                                     (rect_pos, rect_size))
                elif w_name[0] == "red":
                    if len(w_name) > 1:
                        if w_name[1] == 'yellow':
                            pygame.draw.rect(self.screen, c.VERMILION,
                                             (rect_pos, half_rect_size))
                            pygame.draw.rect(self.screen, c.YELLOW,
                                             (half_rect_pos, half_rect_size))
                        else:
                            pygame.draw.rect(self.screen, c.VERMILION,
                                             (rect_pos, rect_size))
                    else:
                        pygame.draw.rect(
                            self.screen, c.VERMILION, (rect_pos, rect_size))
                elif w_name[0] == "yellow":
                    pygame.draw.rect(self.screen, c.YELLOW,
                                     (rect_pos, rect_size))
                elif w_name[0] == "blue":
                    if len(w_name) > 1:
                        if w_name[1] == 'green':
                            pygame.draw.rect(self.screen, c.C_BLUE,
                                             (rect_pos, half_rect_size))
                            pygame.draw.rect(self.screen, c.BLUISH_GREEN,
                                             (half_rect_pos, half_rect_size))
                        else:
                            pygame.draw.rect(self.screen, c.C_BLUE,
                                             (rect_pos, rect_size))
                    else:
                        pygame.draw.rect(self.screen, c.C_BLUE,
                                         (rect_pos, rect_size))
                elif w_name[0] == "green":
                    pygame.draw.rect(
                        self.screen, c.BLUISH_GREEN, (rect_pos, rect_size))

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
        pass_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 3), self.settings['screen'][1] * (1 / 3), c.PASS, 150, 150)
        reverse_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 3), self.settings['screen'][1] * (1 / 3), c.REVERSE, 150, 150)
        change_button = rf.Button(self.screen, self.settings['screen'][0] * (
            1 / 3), self.settings['screen'][1] * (1 / 3), c.CHANGE, 150, 150)

        if name[1] == 'pass':
            pass_button.show()
            pygame.time.wait(500)
            self.now_turn = self.get_next_player(self.now_turn)
            self.first = False
        elif name[1] == 'reverse':
            if self.player_num == 2:
                reverse_button.show()
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
                change_button.show()
                pygame.time.wait(500)
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

    def user_skill_count(self):
        self.count = 0
        if self.card_skill == True:
            if self.now_turn == 0:
                self.count += 1

        if self.count >= 10:
            self.settings['win_count']['skill'] += 1
            start_time = time.time()
            if self.settings['win_count']['skill'] == 1 and not self.settings['achievement']['skill_master']:
                while time.time() - start_time < 5:
                    self.achv_alarm_li[10].show()
                self.settings['achievement']['skill_master'] = True
                self.settings['achievement']['skill_master'] = datetime.now().strftime(
                    '%Y-%m-%d')
                self.setting.change_setting(self.settings)

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
        # pygame.mixer.pre_init(44100, -16, 1, 512)
        # win = pygame.mixer.Sound('./sound/win.wav')
        # lose = pygame.mixer.Sound('./sound/lose.wav')
        pygame.draw.rect(self.screen, c.BLUE,
                         pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(self.screen, (255, 180, 0),
                         pygame.Rect(210, 210, 380, 180))
        restart = True
        if restart:
            self.settings['win_count']['first'] += 1
            if self.settings['win_count']['first'] == 1 and not self.settings['achievement']['first_play']:
                self.achv_alarm_li[7].show()
                pygame.display.update()
                pygame.time.wait(1500)
                self.settings['achievement']['first_play'] = True
                self.settings['achievement']['first_play'] = datetime.now().strftime(
                    '%Y-%m-%d')
                self.setting.change_setting(self.settings)

            for i in range(self.player_num):
                if len(self.player[i].group) == 0:
                    if i == 0:
                        close_text = text_format(
                            "YOU WIN!", c.BERLIN, 80, c.BLUE)
                        press_text = text_format(
                            "Press SPACE to MENU", c.BERLIN, 35, c.BLUE)
                        self.screen.blit(close_text, (230, 220))
                        pygame.display.update()
                        self.settings['win_count']['single'] += 1
                        if self.settings['win_count']['single'] == 1 and not self.settings['achievement']['single_win']:
                            self.achv_alarm_li[0].show()
                            pygame.display.update()
                            pygame.time.wait(1500)
                            self.settings['achievement']['single_win'] = True
                            self.settings['achievement_date']['single_win'] = datetime.now().strftime(
                                '%Y-%m-%d')
                            self.setting.change_setting(self.settings)

                        elif self.game_turn <= 10:
                            self.settings['win_count']['speed'] += 1
                            if self.settings['win_count']['speed'] == 1 and self.settings['achievement']['speed_win'] == False:
                                self.achv_alarm_li[5].show()
                                pygame.display.update()
                                pygame.time.wait(1500)
                                self.settings['achievement']['speed_win'] = True
                                self.settings['achievement_date']['speed_win'] = datetime.now().strftime(
                                    '%Y-%m-%d')
                                self.setting.change_setting(self.settings)

                        elif self.count == 0:
                            self.settings['win_count']['no_skill'] += 1
                            if self.settings['win_count']['no_skill'] == 1 and not self.settings['achievement']['no_skill_card']:
                                self.achv_alarm_li[6].show()
                                pygame.display.update()
                                pygame.time.wait(1500)
                                self.settings['achievement']['no_skill_card'] = True
                                self.settings['achievement_date']['no_skill_card'] = datetime.now().strftime(
                                    '%Y-%m-%d')
                                self.setting.change_setting(self.settings)

                        elif self.turtle_win == True:
                            self.settings['win_count']['turtle'] += 1
                            if self.settings['win_count']['turtle_win'] == 1 and not self.settings['achievement']['turtle_win']:
                                self.achv_alarm_li[7].show()
                                pygame.display.update()
                                pygame.time.wait(1500)
                                self.settings['achievement']['turtle_win'] = True
                                self.settings['achievement_date']['turtle_win'] = datetime.now().strftime(
                                    '%Y-%m-%d')
                                self.setting.change_setting(self.settings)
                        self.screen.blit(self.bg_img, (0, 0))
                        pygame.draw.rect(self.screen, c.BLUE,
                                         pygame.Rect(200, 200, 400, 200))
                        pygame.draw.rect(self.screen, (255, 180, 0),
                                         pygame.Rect(210, 210, 380, 180))
                        close_text = text_format(
                            "YOU WIN!", c.BERLIN, 80, c.BLUE)
                        press_text = text_format(
                            "Press SPACE to MENU", c.BERLIN, 35, c.BLUE)
                        self.screen.blit(close_text, (230, 220))
                        self.screen.blit(press_text, (228, 330))
                        pygame.display.update()
                    else:
                        close_text = text_format(
                            "YOU LOSE!, com{} win!".format(i), c.BERLIN, 40, c.BLUE)
                        press_text = text_format(
                            "Press SPACE to go MENU", c.BERLIN, 35, c.BLUE)
                        self.screen.blit(close_text, (230, 220))
                        self.screen.blit(press_text, (228, 330))
                        pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()

                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            restart = False
                            self.playing_game = False
                            self.setting.change_setting(self.settings)
                            UNO.TitleMenu().menu()
                            # 객체를 생성해서 호출하는게 좋지않을까? - 객체를 미리 생성하고 어떤 곳은 dictionary로 가더라 이것도 좋아
                            # 그리고 객체를 생성하면 업적이 망가지지 않을까?
                            return
            return 0

    # 리팩토링 match로 해도 될 것 같아
    def check_player(self):

        for i in range(self.player_num):
            if len(self.player[i].card) == 0:
                self.playing_game = False
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

            if len(self.player[0].group) >= 20:
                self.settings['win_count']['collector'] += 1
                start_time = time.time()
                if self.settings['win_count']['collector'] == 1 and not self.settings['achievement']['card_collector']:
                    while time.time() - start_time < 5:
                        self.achv_alarm_li[9].show()
                    self.settings['achievement']['card_collector'] = True
                    self.settings['achievement']['card_collector'] = datetime.now().strftime(
                        '%Y-%m-%d')
                    self.setting.change_setting(self.settings)

            self.print_window()
            pygame.display.update()

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
                if event.key == self.keys["left"]:
                    if self.selected <= 0:
                        self.selected = 0
                    else:
                        self.selected = self.selected - 1
                elif event.key == self.keys["right"]:
                    if self.selected >= len(self.player[0].card) - 1:
                        self.selected = len(self.player[0].card) - 1
                    else:
                        self.selected = self.selected + 1
                elif event.key == self.keys["up"]:
                    if self.selected_up == 0:
                        self.selected_up = 1
                    else:
                        self.selected_up = 1
                elif event.key == self.keys["down"]:
                    if self.selected_up == 1:
                        self.selected_up = 0
                    else:
                        self.selected_up = 0

                if event.key == self.keys["click"]:
                    if self.selected_up == 1:
                        self.get_from_deck(self.now_turn)
                        return 'Back'
                        # self.now_turn = self.get_next_player(self.now_turn)
                        # break
                    else:
                        for sprite in self.player[0].group:
                            if sprite.get_name() == self.player[0].card[self.selected] and self.check_card(sprite):
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
                                if self.selected > len(self.player[0].card) - 1:
                                    self.selected = len(
                                        self.player[0].card) - 1
                                break
            for sprite in self.player[0].draw_group:
                card_pos = sprite.getposition()
                if sprite.get_rect().collidepoint(pygame.mouse.get_pos()):
                    index = self.player[0].draw_group.sprites().index(sprite)
                    card = self.player[0].draw_group.sprites()[index]
                    if index >= 21:
                        if card.position[1] == self.card_limit[3]:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], card.position[1] - 20)
                    elif index >= 14:
                        if card.position[1] == self.card_limit[2]:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], card.position[1] - 20)
                    elif index >= 7:
                        if card.position[1] == self.card_limit[1]:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], card.position[1] - 20)
                    else:
                        if card.position[1] == self.card_limit[0]:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], card.position[1] - 20)

                    # if card.position[1] == self.card_limit[0]:
                    #     self.player[0].draw_group.sprites()[index].setposition(card.position[0], card.position[1] - 20)
                else:
                    index = self.player[0].draw_group.sprites().index(sprite)
                    card = self.player[0].draw_group.sprites()[index]
                    if index >= 21:
                        self.player[0].draw_group.sprites()[index].setposition(
                            card.position[0], self.card_limit[3])
                    elif index >= 14:
                        self.player[0].draw_group.sprites()[index].setposition(
                            card.position[0], self.card_limit[2])
                    elif index >= 7:
                        self.player[0].draw_group.sprites()[index].setposition(
                            card.position[0], self.card_limit[1])
                    else:
                        self.player[0].draw_group.sprites()[index].setposition(
                            card.position[0], self.card_limit[0])

            if event.type == MOUSEBUTTONUP:
                select_sound = pygame.mixer.Sound('./sound/card_sound.mp3')
                select_sound.play()
                if self.now_turn == 0:
                    # self.show_now_turn(self.now_turn)
                    for sprite in self.player[0].group:
                        index = self.player[0].group.index(sprite)
                        # index = self.player[0].draw_group.sprites().index(sprite)
                        card = self.player[0].draw_group.sprites()[index]
                        if index >= 21:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], self.card_limit[3])
                        elif index >= 14:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], self.card_limit[2])
                        elif index >= 7:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], self.card_limit[1])
                        else:
                            self.player[0].draw_group.sprites()[index].setposition(
                                card.position[0], self.card_limit[0])
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
            self.animate_card.update(
                (self.size[0] * (3 / 5), self.size[1] * (1 / 3)), 20)
            self.animation_group = pygame.sprite.RenderPlain(self.animate_card)
            s = self.animate_card.getposition()
            pos = (self.size[0] * (3 / 5), self.size[1] * (1 / 3))
            if self.animate_card.getposition() == (self.size[0] * (3 / 5), self.size[1] * (1 / 3)):
                return 0
        return 1

    def get_animation(self):
        if self.animation:
            self.animate_card.update(
                self.player[self.now_turn].last.getposition(), 20)
            self.animation_group = pygame.sprite.RenderPlain(self.animate_card)
            if self.animate_card.getposition() == self.player[self.now_turn].last.getposition():
                return 0
        return 1

    def animation(self, *temp):
        self.playing_game = False
        setting = 1

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
                        AchievementScreen().menu()
                    elif setting_button.get_rect().collidepoint(event.pos):
                        SettingScreen().menu()
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
            close_text = rf.TextRect(self.screen, "PAUSE", 60, c.BLACK)
            close_text.show((self.size[0] / 2, self.size[1] / 3))
            achievement_button = rf.Button(self.screen, self.size[0] * (4 / 9), self.size[1] * (1 / 2) - 70,
                                           "./image/playing_image/pause_achv.jpg", 100, 50)
            setting_button = rf.Button(self.screen, self.size[0] * (4 / 9), self.size[1] * (1 / 2),
                                       "./image/playing_image/pause_setting.jpg", 100, 50)
            exit_button = rf.Button(self.screen, self.size[0] * (4 / 9), self.size[1] * (1 / 2) + 70,
                                    "./image/playing_image/pause_end.jpg", 100, 50)
            achievement_button.show()
            setting_button.show()
            exit_button.show()

            pygame.display.update()

    def check_uno_button(self):
        self.turtle_win = False

        self.print_window()
        print("한장 남음!")
        uno = True
        start_time = time.time()
        while uno:  # 여기
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if self.uno_button[0].get_rect().collidepoint(mouse_pos):
                    self.uno_button[1].show()
                    pygame.display.update()
                else:
                    self.uno_button[0].show()
                    pygame.display.update()
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONUP or event.type == KEYDOWN:
                    if self.uno_button[0].get_rect().collidepoint(event.pos) or event.type == K_SPACE:
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
                                self.uno = 0
                                return 0
                            else:  # 컴퓨터 턴일때 유저가 느리게 누름
                                print("유저가 느리게 누름")
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                                self.uno = 0
                                return 0
                        else:
                            if self.now_turn == 0:  # 유저 턴일 때
                                print("빠르게 누름!")
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                                self.uno = 0
                                return 0
                            else:  # 컴퓨터 턴일 때 유저가 빠르게 누름
                                print("유저가 빠르게 누름!")
                                self.get_from_deck(self.now_turn)
                                # self.now_turn = self.get_next_player(
                                #     self.now_turn)
                                self.first = False
                                uno = False
                                self.uno = 0
                                return 0
            if (time.time() - start_time) > 3:
                if self.now_turn == 0:  # 그냥 버튼 안누르고 있을 때 5초 지나면 한 장 먹음
                    print("컴퓨터가 누름")
                    self.get_from_deck(self.now_turn)
                    # self.now_turn = self.get_next_player(self.now_turn)
                    self.first = False
                    uno = False
                    self.uno = 0
                    return 0
                else:  # 이건 컴퓨터가 1장 남았을 때 유저가 버튼을 안 누르고 있는 경우
                    self.turtle_win = True
                    if self.player_num == 2:  # 유저랑 컴퓨터 1명만 있는 경우 컴퓨터가 uno버튼 누른걸로 판단
                        print("컴퓨터가 누름")
                        # self.now_turn = self.get_next_player(self.now_turn)
                        self.first = False
                        uno = False
                        self.uno = 0
                        return 0
                    else:  # 다른 컴퓨터랑 경쟁
                        com_time = random.randint(0, 1)  # 그냥 0,1로 했어요.
                        if com_time == 1:  # 빠르게 누른 경우
                            print("컴퓨터가 누름")
                            # self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
                            self.uno = 0
                            return 0
                        else:  # 느리게 누른 경우 - 카드 뽑음
                            print("컴퓨터가 못 누름")
                            self.get_from_deck(self.now_turn)
                            # self.now_turn = self.get_next_player(self.now_turn)
                            uno = False
                            self.uno = 0
                            return 0


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

    def restart(self):
        if len(self.player[0].group) == 0:
            self.settings['win_count']['storya'] += 1
            if self.settings['win_count']['storya'] == 1 and not self.settings['achievement']['storya_win']:
                self.achv_alarm_li[1].show()
                pygame.display.update()
                pygame.time.wait(1500)
                self.settings['achievement']['storya_win'] = True
                self.settings['achievement_date']['storya_win'] = datetime.now().strftime(
                    '%Y-%m-%d')
                self.setting.change_setting(self.settings)
        return super().restart()


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
            self.settings['win_count']['storyb'] += 1
            if self.settings['win_count']['storyb'] == 1 and not self.settings['achievement']['storyb_win']:
                self.achv_alarm_li[2].show()
                pygame.display.update()
                pygame.time.wait(1500)
                self.settings['achievement']['storyb_win'] = True
                self.settings['achievement_date']['storyb_win'] = datetime.now().strftime(
                    '%Y-%m-%d')
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
            self.settings['win_count']['storyc'] += 1
            if self.settings['win_count']['storyc'] == 1 and not self.settings['achievement']['storyc_win']:
                self.achv_alarm_li[3].show()
                pygame.display.update()
                pygame.time.wait(1500)
                self.settings['achievement']['storyc_win'] = True
                self.settings['achievement_date']['storyc_win'] = datetime.now().strftime(
                    '%Y-%m-%d')
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
            self.settings['win_count']['storyd'] += 1
            if self.settings['win_count']['storyd'] == 1 and not self.settings['achievement']['storyd_win']:
                self.achv_alarm_li[4].show()
                pygame.display.update()
                pygame.time.wait(1500)
                self.settings['achievement']['storyd_win'] = True
                self.settings['achievement_date']['storyd_win'] = datetime.now().strftime(
                    '%Y-%m-%d')
                self.setting.change_setting(self.settings)
        return super().restart()


class SettingScreen():
    def __init__(self):
        self.setting = s.Settings()
        self.settings = self.setting.get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])

        self.button_li, self.slider_li, self.rect = self.object_init()
        self.setting_text = rf.TextRect(self.screen, "SETTING", 35, c.WHITE)
        self.screen_setting_text = rf.TextRect(
            self.screen, "화면 크기", 20, c.BLACK)
        self.volume = 0.0
        self.setting_run = True
        print(self.settings)

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
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for slider in self.slider_li:
                slider.operate(event)
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

            if event.type == pygame.MOUSEBUTTONUP and current_time - self.start_time >= 1:
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
                    self.setting_run = False

                elif self.button_li[4].get_rect().collidepoint(event.pos):
                    self.key_select_screen()  # 키보드 설정 함수 실행
                elif self.button_li[5].get_rect().collidepoint(event.pos):
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

    def bg_img_load(self, filename: str) -> object:
        bg_img = pygame.image.load(s.resource_path(filename))
        bg_img = pygame.transform.scale(bg_img,
                                        (self.settings['screen']))
        return self.screen.blit(bg_img, (0, 0))

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
                    pygame.quit()
                    sys.exit()

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
                        self.setting_run = False

                    elif save_button.get_rect().collidepoint(event.pos):
                        self.setting.change_setting(self.settings)

            pygame.display.update()

    def menu(self):
        selected = 1

        while True:
            self.bg_img_load(c.SETTING_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()


class AchievementScreen():
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
                    self.achv_run = False

        for achievement in self.achievement_li:
            achievement.y += scroll_pos

    def menu(self):
        while True:
            self.bg_img_load(c.SETTING_BACKGROUND)
            self.object_show()
            self.handle_event()

            pygame.display.update()
