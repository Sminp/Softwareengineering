import sys
import pygame
from pygame.locals import *
import constant as c
import settings as s
import loadcard as lc
import rect_functions as rf
import timer

"""서버에서 리스트를 받아오면 생성하는 클래스입니다."""

# 수정 사항
# 애니메이션 빼기
# user와 나머지 그룹 생성


class ClientUser():
    def __init__(self, screen, player_num: int, user_idx: int, network):
        super().__init__()
        self.player_num = player_num
        self.user_idx = user_idx
        self.n = network
        self.settings = s.Settings().get_setting()
        self.size = self.settings['screen']
        self.card_size = (self.settings['screen']
                          [0] / 10, self.settings['screen'][1] / 6)
        self.startpos = (self.settings['screen'][0] / 3 -
                         self.card_size[0], self.settings['screen'][1] * (7 / 9))
        self.bg_img = pygame.transform.scale(pygame.image.load(s.resource_path(
            c.GAME_BACKGROUND)), (self.settings['screen']))
        self.playing_game = True
        self.time_limit = 10  # -> 시간 제한 설정
        self.time = 0
        self.screen = screen

        self.uno_button = rf.Button(self.screen, self.size[0] * (3 / 4), self.size[1] * (1 / 3),
                                    c.UNO_BUTTON, self.size[1] * (1 / 20),
                                    self.size[1] * (1 / 20))
        
        self.user = []
        self.draw_user = None
        self.others = []
        self.draw_others = None
        self.waste = []
        self.draw_waste = None
        self.last_idx = 0
        self.last = None
        self.now_turn = 0

        pygame.init()
        self.timer = timer.Timer()

    def player_init(self):
        self.user = []
        self.draw_user = None
        self.others = []
        self.draw_others = None
        self.waste = []
        self.draw_waste = None
        self.last_idx = 0
        self.last = None
        self.now_turn = 0

    def set_card(self, deck: list) -> int:
        for num in range(self.player_num):
            if num == self.user_idx:
                idx = 0
                for val in deck[num]:
                    self.set_user(val, idx)
                    idx += 1
            else:
                idx = 0
                for _ in deck[num]:
                    order = num
                    self.set_others(order, idx)
                    idx += 1

    def set_user(self, val: str, idx: int) -> int:
        card = lc.Card(
            val, (self.size[0] * (1 / 3) + self.card_size[0] * idx, self.size[1] * (7 / 9)), self.card_size)
        self.user.append(card)
        self.draw_user = pygame.sprite.RenderPlain(*self.user)

    def set_others(self, order: int, idx: int) -> int:
        card = lc.Card(
            'back', (self.size[0] * (1 / 30) + 10 * idx, self.size[1]
                     * ((2 * order - 1) / 10)), self.card_size)
        self.others.append(card)
        self.draw_others = pygame.sprite.RenderPlain(*self.others)

    def set_waste(self, val: str):
        waste = lc.Card(val, (self.size[0] * (3 / 5),
                              self.size[1] * (1 / 3)), self.card_size)
        self.waste.append(waste)
        self.draw_waste = pygame.sprite.RenderPlain(self.waste)

    def set_back(self):
        back = lc.Card('back', (self.size[0] * (2 / 5),
                                self.size[1] * (1 / 3)), self.card_size)
        self.waste.append(back)
        self.draw_waste = pygame.sprite.RenderPlain(self.waste)

    def set_name(self):  # 이름이랑 위치 리스트로 저장하는거 어때?! - 이거 json파일로 하면 훨씬 편해.
        player_names = []
        text = rf.TextRect(self.screen, "ME", 30, c.WHITE)
        player_names.append(
            [text, (self.size[0] * (3 / 5), self.size[1] * (2 / 3))])
        for i in range(1, self.player_num):
            text = rf.TextRect(self.screen, "COM" + str(i), 20, c.BLACK)
            player_names.append(
                [text, (self.size[0] * (1 / 10), self.size[1] * ((5 * i - 4) / 25))])
        return player_names

    # 스프라이트에서 제거 후 서버로 이름을 넘겨준다.
    def remove(self, sprite) -> str:
        name = sprite.get_name()
        self.user.remove(sprite)
        self.draw_user.remove(sprite)
        for temp in self.user:
            temp.move(sprite.getposition())
        sprite.setposition(self.size[0] * (3 / 5), self.size[1] * (1 / 3))
        self.last_idx -= 1
        if self.last_idx >= 1:
            self.last = self.user[self.last_idx - 1]
        return name

    def handle_event(self):
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
                    else:
                        for sprite in self.player[0].user:
                            if sprite.get_name() == self.player[0].card[selected] and self.check_card(sprite):
                                self.player[0].remove(sprite)
                                for temp in self.player[0].user:
                                    temp.move(sprite.getposition())
                                sprite.setposition(
                                    self.size[0] * (3 / 5), self.size[1] * (1 / 3))
                                self.waste.updating(sprite.get_name())
                                self.card_skill(sprite.get_name())
                                if len(self.player[0].user) == 1:  # 카드 내고 한장 남음
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
                    for sprite in self.player[0].user:
                        if sprite.get_rect().collidepoint(event.pos) and self.check_card(sprite):
                            self.set_animation(
                                sprite.get_name(), sprite.getposition())
                            # pygame.mixer.pre_init(44100, -16, 1, 512)
                            # card = pygame.mixer.Sound('./sound/deal_card.wav')
                            self.player[0].remove(sprite)
                            self.waste.updating(sprite.get_name())
                            self.card_skill(sprite.get_name())
                            if len(self.player[0].user) == 1:  # 카드 내고 한장 남음
                                pygame.display.update()
                                self.check_uno_button()
                            return sprite.get_name()
                            # return 1
                    for sprite in self.waste.user:
                        if sprite.get_rect().collidepoint(event.pos):
                            self.get_from_deck(self.now_turn)
                            return 'Back'

    # 모두 없애고 다시 객체를 만들거야
    def clear(self):
        del self.user
        del self.draw_user
        del self.others
        del self.draw_others
        del self.last_idx
        del self.last
        del self.waste
        del self.draw_waste

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

    def pick_color(self, input):
        if input:
            self.playing_game = False
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
                        for sprite in color_group:
                            if sprite.get_rect().collidepoint(event.pos):
                                temp_name = sprite.get_name()
                                loop = False
                                self.playing_game = True
            return temp_name

    def pick_player(self, input):
        if input:
            self.playing_game = False

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
                                loop = False
                                self.playing_game = True
                                return i + 1
            return index + 1

    def set(self):
        self.clear()
        self.player_init()
        self.set_name()
        self.reply_server()
        self.timer.reset_tmr()
        self.update()

    def print_computer_box(self) -> list:
        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.size[1] - 500) / 6), self.size[0] / 5,
                               self.size[1] / 6)
            computer_rect.append(rect)
        return computer_rect

    def show_now_turn(self, now_turn):

        for i, text in enumerate(self.player_names):
            if i == now_turn:
                text[0].change_color(c.YELLOW)
                text[0].show(text[1])
            else:
                text[0].change_color(c.BLACK)
                text[0].show(text[1])

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        # self.draw_color_rect()
        self.timer.show_tmr(self.now_turn)
        for rect in self.print_computer_box():
            pygame.draw.rect(self.screen, c.WHITE, rect)
        self.draw_user.draw(self.screen)
        self.draw_others.draw(self.screen)
        self.draw_waste.draw(self.screen)
        self.uno_button.show()
        self.show_now_turn(self.now_turn)
        pygame.display.update()

    # 서버로 받을 것 : 카드 리스트, 현재 턴, 낸 카드
    def reply_server(self):
        reply = self.n.send({'game':''})
        game = reply['game']
        waste = game.waste
        deck = game.card_deck
        self.now_turn = game.now_turn
        # pick_color = None
        # pick_player = None
        self.set_back()
        self.set_waste(waste)
        self.set_card(deck)
        # self.pick_color(pick_color)
        # self.pick_player(pick_player)

    # 서버로 보낼 것 : 낸 카드, 다음 턴
    def send_server(self, temp: str):
        pass

    def update(self):
        playing_game = True

        while playing_game:
            tmr_bool = self.timer.tick_tmr()
            self.reply_server()
            # 순서는 나중에 고려
            self.draw()
            if self.now_turn != self.user_idx:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                temp = self.handle_event()
            if temp or tmr_bool is False:
                self.send_server(temp)
