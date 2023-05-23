import socket
import pickle
import pygame
from network import Network
from constant import *
from rect_functions import Button, Slider, TextRect
from settings import Settings, resource_path
import sys
import time
import game_functions as gf
import constant as c
import player as pl
import settings as s
import computer as com
import loadcard as lc
import rect_functions as rf
import timer
import time
import math
from client_player import ClientUser
from player import User, Waste, Computer
import random

class Client:
    def __init__(self, screen, password, user_name, ip_address):
        self.password = password
        self.user_name = user_name
        self.screen = screen
        self.settings = Settings().get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = self.settings['screen']
        self.n = Network(ip_address)
        self.font = pygame.font.SysFont(self.settings['font'], 30)
        self.button, self.text_list, self.player_rect = self.object_init()
        self.user_name_text = TextRect(self.screen, self.user_name, 30, BLACK)
        self.input_active = False
        self.lobby_run = True
        self.game_run = False
        self.waste = []
        self.user = []
        self.rotate = 0
        self.card_size = (self.settings['screen']
                          [0] / 10, self.settings['screen'][1] / 6)
        self.uno_button = rf.Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                                    c.UNO_BUTTON, self.size[1] * (1 / 20),
                                    self.size[1] * (1 / 20))
        self.bg_img = pygame.transform.scale(pygame.image.load(s.resource_path(
            c.GAME_BACKGROUND)), (self.settings['screen']))
    

    def show_error_msg(self, image_path):
        image = pygame.transform.scale(pygame.image.load(resource_path(image_path)), [
                                       self.settings['screen'][0] / 2, self.settings['screen'][1] / 2])
        rect = image.get_rect()
        rect.center = (self.settings['screen'][0] / 2,
                       self.settings['screen'][1] / 2)
        self.screen.blit(image, rect)
        pygame.display.update()
        time.sleep(2)
        self.screen.fill(WHITE)
        pygame.display.update()

    def lobby(self):

        p = self.n.getP()

        pygame.init()
        self.screen.fill(WHITE)
        pygame.display.update()
    
        reply = self.n.send({"password": ''})
        if reply["password"] != self.password:
            self.n.client.close()
            return False

        if p != 0:
            reply = self.n.send({'get_players': ''})
            if len(reply['players']) >= 6:
                reply = self.n.send({'full': True})
                self.show_error_msg(c.ERROR_MSG)
                self.n.client.close()
                return False
            else:
                reply = self.n.send({"add_players": self.user_name})
        else:
            reply = self.n.send({"add_players": self.user_name})
            reply = self.n.send({'full': False})

        while self.lobby_run:
            try:
                reply = self.n.send({'get_players': ''})
                index = reply['players'].index(self.user_name)
                self.object_show(reply['players'], index)
                self.handle_event(index)
                reply = self.n.send({'is_start': ''})
                if reply['start'] == True:
                    self.game_screen()
                    self.lobby_run = False
                # 수정 필요 reply['full']이 계속 False여서 안들어가짐
                if p == 0 and reply['full'] == True:
                    self.show_error_msg(c.ERROR_MSG)
                    self.n.send({'full': False})

            except Exception as e:
                print(str(e))
                pygame.quit()
                sys.exit()

    def init_player_list(self, list, index):
        for i in range(len(list)):
            if self.player_rect[i][1] != list[i]:
                if i == index:
                    name = TextRect(self.screen, list[i], 30, BLACK)
                    self.player_rect[i][1] = name
                else:
                    self.player_rect[i][1] = list[i]
        for j in range(len(list), 5):
            self.player_rect[j][1] = ''

    def object_init(self):
        player_rect = [[pygame.Rect(self.settings['screen'][0] / 2, self.settings['screen'][1] * (
            2 / 3), self.settings['screen'][0] / 5, self.settings['screen'][1] / 6), '']]
        button = Button(self.screen, self.settings['screen'][0] * (4 / 9), self.settings['screen'][0] * (1 / 4),
                        GAMESTART_BUTTON, self.settings['screen'][0] * (1 / 4), self.settings['screen'][1] * (1 / 5))
        text_list = [TextRect(self.screen, "방장", 30, BLACK), TextRect(
            self.screen, "IP 주소:" + str(socket.gethostbyname(socket.gethostname())), 40, BLACK)]
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.settings['screen'][1] - 500) / 6),
                               self.settings['screen'][0] / 5, self.settings['screen'][1] / 6)
            player_rect.append([rect, ""])
        return button, text_list, player_rect

    def object_show(self, list, index):
        self.screen.fill(WHITE)
        self.button.show()
        # 모두에게 방장 표시, 방장의 화면에만 ip 주소 표시
        self.text_list[0].show(
            (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] * (3 / 5)))
        if self.n.getP() == 0:
            self.text_list[1].show(
                (self.settings['screen'][0] * (3 / 5), self.settings['screen'][1] / 6))

        self.init_player_list(list, index)
        for rect, label in self.player_rect:
            pygame.draw.rect(self.screen, GRAY, rect)
            if type(label) == str:
                label_surface = self.font.render(label, True, BLACK)
                label_rect = label_surface.get_rect()
                label_rect.center = rect.center
                self.screen.blit(label_surface, label_rect)
            else:
                label.show((rect.center))

        if self.input_active:
            pygame.draw.rect(self.screen, YELLOW, self.player_rect[index][0])
            self.player_rect[index][1].show(
                (self.player_rect[index][0].center))

        pygame.display.update()

    def sound(self):
        pass

    def handle_event(self, index):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.n.send({'disconnect': self.n.getP()})
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.player_rect[index][0].collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False

                if self.n.getP() == 0:  # 방장일 경우 해당 플레이어를 클릭하면 강퇴
                    for i in range(1, len(self.player_rect)):
                        if self.player_rect[i][0].collidepoint(event.pos):
                            if self.player_rect[i][1] != '' and self.player_rect[i][1] != 'computer':
                                self.n.send({'kick': i})
                            else:  # 아직 컴퓨터 지우는 거는 추가 안함
                                self.player_rect[i][1] = 'computer'
                                self.n.send({'add_players': 'computer'})
                    if self.button.get_rect().collidepoint(event.pos):
                        self.n.send({'start':True})

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        if len(self.user_name) > 10:
                            self.user_name = self.user_name
                        else:
                            self.user_name += event.unicode
                    self.player_rect[index][1].change_text_surface(
                        self.user_name)
                    msg = self.user_name+','+str(index)
                    reply = self.n.send({"change_name": msg})

    def game_screen(self):
        pygame.init()
        reply = self.n.send({'get_players': ''})
        self.index = reply['players'].index(self.user_name)
        reply = self.n.send({'game': ''})
        self.player_num = len(reply['players'])
        game = reply['game']
        self.waste = Waste()
        self.waste.set_card()
        # self.waste.updating(game.waste[0])
        self.player_user = Multiplayer()
        for item in game.player[self.index]:
            self.player_user.append(item)
        self.player_user.set_card()
        self.player_user.set()
        self.other = []
        for i in range(1, self.player_num):
            self.other.append(Computer(i))
        self.other_index = []
        j = 0
        for i in range(self.player_num):
            if i != self.index:
                for item in game.player[i]:
                    self.other[j].append(item)
                self.other[j].set_card()
                self.other[j].set()
                self.other_index.append((i,j))
                j += 1
        self.game_run = True
        self.set_name(reply['players'])
        print(game.now_turn)
        while self.game_run:
            reply = self.n.send({'game': ''})
            self.now_turn = reply['game'].now_turn
            if len(self.waste.card) != 0 :
                if self.waste.card[-1] != reply['game'].waste[-1]:
                    self.waste.updating(reply['game'].waste[-1])
            self.screen.blit(self.bg_img, (0, 0))
            self.draw_color_rect()
            self.uno_button.show()
            for rect in self.print_computer_box():
                pygame.draw.rect(self.screen, c.WHITE, rect)
            self.waste.draw_group.draw(self.screen)
            if self.player_user.card != reply['game'].player[self.index]:
                self.player_user.clear()
                self.player_user.card = reply['game'].player[self.index]
                self.player_user.set_card()
                self.player_user.set()
            self.player_user.draw_group.draw(self.screen)
            for i in range(len(self.other)):
                index = self.other_index[i]
                if self.other[index[1]].card != reply['game'].player[index[0]]:
                    self.other[index[1]].clear()
                    self.other[index[1]].card = reply['game'].player[index[0]]
                    self.other[index[1]].set_card()
                    self.other[index[1]].set()
                self.other[i].draw_group.draw(self.screen)
            self.show_now_turn(self.now_turn)
            if len(self.waste.card) == 0:
                self.waste.updating(reply['game'].waste[0])
                self.card_skill(self.waste.card[-1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.n.send({'disconnect': self.n.getP()})
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    select_sound = pygame.mixer.Sound('./sound/card_sound.mp3')
                    select_sound.play()
                    if self.now_turn == self.index:
                        for sprite in self.player_user.group:
                            if sprite.get_rect().collidepoint(event.pos) and self.check_card(sprite):
                                self.player_user.remove(sprite)
                                self.n.send({'put_card': [self.index, sprite.get_name()]})
                                self.waste.updating(sprite.get_name())
                                self.n.send({'waste':sprite.get_name()})
                                self.card_skill(sprite.get_name())
                                self.now_turn = self.get_next_player(self.now_turn)
                                self.n.send({'next_turn': self.now_turn})
                        for sprite in self.waste.group:
                            if sprite.get_rect().collidepoint(event.pos):
                                self.get_from_deck(self.now_turn)
                                self.now_turn = self.get_next_player(self.now_turn)
                                self.n.send({'next_turn': self.now_turn})

            pygame.display.update()

    def set_name(self, list): 
        self.player_names = []
        i = 1
        for name in list:
            if name == self.user_name:
                text = rf.TextRect(self.screen, self.user_name, 30, c.WHITE)
                self.player_names.append(
                    [text, (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
            else:
                text = rf.TextRect(self.screen, name, 20, c.BLACK)
                self.player_names.append(
                    [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
                i += 1

        print(self.player_names)
        return self.player_names
    
    def show_now_turn(self, now_turn):

        for i, text in enumerate(self.player_names):
            if i == now_turn:
                text[0].change_color(c.YELLOW)
                text[0].show(text[1])
            else:
                text[0].change_color(c.BLACK)
                text[0].show(text[1])

        pygame.display.update()

    def get_from_deck(self, now_turn):
        reply = self.n.send({'get_from_deck': now_turn})
        if now_turn == self.index:
            i = len(reply['game'].player[self.index]) - len(self.player_user.card)
            j = len(reply['game'].player[self.index]) - 1 
            for _ in range(i):
                self.player_user.add_card(reply['game'].player[self.index][j])
                j -= 1
        else:
            for index in self.other_index:
                if now_turn == index[0]:
                    i = len(reply['game'].player[index[0]]) - len(self.other[index[1]].card)
                    j = len(reply['game'].player[index[0]]) - 1
                    for _ in range(i):
                        self.other[index[1]].add_card(reply['game'].player[index[0]][j])
                        j -= 1

    def card_skill(self, name):
        name = name.split('_')
        if name[1] == 'pass':
            pygame.time.wait(500)
            self.now_turn = self.get_next_player(self.now_turn)
            self.n.send({'next_turn': self.now_turn})
        elif name[1] == 'reverse':
            if self.player_num == 2:
                pygame.time.wait(500)
                self.now_turn = self.get_next_player(self.now_turn)
                self.n.send({'next_turn': self.now_turn})
            else:
                if self.rotate == 0:
                    self.rotate = 1
                else:
                    self.rotate = 0
        elif name[1] == 'change':
            if self.now_turn == self.index:
                index = self.pick_player()
                self.n.send({'card_change': [self.now_turn, index]})

        elif name[1] == 'plus':
            if name[2] == 'two':
                pygame.time.wait(500)
                reply = self.n.send({'game': ''})
                if len(reply['game'].card_deck) < 2:
                    pass
                else:
                    self.give_card(2)
            elif name[2] == 'four':
                reply = self.n.send({'game': ''})
                if len(reply['game'].card_deck) < 4:
                    pass
                else:
                    self.give_card(4)
                temp = self.pick_color()
                self.n.send({'color_change': temp})
        elif name[0] == 'wild':
            temp = self.pick_color()
            self.n.send({'color_change': temp})

    def print_computer_box(self) -> list:
        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.size[1] - 500) / 6), self.size[0] / 5,
                               self.size[1] / 6)
            computer_rect.append(rect)
        return computer_rect
    
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
            color_group.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in color_group:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            temp_name = sprite.get_name()
                            loop = False
        return temp_name
    
    def check_card(self, sprite):
        if len(self.waste.card) == 0:
            return True
        else:
            name = sprite.get_name()
            name = name.split('_')
            w_name = self.waste.card[-1]
            w_name = w_name.split('_')
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
    
    def get_next_player(self, now_turn):
        if self.rotate == 0 and now_turn + 1 == self.player_num:
            turn = 0
        elif self.rotate == 1 and now_turn - 1 < 0:
            turn = self.player_num - 1
        else:
            if self.rotate == 0:
                turn = now_turn + 1
            elif self.rotate == 1:
                turn = now_turn - 1
        return turn
    
    def give_card(self, card_num):
        if len(self.waste.card) == 1:  # 처음 카드가 +2,+4일때 처음 플레이어가 카드 받음
            dest_player = self.now_turn
        else:
            dest_player = self.get_next_player(self.now_turn)
        for i in range(0, card_num):
            self.get_from_deck(dest_player)
    
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
                            for index in self.other_index:
                                if index[1] == i :
                                    return index[0]
        return index + 1

class Multiplayer(User):
    def __init__(self):
        super().__init__()
    def set_card(self):
        for item in self.card:
            card = lc.Card(
                item, (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
            self.group.append(card)
            self.last_idx += 1
        self.last = self.group[self.last_idx - 1]

    def set(self):
        i = 0
        j = 0 
        for item in self.group:
            if  7 <= i < 14:
                item.setposition(self.size[0] * (1 / 3) + self.card_size[0] * j,
                             self.size[1] * (7 / 9) + self.size[1] / 10)
                i += 1
                j += 1
            else:
                item.setposition(
                    self.size[0] * (1 / 3) + self.card_size[0] * i, self.size[1] * (7 / 9))
                i += 1

        self.draw_group = pygame.sprite.RenderPlain(*self.group)
        return self.test_set()




