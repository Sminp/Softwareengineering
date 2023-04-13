temp = []


class AI():
    def __init__(self, player_num, player_deck, waste_card):
        print(player_deck)
        self.player_num = player_num
        self.player_deck = player_deck
        self.now_card = waste_card[-1]
        self.wastes = waste_card

    def basic_play(self):
        now = self.now_card.split('_')
        for item in self.player_deck:
            card = item.split('_')
            if now[0] == 'wild':
                return item
            if len(now) == 1:
                if card[0] == now[0]:
                    return item
            elif len(card) < 3 or len(now) < 3:
                if card[0] == now[0]:
                    return item
                elif card[1] == now[1]:  # 여기에서 자꾸 오류나는데 wild카드 낼 때 문제인듯 card[1]이 없어서? 그럼 wild 카드에 뒤에 .이나 무슨 표시를 넣어야할듯?
                    return item
                elif card[0] == now[1]: # 색 두 개인 카드 낼 수 있게  
                    return item
                elif card[1] == now[0]:
                    return item
            else:
                if card[0] == now[0]:
                    return item
                elif card[2] == now[2]:
                    return item
        for item in self.player_deck:
            card = item.split('_')
            if card[0] == 'wild':
                return item
        return 0

    # difficulty 2
    def advanced_play(self, next_user):
        now = self.now_card.split('_')
        solution = []
        for item in self.player_deck:
            card = item.split('_')
            if len(next_user) < 3:
                if len(card) == 3:
                    if card[2] == 4:
                        return item
                    elif card[2] == 2:
                        return item
        if len(self.player_deck) == 1:
            return self.player_deck[0]
        result = self.find_solution(now)
        if result is None:
            for item in self.player_deck:
                card = item.split('_')
                if card[0] == 'wild':
                    result = item
            return result
        else:
            return result

    def find_solution(self, now):
        temp = []
        for item in self.player_deck:
            item_ = item.split('_')
            if len(item_) == 2:
                if len(now) == 1: # wild, red, blue, green, yellow
                    if item_[0] == now[0]:
                        temp.append(item)
                if len(now) == 2:
                    if item_[0] == now[0]:
                        temp.append(item)
                    elif item_[1] == now[1]:
                        temp.append(item)
                if len(now) == 3:
                    if item_[0] == now[0]:
                        temp.append(item)
            if len(item_) == 3:
                if item_[0] != 'wild':
                    if item_[0] == now[0]:
                        if self.player_num == 2:
                            if self.check_same_color(item_[0]):
                                temp.append(item)
                        else:
                            temp.append(item)
                    if len(now) == 3:
                        if item_[2] == now[2]:
                            if self.player_num == 2:
                                if self.check_same_color(item_[0]):
                                    temp.append(item)
                            else:
                                temp.append(item)
                elif item_[0] == 'wild':
                    temp.append(item)
        if len(temp) == 1:
            return temp[0]
        if len(temp) > 1:
            before = temp[0]
            check = 0
            for i in range(1, len(temp)):
                before_ = before.split('_')
                card = temp[i]
                card_ = card.split('_')
                if before_[0] == card_[0]:
                    before = card
                else:
                    check = 1

            if check == 1:
                result = self.calculate_p(temp)
            else:
                result = temp[0]
                for card in temp:
                    card_ = card.split('_')
                    if len(card_) == 3:
                        result = card
            return result

    def check_same_color(self, color):
        sum = 0
        for item in self.player_deck:
            item_ = item.split('_')
            if item_[0] == color:
                sum += 1
        if sum > 1:
            return True
        else:
            return False

    def calculate_p(self, result):
        red = 0;
        yellow = 0;
        green = 0;
        blue = 0
        for card in self.wastes:
            card_ = card.split('_')
            if len(card_) != 1:
                if card_[0] == 'red':
                    red += 1.0
                elif card_[0] == 'yellow':
                    yellow += 1.0
                elif card_[0] == 'green':
                    green += 1.0
                elif card_[0] == 'blue':
                    blue += 1.0

        temp = [red, yellow, green, blue]
        if 0 in temp:
            temp.remove(0)
        temp.sort(reverse=True)
        c_temp = []
        for p in temp:
            if p == red:
                c_temp.append('red')
            elif p == yellow:
                c_temp.append('yellow')
            elif p == green:
                c_temp.append('green')
            elif p == blue:
                c_temp.append('blue')

        for c in c_temp:
            for i in result:
                card = i.split('_')
                if card[0] == c:
                    return i

        return result[0]
