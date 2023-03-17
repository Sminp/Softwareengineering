"""여기가 아마 인게임 즉 게임이 시작할 때 구현해야 하는 공간이야 지금 아마 나랑 나연이가 많이 구현할거야."""
import random
import sys

input = sys.stdin.readline

color_set = ['r', 'g', 'b', 'y']
game_card = []
player_card = []
computer_card = []
game_turn = 0

for card_c in range(4):
    for j in range(1, 10):
        game_card.append(color_set[card_c] + str(j))

for card_c in range(14):
    select_num = random.randint(0, len(game_card) - 1)
    selected_card = game_card[select_num]
    if card_c % 2 == 0:
        player_card.append(selected_card)
        game_card.remove(selected_card)
    else:
        computer_card.append(selected_card)
        game_card.remove(selected_card)

print('플레이어 카드')
print(player_card)
print('컴퓨터 카드')
print(computer_card)

"""가위바위보 또는 다른 것으로 순서 정하기 지금은 플레이어 먼저!"""
# 플레이어는 숫자 즉 인덱스로 입력을 하며 카드는 무조건 범위 안에 있는 것을 고른다고 가정.
# 낼 수 있는 카드가 없을 때에는 7을 내고 카드를 먹는다.

given_card = game_card.pop()
while len(player_card) != 0 and len(game_card) != 0:
    game_turn += 1
    if game_turn % 2 != 0:
        print('=> ' + given_card)
        card_num = int(input())
        if card_num == 100:
            player_card.append(game_card.pop())
        else:
            card = player_card[card_num]
            if card.startswith(given_card[0]) or card.endswith(given_card[1]):
                given_card = card
                print(card)
                player_card.remove(card)
            else:
                continue

    else:
        # 컴퓨터 알고리즘을 실행할 공간인데 일단은 for문 겁나 돌릴예정이야.
        for i in range(len(computer_card)):
            card_c = computer_card[i]
            if card_c.startswith(given_card[0]) or card_c.endswith(given_card[-1]):
                given_card = card_c
                print(card_c)
                computer_card.remove(card_c)
                break
            elif i == len(computer_card) - 1 and card_c[0] != given_card[0] and card_c[1] != given_card[1]:
                computer_card.append(game_card.pop())
                break
            else:
                continue
        print('플레이어')
        print(player_card)
        print('컴퓨터')
        print(computer_card)
print('end'+str(game_turn))

# 일단 게임 뒤집기나 특징적인 카드 구현 안함
# 둘 다 게임 다 나와 있음
# 만약에 game_card가 없어진다면 이미 냈던 카드 섞어서 해야 함
# 동적 계획 또는 다익스트라로 구현...? 근데 이게 부분인지 아닌지 확인이 가능한가?
# 반복문 줄일 수 있는 방법이 없을까?
# 한 턴이 플레이어랑 컴퓨터 둘 다여서 오바야.. -> if문으로 해결
