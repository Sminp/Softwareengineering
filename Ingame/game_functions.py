import random

"""
108장의 카드 생성 
Parameters: None
Return values: deck(list)
"""


def buildDeck():
    deck = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
    wilds = ["Wild", "Wild Draw Four"]
    for color in colors:
        for value in values:
            cardVal = "{} {}".format(color, value)
            deck.append(cardVal)
            if value != 0:
                deck.append(cardVal)
    for i in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck


"""
카드 섞기
Parameters: deck(list)
Return values: deck(list)
"""


def shuffleDeck(deck):
    for cardPos in range(len(deck)):
        randPos = random.randint(0, 107)
        deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
    return deck


"""
카드 뽑기 
Parameters: numCards (int) : 뽑을 카드 수
Return: cardsDrawn (list)
"""


def drawCards(numCards):
    cardsDrawn = []
    for x in range(numCards):
        cardsDrawn.append(unoDeck.pop(0))
    return cardsDrawn


"""
플레이어가 가지고 있는 카드를 보여줌
Parameter: player(int), playerHand(list)
Return: None
"""


def showHand(player, playerHand):
    print("Player {}'s Turn".format(player + 1))
    print("Your Hand")
    print("------------------")
    y = 1
    for card in playerHand:
        print("{}) {}".format(y, card))
        y += 1
    print("")


"""
현재 카드의 색과 값을 플레이어의 카드들과 비교하여 낼 수 있는 상태인지 확인
Parameters: color(string), value(string), playerHand(list)
Return: boolean
"""


def canPlay(color, value, playerHand):
    for card in playerHand:
        if "Wild" in card:
            return True
        elif color in card or value in card:
            return True
    return False


unoDeck = buildDeck()
unoDeck = shuffleDeck(unoDeck)
unoDeck = shuffleDeck(unoDeck)
discards = []

players = []
colors = ["Red", "Green", "Yellow", "Blue"]
numPlayers = int(input("player의 수를 입력하세요: "))
while numPlayers < 2 or numPlayers > 4:
    numPlayers = int(input("2~4 명의 player만 가능합니다. 다시 입력하세요:"))
for player in range(numPlayers):
    players.append(drawCards(5))

playerTurn = 0
playDirection = 1
playing = True
discards.append(unoDeck.pop(0))
splitCard = discards[0].split(" ", 1)
currentColor = splitCard[0]
if currentColor != "Wild":
    cardVal = splitCard[1]

else:
    print("현재 카드: {}".format(discards[-1]))
    for x in range(len(colors)):
        print("{}) {}".format(x + 1, colors[x]))
    newColor = int(input("바꿀 색을 선택하세요: "))
    while newColor < 1 or newColor > 4:
        newColor = int(input("입력이 올바르지 않습니다. 바꿀 색을 선택하세요: "))
    currentColor = colors[newColor - 1]
    cardVal = "Any"

while playing:
    showHand(playerTurn, players[playerTurn])
    print("현재 카드: {}".format(discards[-1]))
    if canPlay(currentColor, cardVal, players[playerTurn]):
        cardChosen = int(input("낼 카드를 선택하세요: "))
        while not canPlay(currentColor, cardVal, [players[playerTurn][cardChosen - 1]]):
            cardChosen = int(input("입력이 올바르지 않습니다. 낼 카드를 선택하세요: "))
        print("당신이 낸 카드: {}".format(players[playerTurn][cardChosen - 1]))
        discards.append(players[playerTurn].pop(cardChosen - 1))
        # 이긴 사람 확인
        if len(players[playerTurn]) == 0:
            playing = False
            winner = "Player {}".format(playerTurn + 1)
        else:
            # 기능 카드 확인
            splitCard = discards[-1].split(" ", 1)
            currentColor = splitCard[0]
            if len(splitCard) == 1:
                cardVal = "Any"
            else:
                cardVal = splitCard[1]
            if currentColor == "Wild":
                for x in range(len(colors)):
                    print("{}) {}".format(x + 1, colors[x]))
                newColor = int(input("바꿀 색을 선택하세요: "))
                while newColor < 1 or newColor > 4:
                    newColor = int(input("입력이 올바르지 않습니다. 낼 카드를 선택하세요: "))
                currentColor = colors[newColor - 1]
            if cardVal == "Reverse":
                playDirection = playDirection * -1
            elif cardVal == "Skip":
                playerTurn += playDirection
                if playerTurn >= numPlayers:
                    playerTurn = 0
                elif playerTurn < 0:
                    playerTurn = numPlayers - 1
            elif cardVal == "Draw Two":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers - 1
                players[playerDraw].extend(drawCards(2))
            elif cardVal == "Draw Four":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers - 1
                players[playerDraw].extend(drawCards(4))
            print("")
    else:
        print("낼 카드가 없습니다. 카드를 뽑습니다.")
        players[playerTurn].extend(drawCards(1))

    playerTurn += playDirection
    if playerTurn >= numPlayers:
        playerTurn = 0
    elif playerTurn < 0:
        playerTurn = numPlayers - 1

print("Game Over")
print("승자 : {}".format(winner))