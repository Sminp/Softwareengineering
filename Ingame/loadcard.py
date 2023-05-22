import pygame
from pygame.locals import *
import math
from settings import Settings, resource_path
import constant as c
import math


class Card(pygame.sprite.Sprite):
    def __init__(self, name, position, size):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.settings = Settings().get_setting()
        if self.settings['setting_color'] == True:
            self.image = pygame.image.load(resource_path(
                './image/color_card_img/' + name + '.png'))  # 여기 색약 모드 이미지 불러오는걸로!
        else:
            self.image = pygame.image.load(
                './image/card_img/' + name + '.png')  # 여기는 기본 이미지!
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.orig_pos = position
        self.position = position
        self.user_rotation = 30
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self, dest_loc, speed=10):
        x, y = self.position
        vx, vy = (dest_loc[0] - x, dest_loc[1] - y)
        vx, vy = (x / (x ** 2 + y ** 2) ** 0.5, y / (x ** 2 + y ** 2) ** 0.5)

        x = x + speed * vx
        y = y + speed * vy

        if x >= dest_loc[0]:
            x = dest_loc[0]
        if y >= dest_loc[1]:
            y = dest_loc[1]

        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def animate(self, dest_loc):
        x, y = self.position
        vx, vy = (x / (x ** 2 + y ** 2) ** 0.5, y / (x ** 2 + y ** 2) ** 0.5)

        speed = 20

        if x >= dest_loc[0] and y >= dest_loc[1]:
            x = x - speed * vx
            y = y - speed * vy
        elif x >= dest_loc[0] and y < dest_loc[1]:
            x = x - speed * vx
            y = y + speed * vy
        elif x < dest_loc[0] and y >= dest_loc[1]:
            x = x + speed * vx
            y = y - speed * vy
        elif x < dest_loc[0] and y < dest_loc[1]:
            x = x + speed * vx
            y = y + speed * vy

        if abs(x - dest_loc[0]) <= 20:
            x = dest_loc[0]
        if abs(y - dest_loc[1]) <= 20:
            y = dest_loc[1]

        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def rotation(self, rotate):
        self.image = pygame.transform.rotate(self.image, rotate)

    def getposition(self):
        return self.position

    def setposition(self, x, y):
        i_x = x
        i_y = y
        self.position = (i_x, i_y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def move(self, compare_pos):
        x, y = self.position
        i_x = compare_pos[0]
        i_y = compare_pos[1]

        if x >= i_x + c.SCREEN_WIDTH / 10 and y == i_y:
            x -= c.SCREEN_WIDTH / 10

        elif y > i_y:
            if x <= c.SCREEN_WIDTH / 3:
                x = c.SCREEN_WIDTH * (28 / 30)
                y = y - c.SCREEN_HEIGHT / 10
            else:
                x -= c.SCREEN_WIDTH / 10
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_rect(self):
        return self.rect

    def get_name(self):
        return self.name


class Popup(pygame.sprite.Sprite):
    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load('./image/card_img/' + name + '.png')
        # self.colorimg = pygame.image.load(
        #     './image/color_card_img/' + name + '.png')
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_name(self):
        return self.name

    def get_rect(self):
        return self.rect
