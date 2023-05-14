import pygame
from abc import ABC, abstractmethod
from .component import loadcard as lc
from . import settings as s

"""Game에도 함수 이름은 있되 거기에서 여기 있는 함수들을 활용할 거야."""


class Player(ABC):
    """게임을 하는 대상, 컴퓨터 및 사용자 모두 포함한다."""

    def __init__(self):
        pass

    # 카드 받는 거
    @abstractmethod
    def set_card(self):
        pass

    # 카드 이름 받는 리스트
    @abstractmethod
    def append(self, val):
        pass

    # @abstractmethod
    def update_card(self):
        pass

    # @abstractmethod
    def update_value(self):
        pass

    def update(self):
        pass


class User(Player):
    """ 우리가 멀티 플레이어를 만들려면 최소한 사용자도 객체여야만 해"""

    def __init__(self):
        super().__init__()
        self.card = []
        self.group = []
        self.draw_group = None
        self.last_idx = 0
        self.last = None
        self.settings = s.Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen']
                          [0] / 10, self.settings['screen'][1] / 6)
        self.startpos = (self.settings['screen'][0] / 3 -
                         self.card_size[0], self.settings['screen'][1] * (7 / 9))

    def append(self, val):
        self.card.append(val)

    def set_card(self):
        for item in self.card:
            card = lc.Card(
                item, (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
            self.group.append(card)
            self.last_idx += 1
        self.last = self.group[self.last_idx - 1]

    # bool 값 받기
    def test_set(self):
        if self.last_idx:
            last_pos = self.last.getposition()
            if last_pos == (
                    self.size[0] * (1 / 3) + self.card_size[0] * (self.last_idx - 1), self.size[1] * (7 / 9)):
                return 0
        return 1

    def set(self):
        i = 0
        for item in self.group:
            item.update(
                (self.size[0] * (1 / 3) + self.card_size[0] * i, self.size[1] * (7 / 9)))
            i += 1
        self.draw_group = pygame.sprite.RenderPlain(*self.group)
        return self.test_set()

    # 수정중이여서 아직 self.card_size로 안 바꿈
    def set_lastcard(self):  # 아니 근데 이거 안 쓰이는 것 같은데?!
        # x, y = self.last.getposition()
        x, y = self.get_lastcard()

        i_x = 0
        i_y = 0

        if x >= i_x + self.size[0] / 10 and y == i_y:
            x -= self.size[0] / 10

        elif y > i_y:
            if x <= self.size[0] / 3:
                x = self.size[0] * (28 / 30)
                y = y - self.size[1] / 10
            else:
                x -= self.size[0] / 10
        self.last.setposition(x, y)  # 이렇게 하면 last카드의 위치가 x,y로 옮겨지는거라 바꿔야 해!

    def get_lastcard(self):  # 마지막 카드의 위치를 반환
        if self.group:
            return self.group[-1].getposition()
        else:
            return self.startpos

    def remove(self, sprite):
        name = sprite.get_name()
        self.card.remove(name)
        self.group.remove(sprite)
        self.draw_group.remove(sprite)  # 이거 없어도 되나?!
        for temp in self.group:
            temp.move(sprite.getposition())
        sprite.setposition(self.size[0] * (3 / 5), self.size[1] * (1 / 3))

    def add_card(self, card):
        temp = lc.Card(card, (self.size[0] * (2 / 5),
                    self.size[1] * (1 / 3)), self.card_size)
        # current_pos = self.last.getposition()
        current_pos = self.get_lastcard()
        if current_pos[0] >= self.size[0] * (28 / 30):
            y = current_pos[1] + self.size[1] / 10
            x = self.size[0] * (1 / 3)
        else:
            y = current_pos[1]
            x = current_pos[0] + self.size[0] / 10
        temp.setposition(x, y)
        # self.last.setposition(x, y)
        self.card.append(card)  # 여기 왜 self.append(card)라고 했지?
        self.group.append(temp)
        self.draw_group.add(temp)

    # 창에 나타내는거

    def update_card(self):
        i = 0
        temp_list = []
        j = 0
        k = 0
        for item in self.card:
            if 7 <= i < 14:
                item.update((self.size[0] * (1 / 3) + self.card_size[0] * j,
                             self.size[1] * (7 / 9) + self.size[1] / 10))
                temp_list.append(item)
                j += 1
                i += 1
            elif i >= 14:
                item.update((self.size[0] * (1 / 3) + self.card_size[0] * k,
                             self.size[1] * (7 / 9) + self.size[1] * 2 / 10))
                temp_list.append(item)
                k += 1
                i += 1
            else:
                item.update((self.size[0] * (1 / 3) + self.card_size[0] *
                             i, self.size[1] * (7 / 9)))
                temp_list.append(item)
                i += 1
        self.group = pygame.sprite.RenderPlain(*temp_list)
        if temp_list:
            pos = temp_list[-1].getposition()
            self.last.setposition(pos)
        if self.last.getposition() == (
                self.size[0] * (1 / 3) + 80 * (len(temp_list) % 7 - 1),
                self.size[1] * (7 / 9) + self.size[1] * 2 / 10):
            return 0

    def handle_event(self):
        pass

    def clear(self):
        for sprite in self.draw_group:
            self.draw_group.remove(sprite)
        self.card = []
        self.group = []
        self.last_idx = 0
        self.last = None


class Computer(Player):
    def __init__(self, index):
        super().__init__()
        self.card = []
        self.group = []
        self.last_idx = 0
        self.draw_group = None
        self.last = None
        self.settings = s.Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (
            self.settings['screen'][0] / 30, self.settings['screen'][1] / 18)
        self.index = index
        self.startpos = (
            self.card_size[0] - 10, self.size[1] * (((self.index - 1) * 2 + 1) / 10))

    def append(self, card):
        self.card.append(card)

    def set_card(self):
        for _ in self.card:
            card = lc.Card(
                'back', (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
            self.group.append(card)
            self.last_idx += 1
        self.last = self.group[self.last_idx - 1]

    def test_set(self):
        if self.last_idx:
            last_pos = self.last.getposition()
            if last_pos == (
                    self.size[0] * (1 / 30) + 10 * (self.last_idx - 1), self.size[1] * ((2 * self.index - 1) / 10)):
                return 0
        return 1

    def set(self):
        i = 0
        for item in self.group:
            item.update((self.size[0] * (1 / 30) + 10 * i, self.size[1]
                        * ((2 * self.index - 1) / 10)))  # 이거 애니메이션인데 왜 안될까?
            i += 1
        self.draw_group = pygame.sprite.RenderPlain(*self.group)
        return self.test_set()

    def remove(self, val):
        self.card.remove(val)
        for sprite in self.group:
            if sprite.getposition() == self.get_lastcard():
                self.group.remove(sprite)
                self.draw_group.remove(sprite)

    def add_card(self, card):
        temp = lc.Card('back', (350, 300), self.card_size)
        current_pos = self.get_lastcard()
        if current_pos[0] >= self.size[0] * (1 / 6):
            y = current_pos[1] + self.size[1] / 30
            x = self.size[0] * (1 / 30)
        else:
            y = current_pos[1]
            x = current_pos[0] + 10
        temp.setposition(x, y)
        # self.last.setposition(x, y)
        self.card.append(card)  # 여기 왜 self.append(card)라고 했지?
        self.group.append(temp)
        self.draw_group.add(temp)

    def get_lastcard(self):  # 마지막 카드의 위치를 반환
        if self.group:
            return self.group[-1].getposition()
        else:
            return self.startpos

    def set_lastcard(self):
        x, y = self.get_lastcard()

        if x == self.size[0] * (1 / 6) and y > self.size[1] * (2 * self.index - 1 / 10):
            y -= self.size[1] * (1 / 30)
            x = self.size[0] * (1 / 6)
        else:
            x -= 10

    # 이거 내 생각에 dictionary로 깔끔하게 만들 수 있을 거 같아, 정렬 알고리즘 활용하기

    def most_num_color(self):
        temp_name = None
        r = y = g = b = 0
        for item in self.card:
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
        return temp_name

    # change 카드를 컴퓨터 플레이어가 선택할 때 제일 카드가 적은 플레이어 선택

    def check_card_num(self, player_deck_list):
        shortest_list = min(player_deck_list, key=len)
        return player_deck_list.index(shortest_list)

    def clear(self):
        self.card = []
        self.group = []
        for sprite in self.draw_group:
            self.draw_group.remove(sprite)
        self.last_idx = 0
        self.last = None


class Waste(Player):
    """나머지 카드들"""

    def __init__(self):
        super().__init__()
        self.card = []
        self.group = []
        self.draw_group = None
        self.last_idx = 0
        self.settings = s.Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen']
                          [0] / 10, self.settings['screen'][1] / 6)

    def append(self, val):
        self.card.append(val)

    def set_card(self):
        deck = lc.Card('back', (self.size[0] * (2 / 5),
                    self.size[1] * (1 / 3)), self.card_size)
        self.group.append(deck)
        self.draw_group = pygame.sprite.RenderPlain(self.group)

    def update_value(self, val):
        self.card.append(val)

    def update_card(self, sprite):
        self.group.append(sprite)

    # 수정중
    def update(self, sprite):
        self.update_card(sprite)
        self.update_value(sprite.get_name())
        print("버린카드의 position {}".format(sprite.getposition()))
        # 밖으로 꺼내기
        if len(self.card) != 1:
            self.set_lastcard(self.card[0].group[-1], sprite.getposition())
        print("내고 나서 lastcard {}".format(self.card[0].group[-1]))

    def updating(self, val):
        self.update_value(val)
        temp = lc.Card(val, (self.size[0] * (3 / 5),
                    self.size[1] * (1 / 3)), self.card_size)
        self.update_card(temp)
        self.draw_group = pygame.sprite.RenderPlain(self.group)

    def draw_last(self):
        pass
