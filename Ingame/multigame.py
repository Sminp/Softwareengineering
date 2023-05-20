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

class MutiGame():
    def __init__(self, player_list):
        self.player_list = player_list
        self.player_num = len(player_list)
        self.setting = s.Settings()
        self.player = []
        self.card_deck = []
        self.waste = []
        self.now_turn = None
        self.rotate = 0

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

    # 처음 카드 나눠준다 by 리스트
    def hand_out_deck(self):
        random.shuffle(self.card_deck)
        print("플레이어 수 {}".format(len(self.player_list)))
        for i in range(len(self.player_list)):
            temp_list = []
            for _ in range(0, 7):
                temp = self.card_deck.pop()
                temp_list.append(temp)
            self.player.append(temp_list)

    def get_next_player(self, now_turn):
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
    
    def selected_turn(self):
        return random.randint(0, self.player_num - 1)
    
    def card_change(self, now_turn, pick_turn):
        temp_player = self.player[now_turn]
        self.player[now_turn].clear()
        for item in self.player[pick_turn]:
            self.player[now_turn].append(item)
        self.player[pick_turn].clear()
        for item in temp_player:
            self.player[pick_turn].append(item)

    # 가장 적은 숫자 카드 나타내는 함수
    def least_num(self, my_index) -> int:
        least_player_idx = 0
        least_player_num = len(self.player[0])
        for num in range(1, self.player_num):
            if least_player_num > len(self.player[num]):
                if num != my_index:
                    least_player_idx = num
                    least_player_num = len(self.player[num])
        return least_player_idx
    
    # 다음 차례 플레이어에게 카드 뽑게 함 -> draw 카드
    def give_card(self, card_num):
        if len(self.waste) == 1:  # 처음 카드가 +2,+4일때 처음 플레이어가 카드 받음
            dest_player = self.now_turn
        else:
            dest_player = self.get_next_player(self.now_turn)
        for i in range(0, card_num):
            self.get_from_deck(dest_player)

    def get_from_deck(self, now_turn):
        if self.card_deck:
            item = self.card_deck.pop()
        else:
            random.shuffle(self.waste.card)
            self.card_deck = self.waste.card[:-1]
            item = self.card_deck.pop()
        self.player[now_turn].append(item)
    
    # 덱 세팅, 플레이어 세팅, 덱 분배
    def startgame(self):
        self.card_deck = self.set_deck()
        self.hand_out_deck()
        self.waste.append(self.card_deck.pop())
        self.now_turn = self.selected_turn()

    def restart(self): 
        for i in range(self.player_num):
            self.player[i].clear()
        self.waste.clear()
        self.card_deck.clear()
        self.startgame()


