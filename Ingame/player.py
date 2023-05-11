import pygame
from abc import ABC, abstractmethod
from loadcard import Card, Popup
from UNO import terminate
from settings import Settings

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
        self.settings = Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen'][0] / 10, self.settings['screen'][1] / 6)


    def append(self, val):
        self.card.append(val)

    def set_card(self):
        for item in self.card:
            card = Card(item, (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
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
            item.update((self.size[0] * (1 / 3) + self.card_size[0] * i, self.size[1] * (7 / 9)))
            i += 1
        self.draw_group = pygame.sprite.RenderPlain(*self.group)
        return self.test_set()

    # 수정중이여서 아직 self.card_size로 안 바꿈 
    def set_lastcard(self): # 아니 근데 이거 안 쓰이는 것 같은데?!
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
        self.last.setposition(x, y) # 이렇게 하면 last카드의 위치가 x,y로 옮겨지는거라 바꿔야 해!
    
    def get_lastcard(self): # 마지막 카드의 위치를 반환
        return self.group[-1].getposition()
    
    def remove(self, sprite):
        name = sprite.get_name()
        self.card.remove(name)
        self.group.remove(sprite)
        self.draw_group.remove(sprite) # 이거 없어도 되나?!
        for temp in self.group:
            temp.move(sprite.getposition())
        sprite.setposition(self.size[0] * (3 / 5), self.size[1] * (1 / 3))

    def add_card(self, card):
        temp = Card(card, (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
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
        self.card.append(card) # 여기 왜 self.append(card)라고 했지?
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

    # 변경할 색 선택 -> 이걸 game_function으로 옮겨야하지 않을까?
    def pick_color(self, size):
        # 뒤에 이미지 -> 빼거나 대체
        red = Popup('red', (306, 320))
        yellow = Popup('yellow', (368, 320))
        green = Popup('green', (432, 320))
        blue = Popup('blue', (494, 320))
        colors = [red, yellow, green, blue]
        color_group = pygame.sprite.RenderPlain(*colors)

        while 1:
            # popup_group.update_card(self.screen)
            color_group.update_card(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    for sprite in color_group:
                        if sprite.get_rect().collidepoint(event.pos):
                            temp_name = sprite.get_name()
                            temp = Card(temp_name,
                                        (size[0] * (3 / 5),
                                         size[1] * (1 / 3)),
                                        (size[0] / 10, size[1] / 6))
                            return temp_name
        # 아마 버그 있을 거 같은데
        return 0

    # change 카드 사용할 때 바꿀 플레이어 선택
    def pick_player(self):

        pick_player_button = []
        for i in range(1, self.card_num):
            image_name = "./image/playing_image/deckchange_player" + \
                         str(i) + ".jpg"
            # 이거 약간 애매해 - 밖으로 꺼내자.
            temp_button = Button(self.screen, self.screen_width * (1 / 2), self.screen_height / 6 * i, image_name,
                                 self.screen_width * (1 / 8), self.screen_height * (1 / 9))
            pick_player_button.append(temp_button)
        index = 0

        loop = True
        while loop:
            for i in range(self.card_num - 1):
                pick_player_button[i].show_button()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(self.card_num - 1):
                        if pick_player_button[i].get_rect().collidepoint(event.pos):
                            # 수정중
                            return i
                            # loop = False

        return index + 1


class Computer(Player):
    def __init__(self):
        super().__init__()
        self.card = []
        self.group = []
        self.last_idx = 0
        self.draw_group = None
        self.last = None
        self.settings = Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen'][0] / 30, self.settings['screen'][1] / 18)

    def append(self, card):
        self.card.append(card)

    def set_card(self):
        for _ in self.card:
            card = Card('back', (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
            self.group.append(card)
            self.last_idx += 1
        self.last = self.group[self.last_idx - 1]

    def test_set(self, num):
        if self.last_idx:
            last_pos = self.last.getposition()
            if last_pos == (
                    self.size[0] * (1 / 30) + 10 * (self.last_idx - 1), self.size[1] * ((2 * num - 1) / 10)):
                return 0
        return 1

    def set(self, player_num):
        i = 0
        for item in self.group:
            item.update((self.size[0] * (1 / 30) + 10 * i,
                         self.size[1] * ((2 * player_num - 1) / 10)))
            i += 1
        self.draw_group = pygame.sprite.RenderPlain(self.group)
        return self.test_set(player_num)

    def remove(self, val):
        self.card.remove(val)
        for sprite in self.group:
            if sprite.getposition() == self.get_lastcard():
                self.group.remove(sprite)
                self.draw_group.remove(sprite)

    def add_card(self, card):
        temp = Card(
            'back', (350, 300), self.card_size)
        current_pos = self.get_lastcard()
        if current_pos[0] >= self.size[0] * (1 / 6):
            y = current_pos[1] + self.size[1] / 30
            x = self.size[0] * (1 / 30)
        else:
            y = current_pos[1]
            x = current_pos[0] + 10
        temp.setposition(x, y)
        # self.last.setposition(x, y)
        self.card.append(card) # 여기 왜 self.append(card)라고 했지?
        self.group.append(temp)
        self.draw_group.add(temp)

    def get_lastcard(self): # 마지막 카드의 위치를 반환
        return self.group[-1].getposition()

    def set_lastcard(self, now_turn):
        x, y = self.last.getposition()

        num = now_turn
        if x == self.size[0] * (1 / 6) and y > self.size[1] * (2 * num - 1 / 10):
            y -= self.size[1] * (1 / 30)
            x = self.size[0] * (1 / 6)
        else:
            x -= 10
        self.last.setposition(x, y)

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

    # 가장 적은 숫자 카드 나타내는 함수
    def least_num(self) -> int:
        least_player_idx = 0
        least_player_num = len(self.card[0])
        for num in range(1, self.card_num):
            if least_player_num > len(self.card[num]):
                least_player_idx = num
                least_player_num = len(self.card[num])
        return least_player_idx

    # change 카드를 컴퓨터 플레이어가 선택할 때 제일 카드가 적은 플레이어 선택
    def check_card_num(self, player_deck_list):
        shortest_list = min(player_deck_list, key=len)
        return player_deck_list.index(shortest_list)


class Waste(Player):
    """나머지 카드들"""

    def __init__(self):
        super().__init__()
        self.card = []
        self.group = []
        self.draw_group = None
        self.last_idx = 0
        self.settings = Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen'][0] / 10, self.settings['screen'][1] / 6)


    def append(self, val):
        self.card.append(val)

    def set_card(self):
        deck = Card('back', (self.size[0] * (2 / 5), self.size[1] * (1 / 3)), self.card_size)
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
        temp = Card(val, (self.size[0] * (3 / 5), self.size[1] * (1 / 3)), self.card_size)
        self.update_card(temp)
        self.draw_group = pygame.sprite.RenderPlain(self.group)

    def draw_last(self):
        pass
