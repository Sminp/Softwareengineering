import sys
import random
import pygame
import math
import loadcard
import computer
from pygame.locals import *
from constant import *
from UNO import Button, background_img_load, text_format, terminate


class Game():
    def __init__(self, player_num=2, difficulty=1,player_name ="ME"):  # 초기값 임시로 설정 - 지우기
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.FPS = 30

        self.player_num = player_num
        self.difficulty = difficulty
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
        self.color = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'wild'}
        self.skill = {11: '_pass', 12: '_reverse', 13: '_plus_two', 14: '_basic', 15: '_plus_four', 16: '_change'}
        self.card_deck = []
        self.player = [[0] for _ in range(0, self.player_num)]
        self.waste_group = pygame.sprite.RenderPlain()
        self.waste_card = []
        self.rotate = 0
        self.uno = 0
        self.playing_game = True
        self.game_turn = 0
        self.uno_button = Button(self.screen, 500, 300, "./image/UnoButton.png", 30, 30)
        self.first_show = True
        self.two_first_show = True
        self.time = 0
        self.active = False
        self.player_name = player_name
        self.first = True
        pygame.display.update()

    # 카드 생성
    def set_deck(self) -> list:
        card_deck = []
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
                    self.card_deck.append(now_card)
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
        return card_deck

    # 게임 시작 화면 - 덱 구성, 플레이어에게 카드 지급, 플레이어 숫자마다 카드 위치 다 다름 -> 5명까지 설정해야함
    def set_window(self):
        self.card_deck = self.set_deck()
        if self.difficulty == 1 or self.difficulty == 4:
            random.shuffle(self.card_deck)
            for player in range(0, self.player_num):
                card = []
                for number in range(0, 7):
                    temp = self.card_deck.pop(number)
                    card.append(temp)
                self.player[player] = card
        elif self.difficulty == 2:
            num_card = self.card_deck[:76]
            skill_card = self.card_deck[76:]
            random.shuffle(num_card)
            random.shuffle(skill_card)
            for player in range(1, self.player_num):
                card = []
                for number in range(0, 7):
                    if random.random() < 76 / 164:
                        temp = num_card.pop(number)
                    else:
                        temp = skill_card.pop(number)
                    card.append(temp)
                self.player[player] = card
            self.card_deck = num_card + skill_card
            del num_card, skill_card
            random.shuffle(self.card_deck)
            card = []
            for number in range(7):
                temp = self.card_deck.pop(number)
                card.append(temp)
            self.player[0] = card
        elif self.difficulty == 3:
            random.shuffle(self.card_deck)
            card_temp = self.card_deck[0]  # 첫번째 카드 미리 뽑아두기
            for player in range(0, self.player_num):
                card = []
                for number in range(0, len(self.card_deck) // self.player_num):  # 모든 카드 같은 수 만큼 플레이어에게 분배
                    temp = self.card_deck.pop(number)
                    card.append(temp)
                self.player[player] = card
            self.card_deck.append(card_temp)
        elif self.difficulty == 4:
            random.shuffle(self.card_deck)
            self.player_num = 3
            for player in range(0, self.player_num):
                card = []
                for number in range(0, 7):
                    temp = self.card_deck.pop(number)
                    card.append(temp)
                self.player[player] = card

        deck = loadcard.Card('back', (350, 300))
        self.deck_group = pygame.sprite.RenderPlain(deck)

        # 이거 왜 있어? init? 혹시 몰라서야? -> 엥 이거 왜 있지? 지워볼까?
        player_deck = self.player[0]
        init_card = []
        for item in player_deck:
            cards = loadcard.Card(item, (400, 300))
            init_card.append(cards)

        for i in range(len(self.player)):
            player_deck = self.player[i]
            if i == 0:
                user_card = []
                for item in player_deck:
                    cards = loadcard.Card(item, (400, 300))
                    user_card.append(cards)
            elif i == 1:
                com1_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (400, 300))
                    cards.rotation(180)
                    com1_card.append(cards)
            elif i == 2:
                com2_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (400, 300))
                    cards.rotation(270)
                    com2_card.append(cards)
            else:
                com3_card = []
                for _ in player_deck:
                    cards = loadcard.Card('back', (400, 300))
                    cards.rotation(90)
                    com3_card.append(cards)

        setting = True
        setting_user = 1
        setting_com1 = 1
        setting_com2 = 1
        setting_com3 = 1
        # 이게 뭐지?
        if self.player_num == 3:
            setting_com3 = 0
        elif self.player_num == 2:
            setting_com3 = 0
            setting_com2 = 0

        while setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            i = 0
            temp_list = []

            for item in user_card:
                item.update((200 + 70 * i, 500))
                temp_list.append(item)
                i += 1
            self.user_group = pygame.sprite.RenderPlain(*temp_list)

            # 이거 마지막 카드 겹쳐서 뒤로 갈까봐 한거야
            self.lastcard0 = temp_list[-1].getposition()
            if self.lastcard0 == (200 + 70 * (len(temp_list) - 1), 500):
                setting_user = 0

            i = 0
            temp_list = []
            setting = True
            for item in com1_card:
                item.update((270 + 40 * i, 100))
                temp_list.append(item)
                i += 1
            self.com1_group = pygame.sprite.RenderPlain(*temp_list)
            self.lastcard1 = temp_list[-1].getposition()
            if self.lastcard1 == (270 + 40 * (len(temp_list) - 1), 100):
                setting_com1 = 0

            if self.player_num >= 3:
                i = 0
                temp_list = []
                setting = True
                for item in com2_card:
                    item.update((80, 170 + 40 * i))
                    temp_list.append(item)
                    i += 1
                self.com2_group = pygame.sprite.RenderPlain(*temp_list)
                self.lastcard2 = temp_list[-1].getposition()
                if self.lastcard2 == (80, 170 + 40 * (len(temp_list) - 1)):
                    setting_com2 = 0

            if self.player_num == 4:
                i = 0
                temp_list = []
                setting = True
                for item in com3_card:
                    item.update((710, 170 + 40 * i))
                    temp_list.append(item)
                    i += 1
                self.com3_group = pygame.sprite.RenderPlain(*temp_list)
                self.lastcard3 = temp_list[-1].getposition()
                if self.lastcard3 == (710, 170 + 40 * (len(temp_list) - 1)):
                    setting_com3 = 0

            if setting_user == 0 and setting_com1 == 0 and setting_com2 == 0 and setting_com3 == 0:
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
            user_text = text_format(self.player_name, BERLIN, 30, (0, 0, 0))
            self.screen.blit(user_text, (165, 420))

        elif now_turn == 1:
            com1_text = text_format("COM1", BERLIN, 30, (0, 0, 0))
            self.screen.blit(com1_text, (235, 18))

        elif now_turn == 2:
            com2_text = text_format("COM2", BERLIN, 30, (0, 0, 0))
            self.screen.blit(com2_text, (45, 100))

        elif now_turn == 3:
            com3_text = text_format("COM3", BERLIN, 30, (0, 0, 0))
            self.screen.blit(com3_text, (675, 100))
        temp = self.get_next_player(now_turn)
        return temp

    def get_next_turn(self):
        if self.first:
            self.game_turn += 1
            self.change_color()
            pygame.time.wait(1000)
            print("turn", self.game_turn)
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
            user_text = text_format(self.player_name, BERLIN, 30, (255, 242, 0))
            self.screen.blit(user_text, (165, 420))
        elif now_turn == 1:
            com1_text = text_format("COM1", BERLIN, 30, (255, 242, 0))
            self.screen.blit(com1_text, (235, 18))
        elif now_turn == 2:
            com2_text = text_format("COM2", BERLIN, 30, (255, 242, 0))
            self.screen.blit(com2_text, (45, 100))
        else:
            com3_text = text_format("COM3", BERLIN, 30, (255, 242, 0))
            self.screen.blit(com3_text, (675, 100))
        pygame.display.update()

    # 플레이어 이름 표시 초기화
    def print_window(self, active=1):
        self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
        self.deck_group.draw(self.screen)
        self.user_group.draw(self.screen)
        self.com1_group.draw(self.screen)
        if self.player_num >= 3:
            self.com2_group.draw(self.screen)
            com2_text = text_format("COM2", BERLIN, 30, (0, 0, 0))
            self.screen.blit(com2_text, (45, 100))
        if self.player_num == 4:
            self.com3_group.draw(self.screen)
            com3_text = text_format("COM3", BERLIN, 30, (0, 0, 0))
            self.screen.blit(com3_text, (675, 100))
        user_text = text_format(self.player_name, BERLIN, 30, (0, 0, 0))
        self.screen.blit(user_text, (165, 420))
        com1_text = text_format("COM1", BERLIN, 30, (0, 0, 0))
        self.screen.blit(com1_text, (235, 18))
        self.waste_group.draw(self.screen)
        if len(self.waste_card) == 0:
            pygame.draw.rect(self.screen, BLACK, (500, 500, 100, 100))
        else:
            w_name = self.waste_card[-1]
            w_name = w_name.split('_')
            if w_name[0] == 'wild':
                pygame.draw.rect(self.screen, BLACK, (500, 500, 100, 100))
            elif w_name[0] == "red":
                if len(w_name) > 1:
                    if w_name[1] == 'yellow':
                        pygame.draw.rect(self.screen, RED, (500, 500, 50, 100))
                        pygame.draw.rect(self.screen, YELLOW, (550, 500, 50, 100))
                    else:
                        pygame.draw.rect(self.screen, RED, (500, 500, 100, 100))
                else:
                    pygame.draw.rect(self.screen, RED, (500, 500, 100, 100))
            elif w_name[0] == "yellow":
                pygame.draw.rect(self.screen, YELLOW, (500, 500, 100, 100))
            elif w_name[0] == "blue":
                if len(w_name) > 1:
                    if w_name[1] == 'green':
                        pygame.draw.rect(self.screen, BLUE, (500, 500, 50, 100))
                        pygame.draw.rect(self.screen, GREEN, (550, 500, 50, 100))
                    else:
                        pygame.draw.rect(self.screen, BLUE, (500, 500, 100, 100))
                else:
                    pygame.draw.rect(self.screen, BLUE, (500, 500, 100, 100))
            elif w_name[0] == "green":
                pygame.draw.rect(self.screen, GREEN, (500, 500, 100, 100))
            if active:
                self.show_uno()
            else:
                self.uno_button.cliked()

    # 낼 수 있는지 확인
    def check_card(self, sprite):
        if len(self.waste_card) == 0:
            return True
        else:
            name = sprite.get_name()
            name = name.split('_')
            w_name = self.waste_card[-1]
            w_name = w_name.split('_')
            if w_name[0] == 'wild':
                return True
            if name[0] == 'wild':
                return True
            if len(name) < 3 or len(w_name) < 3:
                if w_name[0] == name[0]:
                    return True
                if len(name) > 1 and len(w_name) > 1:
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
                                                                                                                                                                                                
                if index == 1 :
                    print("바꾸기 전 player0 덱: {}".format(self.player[0]))
                    print("바꾸기 전 player1 덱: {}".format(self.player[1]))

                    # player 0의 카드 임시 저장
                    temp_player0 = []
                    for item in self.player[0]:
                        temp_player0.append(item)
                    
                    # 이게 왜 안될까요..?
                    # temp_player0 = self.player[0]
                    

                    # 마지막 카드 위치 처음으로 
                    self.lastcard0 = (130,500)
                    self.lastcard1 = (230,100)

                    # 플레이어 초기화
                    self.player[0].clear()
                    for sprite in self.user_group:
                        self.user_group.remove(sprite)

                    print("초기화 후 player0 덱: {}".format(self.player[0]))

                    # 컴퓨터 덱을 플레이어 덱으로 
                    for item in self.player[1]:
                        card = loadcard.Card(item,(400,300))
                        current_pos = self.lastcard0
                        if current_pos[0] >= 620:
                            y = current_pos[1] + 80
                            x = 200
                        else:
                            y = current_pos[1]
                            x = current_pos[0] + 70
                        card.setposition(x, y)
                        self.lastcard0 = (x, y)
                        self.user_group.add(card)

                    print("변경 후 user_group: {}".format(self.user_group))
                    for item in self.player[1]:
                        self.player[0].append(item)
                    # self.player[0] = self.player[1]
                    print("변경 후 player0 덱: {}".format(self.player[0]))

                    # 컴퓨터 초기화
                    self.player[1].clear()
                    for sprite in self.com1_group:
                        self.com1_group.remove(sprite)

                    print("초기화 후 com1_group: {}".format(self.com1_group))
                    print("초기화 후 player1 : {}".format(self.player[1]))
                    print("temp: {}".format(temp_player0))
    
                    # 플레이어 덱을 컴퓨터 덱으로 
                    for i in range(len(temp_player0)):
                        card = loadcard.Card("back",(400,300))
                        card.rotation(180)
                        current_pos = self.lastcard1
                        if current_pos[0] >= 510:
                            y = current_pos[1] +  40
                            x = 270
                        else:
                            y = current_pos[1]
                            x = current_pos[0] + 40
                        card.setposition(x, y)
                        self.lastcard1 = (x, y)
                        self.com1_group.add(card)
                    self.player[1] = temp_player0
                    print("변경 후 com1_group: {}".format(self.com1_group))
                    print("변경 후 player1 덱: {}".format(self.player[1]))
                    print("바꾼 후 player0 덱: {}".format(self.player[0]))
                    print("바꾼 후 player1 덱: {}".format(self.player[1]))
                    self.print_window()

                # elif index == 2: # 이거 함수 복붙인데 새로 만들까?! 밑에도 계속 쓰일 것 같긴해..
                #     self.player[0],self.player[2] = self.player[2], self.player[0]
                
            elif self.now_turn == 1:
                pygame.time.wait(500)
                if self.check_card_num(self.player) == 0:
                    self.player[0],self.player[1] = self.player[1], self.player[0]
                    temp = self.user_group
                    temp1 = self.com1_group
                    self.com1_group = temp
                    self.user_group = temp1
                    self.user_group.draw(self.screen)
                    self.com1_group.draw(self.screen)
                # elif self.check_card_num(self.player) == 1: # 이렇게 다 하나하나 해야해서..
            elif self.now_turn == 2:
                pygame.time.wait(500)
                self.player[2], self.player[self.check_card_num(self.player)] = self.player[
                                                                                    self.check_card_num(self.player)], \
                                                                                self.player[2]
                print(self.player[2],"==>" ,self.player[2])
            elif self.now_turn == 3:
                pygame.time.wait(500)
                self.player[3], self.player[self.check_card_num(self.player)] = self.player[
                                                                                    self.check_card_num(self.player)], \
                                                                                self.player[3]
                print(self.player[3],"==>", self.player[3])
                pygame.time.wait(500)
                self.now_turn = self.next_turn(self.now_turn)

        elif name[1] == 'plus':
            if name[2] == 'two':
                pygame.time.wait(500)
                self.give_card(2)
                # self.now_turn = self.next_turn(self.now_turn)
            elif name[2] == 'four':
                # pygame.mixer.pre_init(44100, -16, 1, 512)
                pygame.init()
                # select = pygame.mixer.Sound('./sound/select.wav')
                # select.play()
                self.give_card(4)
                self.pick_color_card()
        elif name[0] == 'wild':
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # select = pygame.mixer.Sound('./sound/select.wav')
            # select.play()
            self.pick_color_card()
        else:
            if self.now_turn != 0:
                return False
        self.show_uno()
        return True

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
        temp = loadcard.Card(temp_name, (430, 300))
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
                            temp = loadcard.Card(temp_name, (430, 300))
                            self.waste_card.append(temp_name)
                            self.waste_group.add(temp)
                            self.print_window()
                            loop = False
        return 0

    # change 카드를 컴퓨터 플레이어가 선택할 때 제일 카드가 적은 플레이어 선택
    def check_card_num(self, player_deck_list):
        shortest_list = min(player_deck_list, key=len)
        print("작동")  # 두번작동
        return player_deck_list.index(shortest_list)

    def check_two(self) -> bool:
        if self.player_num <= 2:
            len_min = min(len(self.user_group), len(self.player[1]))
            if 1 <= len_min <= 2:
                return True
        elif self.player_num == 3:
            len_min = min(len(self.user_group), len(self.player[1]), len(self.player[2]))
            if 1 <= len_min <= 2:
                return True
        elif self.player_num == 4:
            len_min = min(len(self.user_group), len(self.player[1]), len(self.player[2]), len(self.player[3]))
            if 1 <= len_min <= 2:
                return True
        return False

    def check_uno(self) -> bool:
        if self.player_num <= 2:
            len_min = min(len(self.user_group), len(self.player[1]))
            if len_min == 1:
                return True
        elif self.player_num == 3:
            len_min = min(len(self.user_group), len(self.player[1]), len(self.player[2]))
            if len_min == 1:
                return True
        elif self.player_num == 4:
            len_min = min(len(self.user_group), len(self.player[1]), len(self.player[2]), len(self.player[3]))
            if len_min == 1:
                return True
        return False

    def set_uno_timer(self) -> bool:
        if self.difficulty == 1:
            self.time = random.randint(500, 1000)
        elif self.difficulty == 2:
            self.time = random.randint(300, 1000)
        else:
            self.time = random.randint(0, 1000)
        return True

    def uno_clicked(self, active=False):
        if active:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if 500 <= mouse_pos[0] <= 530 and 300 <= mouse_pos[1] <= 330:
                        return True
        return False

    def show_uno(self) -> object:
        if self.check_two():
            if self.check_uno() and self.two_first_show:
                self.uno_button.cliked()
                self.print_window(0)
                if self.first_show:
                    self.set_uno_timer()
                    print(self.time)
                    self.first_show = False
                    self.active = True
                self.time -= 10
                if self.time <= 0:
                    if self.now_turn == 0:
                        self.get_from_deck(self.now_turn)
                        pygame.time.wait(1000)
                        pygame.display.update()
                    self.two_first_show = False
                    print("컴퓨터")
                    return 0
                elif self.uno_clicked(self.active):
                    print("YEAH")
                    if self.now_turn == 0:
                        pass
                    else:
                        self.get_from_deck(self.now_turn)
                        pygame.time.wait(1000)
                        pygame.display.update()
                        self.two_first_show = False
                        self.active = False
                        return 0
                    print(1)
                    self.two_first_show = False
                    self.active = False
                    print(self.two_first_show)
                    return 0
                return 0
            else:
                self.uno_button.show_botton()
            self.two_first_show = True
            self.first_show = True


    # change 카드 사용할 때 바꿀 플레이어 선택
    def pick_player(self):
        pick_player_button = [Button(self.screen, 350, 100 + i * 120, "./image/button_img.png", 100, 100) for i in
                              range(self.player_num - 1)]
        index = 0

        loop = True
        while loop:
            for i in range(self.player_num - 1):
                pick_player_button[i].show_botton()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(self.player_num - 1):
                        if pick_player_button[i].x <= mouse_pos[0] <= pick_player_button[i].width + pick_player_button[
                            i].x and pick_player_button[i].y <= mouse_pos[1] <= pick_player_button[i].y + \
                                pick_player_button[i].height:
                            index = i
                            print("바꿀사람:{}".format(index + 1))
                            self.print_window()
                            loop = False

        return index + 1

    # 다음 차례 플레이어에게 카드 뽑게 함 -> draw 카드
    def give_card(self, card_num):
        if len(self.waste_card) == 1 : # 처음 카드가 +2,+4일때 처음 플레이어가 카드 받음
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
                        self.startgame()
                        return
        return 0

    def no_temp(self, now_turn: int):
        self.get_from_deck(now_turn)
        self.print_window()
        self.now_turn = self.next_turn(self.now_turn)
        pygame.display.update()

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

        while self.playing_game:
            if len(self.user_group) == 0:
                self.restart()
                return
            elif self.player_num == 4:
                if len(self.player[1]) == 0 or len(self.player[2]) == 0 or len(self.player[2]) == 0:
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

            self.show_uno()
            self.select_player(self.now_turn)
            if self.now_turn == 0 and len(self.waste_card) == 0:
                temp = loadcard.Card(self.card_deck.pop(), (430, 300))
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
                if self.difficulty == 1 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
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
                    t_card = loadcard.Card(temp, (430, 300))
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

            elif self.now_turn == 2:
                self.select_player(self.now_turn)
                pygame.time.wait(1000)
                pygame.time.wait(1000)
                ai = computer.AI(3, self.player[2], self.waste_card)
                if self.difficulty == 1 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
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
                    t_card = loadcard.Card(temp, (430, 300))
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
                if self.difficulty == 1 or self.difficulty == 4:
                    temp = ai.basic_play()
                elif self.difficulty == 2:
                    next = self.get_next_player(self.now_turn)
                    if next == 0:
                        next_ = self.user_group
                    else:
                        next_ = self.player[next]
                    temp = ai.advanced_play(next_)
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
                    t_card = loadcard.Card(temp, (430, 300))
                    self.waste_group.add(t_card)
                    self.print_window()
                    pygame.display.update()
                    if self.difficulty == 2 and self.card_skill(t_card):
                        self.print_window()
                        pygame.display.update()
                        continue
                    self.card_skill(t_card)
                    self.print_window()
                    print("computer lastcard", self.lastcard3)
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

                if event.type == MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
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
                                sprite.setposition(430, 300)
                                # card.play()
                                self.put_waste_group(sprite)
                                self.card_skill(sprite)
                                self.now_turn = self.next_turn(self.now_turn)
                                break
                        for sprite in self.deck_group:
                            if sprite.get_rect().collidepoint(mouse_pos):
                                self.get_from_deck(self.now_turn)
                                self.show_uno()
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
            temp = loadcard.Card(item, (400, 300))
            current_pos = self.lastcard0
            if current_pos[0] >= 620:
                y = current_pos[1] + 80
                x = 200
            else:
                y = current_pos[1]
                x = current_pos[0] + 70
            temp.setposition(x, y)
            self.lastcard0 = (x, y)
            self.user_group.add(temp)
            self.player[0].append(item)
        elif now_turn == 1:
            temp = loadcard.Card('back', (350, 300))
            temp.rotation(180)
            current_pos = self.lastcard1
            if current_pos[0] >= 510:
                y = current_pos[1] + 40
                x = 270
            else:
                y = current_pos[1]
                x = current_pos[0] + 40
            temp.setposition(x, y)
            self.lastcard1 = (x, y)
            self.com1_group.add(temp)
            self.player[1].append(item)
        elif now_turn == 2:
            temp = loadcard.Card('back', (350, 300))
            current_pos = self.lastcard2
            temp.rotation(90)
            if current_pos[1] >= 410:
                y = 170
                x = current_pos[0] + 40
            else:
                y = current_pos[1] + 40
                x = current_pos[0]
            temp.setposition(x, y)
            self.lastcard2 = (x, y)
            self.com2_group.add(temp)
            self.player[2].append(item)
        elif now_turn == 3:
            temp = loadcard.Card('back', (350, 300))
            current_pos = self.lastcard3
            temp.rotation(270)
            if current_pos[1] >= 410:
                y = 170
                x = current_pos[0] + 40
            else:
                y = current_pos[1] + 40
                x = current_pos[0]
            temp.setposition(x, y)
            self.lastcard3 = (x, y)
            self.com3_group.add(temp)
            self.player[3].append(item)
        self.print_window()

    def set_lastcard(self, lastcard, compare_pos):
        x = lastcard[0]
        y = lastcard[1]

        i_x = compare_pos[0]
        i_y = compare_pos[1]

        if self.now_turn == 0:
            if x >= i_x + 60 and y == i_y:
                x -= 70

            elif y > i_y:
                if x <= 200:
                    x = 620
                    y = y - 80
                else:
                    x -= 70
            self.lastcard0 = (x, y)
        elif self.now_turn == 1:
            if y > 100 and x == 270:
                y -= 40
                x = 510
            else:
                x -= 40
            self.lastcard1 = (x, y)
        elif self.now_turn == 2:
            if x > 80 and y == 170:
                x -= 40
                y = 410
            else:
                y -= 40
            self.lastcard2 = (x, y)
        elif self.now_turn == 3:
            if x > 710 and y == 170:
                x -= 40
                y = 410
            else:
                y -= 40
            self.lastcard3 = (x, y)

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
                    self.playing_game = True
                    paused = False
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 3 - 100, 400, 400), 5)
            close_text = text_format("PAUSE", 'Berlin Sans FB', 80, (255, 51, 0))
            self.screen.blit(close_text, (230, 220))

            pygame.display.update()

    def change_color(self):
        if self.difficulty == 4 and self.game_turn % 5 == 0 and self.game_turn != 0:
            print("실행")
            colors = ["red", "yellow", "green", "blue"]
            random_name = colors[random.randint(0, 3)]
            random_card = loadcard.Card(random_name, (430, 300))
            self.waste_card.append(random_name)
            self.waste_group.add(random_card)
            print("바뀐 색:" + random_name)
            self.print_window()
