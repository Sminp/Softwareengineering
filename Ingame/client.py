import socket
import pickle
import pygame
from network import Network
from constant import *
from rect_functions import Button, Slider, TextRect
from settings import Settings, resource_path
import game_functions as gf
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


class Client:
    def __init__(self, screen, password, user_name, ip_address):
        self.password = password
        self.user_name = user_name
        self.screen = screen
        self.settings = Settings().get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.n = Network(ip_address)
        self.font = pygame.font.SysFont(self.settings['font'], 30)
        self.button, self.text_list, self.player_rect = self.object_init()
        self.user_name_text = TextRect(self.screen, self.user_name, 30, BLACK)
        self.input_active = False
        self.lobby_run = True

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
        print(p)

        pygame.init()
        self.screen.fill(WHITE)
        pygame.display.update()

        reply = self.n.send({"password": ''})
        if reply["password"] != self.password:
            print("Wrong password")
            self.n.client.close()
            return False

        if p != 0:
            reply = self.n.send({'get_players': ''})
            if len(reply['players']) >= 2:
                print("Room is full")
                reply = self.n.send({'full': True})
                print(reply['full'])
                self.show_error_msg(c.ERROR_MSG)
                self.n.client.close()
                return False
            else:
                reply = self.n.send({"add_players": self.user_name})
                print(reply)
                print(reply["players"])
        else:
            reply = self.n.send({"add_players": self.user_name})
            print(reply)
            print(reply["players"])
            reply = self.n.send({'full': False})
            print(reply['full'])

        while self.lobby_run:
            try:
                reply = self.n.send({'get_players': ''})
                index = reply['players'].index(self.user_name)
                self.object_show(reply['players'], index)
                self.handle_event(index)
                reply = self.n.send({'is_start': ''})
                if reply['start'] == True:
                    print(reply['start'])
                    game = MultiGame(self.n, len(
                        reply['players']), 1, self.user_name)
                    game.startgame()
                    self.lobby_run = False
                # 수정 필요 reply['full']이 계속 False여서 안들어가짐
                if p == 0 and reply['full'] == True:
                    print("Room is full")
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
                        self.n.send({'start': True})

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
                    reply = self.n.send({"change_name": msg})\



# class Multi(gf.Game):
#     def __init__(self, player_num=2, difficulty=1, user_name="ME"):
#         super().__init__(player_num, difficulty, user_name)

class MultiGame(gf.Game):

    def __init__(self, network, player_num=2, difficulty=1, user_name="ME"):
        super().__init__(player_num, difficulty, user_name)
        self.n = network

    def set_name(self):
        player_names = []
        reply = self.n.send({'get_players': ''})
        i = 1
        for name in reply['players']:
            if name == self.user_name:
                text = rf.TextRect(self.screen, self.user_name, 30, c.WHITE)
                player_names.append(
                    [text, (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
            elif name != 'computer':
                text = rf.TextRect(self.screen, name, 20, c.BLACK)
                player_names.append(
                    [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
                i += 1
            else:
                text = rf.TextRect(self.screen, "COM" + str(i), 20, c.BLACK)
                player_names.append(
                    [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
                i += 1

        return player_names
