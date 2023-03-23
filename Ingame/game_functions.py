import random

"""게임 알고리즘 그리디 컴퓨터 플레이어 구현하는 공간"""

"""
108장의 카드 생성 
Parameters: None
Return values: deck(list)
"""


def build_deck():
    deck = []
    colors = ["red", "green", "yellow", "blue"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
    wilds = ["Wild", "Wild Draw Four"]
    for color in colors:
        for value in values:
            card_val = "{} {}".format(color, value)
            deck.append(card_val)
            if value != 0:
                deck.append(card_val)
    for i in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck


# 리스트 안의 원소를 각각 일대일로 대응시켜서 딕셔너리 만드는 함수
def make_dict(key, val):
    new_key = []
    for i in key:
        if i not in new_key:
            new_key.append(i)
    dic = {}
    for k, v in zip(new_key, val):
        dic[k] = v
    return dic


"""
카드 섞기
Parameters: deck(list)
Return values: deck(list)
"""


def shuffle_deck(deck):
    for card_pos in range(len(deck)):
        rand_pos = random.randint(0, 107)
        deck[card_pos], deck[rand_pos] = deck[rand_pos], deck[card_pos]
    return deck


"""
카드 뽑기 
Parameters: num_cards (int) : 뽑을 카드 수
Return: cards_drawn (list)
"""


def draw_card(deck, num_cards):
    cards_drawn = []
    for x in range(num_cards):
        cards_drawn.append(deck.pop(0))
    return cards_drawn


"""
플레이어가 가지고 있는 카드를 보여줌
Parameter: player(int), player_hand(list)
Return: None
"""


# def showHand(player, player_hand):
#     print("Player {}'s Turn".format(player + 1))
#     print("Your Hand")
#     print("------------------")
#     y = 1
#     for card in player_hand:
#         print("{}) {}".format(y, card))
#         y += 1
#     print("")


"""
현재 카드의 색과 값을 플레이어의 카드들과 비교하여 낼 수 있는 상태인지 확인
Parameters: color(string), value(string), player_hand(list)
Return: boolean
"""


def can_play(color, value, player_hand):
    for card in player_hand:
        if "Wild" in card:
            return True
        elif color in card or value in card:
            return True
    return False

# 고칠 부분

"""
split_card = discards[0].split(" ", 1)
current_color = split_card[0]

if current_color != "Wild":
    card_val = split_card[1]

else:
    print("현재 카드: {}".format(discards[-1]))
    for x in range(len(colors)):
        print("{}) {}".format(x + 1, colors[x]))
    new_color = int(input("바꿀 색을 선택하세요: "))
    while new_color < 1 or new_color > 4:
        new_color = int(input("입력이 올바르지 않습니다. 바꿀 색을 선택하세요: "))
    current_color = colors[new_color - 1]
    card_val = "Any"

while playing:
    showHand(player_turn, players[player_turn])
    print("현재 카드: {}".format(discards[-1]))
    if can_play(current_color, card_val, players[player_turn]):
        card_chosen = int(input("낼 카드를 선택하세요: "))
        while not can_play(current_color, card_val, [players[player_turn][card_chosen - 1]]):
            card_chosen = int(input("입력이 올바르지 않습니다. 낼 카드를 선택하세요: "))
        print("당신이 낸 카드: {}".format(players[player_turn][card_chosen - 1]))
        discards.append(players[player_turn].pop(card_chosen - 1))
        # 이긴 사람 확인
        if len(players[player_turn]) == 0:
            playing = False
            winner = "Player {}".format(player_turn + 1)
        else:
            # 기능 카드 확인
            split_card = discards[-1].split(" ", 1)
            current_color = split_card[0]
            if len(split_card) == 1:
                card_val = "Any"
            else:
                card_val = split_card[1]
            if current_color == "Wild":
                for x in range(len(colors)):
                    print("{}) {}".format(x + 1, colors[x]))
                new_color = int(input("바꿀 색을 선택하세요: "))
                while new_color < 1 or new_color > 4:
                    new_color = int(input("입력이 올바르지 않습니다. 낼 카드를 선택하세요: "))
                current_color = colors[new_color - 1]
            if card_val == "Reverse":
                player_direction = player_direction * -1
            elif card_val == "Skip":
                player_turn += player_direction
                if player_turn >= num_player:
                    player_turn = 0
                elif player_turn < 0:
                    player_turn = num_player - 1
            elif card_val == "Draw Two":
                player_draw = player_turn + player_direction
                if player_draw == num_player:
                    player_draw = 0
                elif player_draw < 0:
                    player_draw = num_player - 1
                players[player_draw].extend(draw_card(2))
            elif card_val == "Draw Four":
                player_draw = player_turn + player_direction
                if player_draw == num_player:
                    player_draw = 0
                elif player_draw < 0:
                    player_draw = num_player - 1
                players[player_draw].extend(draw_card(4))
            print("")
    else:
        print("낼 카드가 없습니다. 카드를 뽑습니다.")
        players[player_turn].extend(draw_card(1))

    player_turn += player_direction
    if player_turn >= num_player:
        player_turn = 0
    elif player_turn < 0:
        player_turn = num_player - 1

print("Game Over")
print("승자 : {}".format(winner))

"""
