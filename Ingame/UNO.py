import pygame
import sys
from game_functions import *


pygame.init()


# 카드 리스트 이미지 넣고 인덱스로 접근 (안은 튜플 앞, 뒤)
CARD_LIST = []

# 카드추가
colorList = ["blue", "yellow", "green", "red"]

for color in colorList:
    CARD_LIST.append((pygame.image.load(f"Ingame/image/uno card png/{color}change.png"), pygame.image.load("Ingame/image/uno card png/back.png")))   
    CARD_LIST.append((pygame.image.load(f"Ingame/image/uno card png/{color}pass.png"), pygame.image.load("Ingame/image/uno card png/back.png")))
    CARD_LIST.append((pygame.image.load(f"Ingame/image/uno card png/{color}plus2.png"), pygame.image.load("Ingame/image/uno card png/back.png"))) 
    for i in range(0,10):
         CARD_LIST.append((pygame.image.load(f"Ingame/image/uno card png/{color}{i}.png"), pygame.image.load("Ingame/image/uno card png/back.png")))

CARD_LIST.append((pygame.image.load("Ingame/image/uno card png/colorchange.png"), pygame.image.load("Ingame/image/uno card png/back.png"))) 
CARD_LIST.append((pygame.image.load("Ingame/image/uno card png/plus4.png"), pygame.image.load("Ingame/image/uno card png/back.png"))) 
CARD_LIST.append((pygame.image.load("Ingame/image/uno card png/colorchange.png"), pygame.image.load("Ingame/image/uno card png/back.png"))) 


# 카드 크기
CARD_HEIGHT = 585 / 5
CARD_WIDTH = 410 / 5

# 그리고 좌표도 화면 크기 조정 때문에 다 변수로 만들어야 될 것 같아.


# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200,200,200)
RED = (200,0,0)
GREEN = (0,80,0)


# 화면 크기
screen_width = 800
screen_height = 600

# # 화면 설정
# screen = pygame.display.set_mode((screen_width,screen_height))
# pygame.display.set_caption("UNO Game")

# 게임 종료
def quitGame():
    pygame.quit()
    sys.exit() 

# 텍스트 설정
def text_objects(text,font):
    textSurface = font.render(text,True,BLACK)
    return textSurface, textSurface.get_rect()

# 이미지 변환 _카드 크
def img_transform(img):
    return pygame.transform.scale(img, [CARD_WIDTH, CARD_HEIGHT])



# 시작 화면    
def startScreen():

    start = True

    # 선택된 버튼의 인덱스 저장
    selected_button_index = 0

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            # 방향키로 메뉴 선택 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_button_index >= 2 :
                        selected_button_index = 0   
                    else:
                        selected_button_index += 1
                elif event.key == pygame.K_UP:
                    if selected_button_index <= 0  :
                        selected_button_index = 2   
                    else:
                        selected_button_index -= 1
                elif event.key == pygame.K_RETURN:
                    buttons[selected_button_index].action()
                # # 화면 크기 조정
                # if event.key == pygame.K_F1:
                #     screen = pygame.display.set_mode((400, 300))
                # if event.key == pygame.K_F2:
                #     screen = pygame.display.set_mode((640, 360))


        screen.fill(WHITE)

        # 게임 제목
        largeText = pygame.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("UNO GAME",largeText)
        TextRect.center = ((screen_width/2),(screen_height/5))
        screen.blit(TextSurf,TextRect)

        # 메뉴 버튼 생성 및 그리기
        single_player_button = Button(screen_width // 2 - 100, 300, 200, 50, "Single Player",action=gameSreen)
        setting_button = Button(screen_width // 2 - 100, 400, 200, 50, "Settings",action=settingScreen)
        quit_button = Button(screen_width // 2 - 100, 500, 200, 50, "Quit",action=quitGame)

        buttons = [single_player_button, setting_button, quit_button]

        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen,GRAY,buttons[selected_button_index].rect)
        screen.blit(buttons[selected_button_index].textSurf,buttons[selected_button_index].textRect)
        
        pygame.display.update()

# 게임 화면
def gameSreen():

    gameExit = False
    playerXY = (480,400)
    playerRect = [(10,100*i+(i+1)*((screen_height-500)/6),180,100) for i in range(5)]
    font = pygame.font.Font(None,30)
    clock = pygame.time.Clock()
    clicked = False
    tmr = 0

    # 카드 생성, 반환값 리스트
    unoDeck = buildDeck()
    make_dict(unoDeck, CARD_LIST)
    # 카드 무작위 셔플, 반환값 리스트
    unoDeck = shuffleDeck(unoDeck)
    # 게임 카드
    discards = []

    # 0 player, 1 ~ 5 computers
    players = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    # 아마 2차 과제
    # numPlayers = int(input("player의 수를 입력하세요: "))
    # while numPlayers < 2 or numPlayers > 4:
    #     numPlayers = int(input("2~4 명의 player만 가능합니다. 다시 입력하세요:"))

    # 아마 인원수에 따라 바꿀 듯
    # for player in range(numPlayers):
    for player in range(2):
        players.append(drawCards(unoDeck, 5))

    # 0 나, 1 컴퓨터 - 게임 차례
    playerTurn = 0
    # reverse 방향 전환
    playDirection = 1
    playing = True
    discards.append(unoDeck.pop(0))

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                # 강제 종료
                if event.key == pygame.K_ESCAPE:
                    # 일시정지 함수 적기
                    pause()
 
        screen.fill(GREEN)
        for i in range(len(playerRect)):
            pygame.draw.rect(screen,WHITE,playerRect[i],width=0)

        for i in range(len(playerRect)):
            sur = font.render("player {}".format(i+1),True,BLACK)
            screen.blit(sur,(playerRect[i][0],playerRect[i][1]))
        
        # 마우스 위치
        mouseX, mouseY = pygame.mouse.get_pos()
        # 마우스 누르는 버튼
        mBtn1, mBtn2, mBtn3 = pygame.mouse.get_pressed()

        # 이미지 올리기
        for i in range(1, 11):
            # 엎어져 있는 카드
            if i <= 9:
                screen.blit(img_transform(CARD_LIST[2 % i][1]), [300 + i * 2, 200])
            # 게임 카드
            else:
                screen.blit(img_transform(CARD_LIST[0][0]), [450, 200])

        # 플레이어 카드
        for i in range(1, 8):
            screen.blit(img_transform(CARD_LIST[2 % i][1]), [50 + (i - 1) * 100, 400])

        # 타이머 설정
        tmr += 1
        txt = font.render(str(10 - tmr % 10), True, WHITE)
        screen.blit(txt, [10, 10])
        clock.tick(1)


        # 좌표 설정해서 노가다
        if 50 <= mouseX <= 50 + CARD_WIDTH and 400 <= mouseY <= 400 + CARD_HEIGHT and mBtn1 == 1:
            clicked = True
        if clicked:
            pygame.draw.rect(screen, YELLOW, [50 - 2, 400-2, CARD_WIDTH + 2, CARD_HEIGHT + 2], 2)
        if tmr%10 == 0:
            clicked = False

        # color =[(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        # cards=[]

        # for j in range(4):
        #     for i in range(10):
        #         pos=(400+i*2 - 50, 200 -50)
        #         card = Cards(color[j], pos, i)
        #         cards.append(card)
        
        # # 처음 카드 임의로 설정.
        # current_card=Cards(color[2], (500, 200 -50), 4)
        # current_card.show()

        # for card in cards:
        #     card.show()

        text = font.render("You",True,BLACK)
        screen.blit(text,playerXY)
    

        pygame.display.update()

            
# 설정 화면 
def settingScreen():
    
    gameExit = False

    # 배경음, 효과음 slider
    backgroundsound_slider = Slider(screen, 300, (250,180),(0,100))
    soundeffect_slider = Slider(screen, 300, (250,250),(0,100))


    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            
            backgroundsound_slider.operate(event)
            soundeffect_slider.operate(event)

        screen.fill(WHITE)

        # 설정화면 텍스트 표시
        largeText = pygame.font.SysFont("malgungothic",50)
        TextSurf, TextRect = text_objects("설정 화면",largeText)
        TextRect.center = (130,50)
        screen.blit(TextSurf,TextRect)

        # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야함
        FONT = pygame.font.SysFont("malgungothic",20)
        text = FONT.render("화면 설정" , True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (130,340)
        screen.blit(text, text_rect)

        # 화면 설정 버튼 - 변수명 바꿔야함
        sizefull_button = Button(270, 315, 100, 50, "전체화면",20,color=GRAY, hover_color=YELLOW,action=screenSize)
        size16_button = Button(420, 315, 100, 50, "16:9",20,color=GRAY, hover_color=YELLOW,action=settingScreen)
        size4_button = Button(570, 315, 100, 50, "4:3",20,color=GRAY, hover_color=YELLOW,action=quitGame)


        # 배경음, 효과음 그림
        backgroundsound_slider.draw()
        backgroundsound_slider.text_draw('배경음',(130,180))
        soundeffect_slider.draw()
        soundeffect_slider.text_draw('효과음',(130,250))

        # 조작키 설정, 설정 초기화, 설정 저장 버튼 
        control_button = Button(80, 400, 100, 50, "조작키 설정",20,color=GRAY, hover_color=YELLOW,action=gameSreen)
        settinginit_button = Button(80, 500, 100, 50, "설정 초기화",20,color=GRAY, hover_color=YELLOW,action=settingScreen)
        settingsave_button = Button(screen_width // 2 + 200, 500, 100, 50, "설정 저장",20,color=GRAY, hover_color=YELLOW,action=quitGame)

        buttons = [control_button, settinginit_button, settingsave_button]

    

        pygame.display.update()

# 버튼 클래스
class Button:
    def __init__(self,x,y,width,height,text,font_size=30,font_name='malgungothic', color=WHITE, hover_color=GRAY,action=None):
        self.rect = pygame.Rect(x,y,width,height) 
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            # 마우스를 버튼위에 올렸을 때 색깔 변함
            pygame.draw.rect(screen, self.hover_color, self.rect) 
            if click[0] == 1 and action != None:
                # 클릭하면 해당 버튼 기능 수행
                action()
        else: 
            pygame.draw.rect(screen, self.color, self.rect)

        # 버튼의 text 설정
        font = pygame.font.SysFont(font_name,font_size)
        self.textSurf, self.textRect = text_objects(text,font)
        self.textRect.center = ((x + width/2),(y + height/2))
        screen.blit(self.textSurf,self.textRect)


# # 카드 객체 생성
# class Cards():
#     # color 나중에 뺄거야 (이미지 대체)
#     def __init__(self, color, pos, num = 10, size = (100, 150)) -> None:
#         self.color=color
#         self.x, self.y = pos
#         self.num = num
#         self.w, self.h = size
    
#     def show(self):
#         # 카드 테두리
#         pygame.draw.rect(screen, (0, 0, 0), (self.x-1, self.y-1, self.w+2, self.h+2), 5)
#         # 카드 색깔
#         pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
#         if self.num == 10:
#             pass
#         else:
#             # 카드 번호
#             card_text = pygame.font.SysFont("malgungothic",50)
#             TextSurf, TextRect = text_objects(f'{self.num}',card_text)
#             TextRect.center = (self.x +50, self.y+75)
#             screen.blit(TextSurf,TextRect)

# 일시정지 함수
def pause():

    paused = True 
      
    selected_button_index = 0

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 클릭시 다시 시작 
                paused = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_button_index >= 1 :
                        selected_button_index = 0   
                    else:
                        selected_button_index += 1
                elif event.key == pygame.K_UP:
                    if selected_button_index <= 0  :
                        selected_button_index = 1   
                    else:
                        selected_button_index -= 1
                elif event.key == pygame.K_RETURN:
                    buttons[selected_button_index].action()

        pygame.draw.rect(screen, WHITE ,(screen_width/2-200,screen_height/3-100,400,400))
        pygame.draw.rect(screen, BLACK ,(screen_width/2-200,screen_height/3-100,400,400),5)
       
        
        setting_button = Button(screen_width // 2 - 100, 300, 200, 50, "Settings",action=settingScreen)
        quit_button = Button(screen_width // 2 - 100, 400, 200, 50, "Quit",action=quitGame)
        buttons = [setting_button, quit_button]

    
        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen,GRAY,buttons[selected_button_index].rect)
        screen.blit(buttons[selected_button_index].textSurf,buttons[selected_button_index].textRect)
       

        largeText = pygame.font.SysFont("malgungothic",50)
        TextSurf, TextRect = text_objects("일시 정지",largeText)
        TextRect.center = ((screen_width/2),(screen_height/3))
        screen.blit(TextSurf,TextRect)

        pygame.display.update()

# Slider 클래스 배경음, 효과음 조절
class Slider: 

    def __init__(self, screen, length, pos, slider_range, main_color = BLACK, button_color = RED):
        
        self.drag = False # 버튼을 드래그하기 위한 초기 변수 
        self.offset_x = 0

        self.screen = screen
        self.length = length # 슬라이더 크기
        self.x, self.y = pos # 슬라이더 위치
        self.min, self.max = slider_range # 슬라이더 값의 범위
        self.color1 = main_color # 선 색
        self.color2 = button_color # 버튼색

        button = pygame.rect.Rect(int(self.x + 9 / 20 * self.length), int(self.y - 1 / 20 * self.length), int(self.length * 1 / 10),int(self.length * 1 / 10))      
        
        self.value = (self.max + self.min) / 2 # 값의 초기값
        self.button_rect = button

    def draw(self): # 선, 버튼을 스크린에 그림
        pygame.draw.line(self.screen,self.color1,(self.x,self.y),(self.x+self.length,self.y),5)
        pygame.draw.rect(self.screen, self.color2, self.button_rect)

    def operate(self, Event): # pygame 메인 루프에서 event를 받아 드래그 하기 위한 함수
        if Event.type == pygame.MOUSEBUTTONDOWN:
            if Event.button == 1:
                if self.button_rect.collidepoint(Event.pos):
                    self.drag = True

                    mouse_x, mouse_y = Event.pos
                    self.offset_x = self.button_rect.x - mouse_x

        elif Event.type == pygame.MOUSEBUTTONUP:
            if Event.button == 1:
                self.drag = False

        elif Event.type == pygame.MOUSEMOTION:
            if self.drag:
                mouse_x, mouse_y = Event.pos
                self.button_rect.x = mouse_x + self.offset_x
                if self.button_rect.x <= self.x  : # 드래그 제한
                    self.button_rect.x = self.x  

                elif self.button_rect.x >= (self.x + self.length) - 1 / 10 * self.length:
                    self.button_rect.x = int((self.x + self.length) - 1 / 10 * self.length)
        
        self.value = self.max + (self.min - self.max) * (1 - (self.button_rect.x - self.x) / ( 9 / 10 * self.length)) # value 수정
     
    # value을 text로 출력 
    def text_draw(self, name, pos ,color = BLACK , size = 20):
        FONT = pygame.font.SysFont("malgungothic",size)
        text = FONT.render("{} : {}".format(name, int(self.value)) , True, color)
        text_rect = text.get_rect()
        text_rect.center = pos

        self.screen.blit(text, text_rect)

# 화면 설정 -> 사이즈마다 구현해야 함
def screenSize():
    screen_width = 1280
    screen_height = 800
    screen = pygame.display.set_mode((screen_width,screen_height))
 
# 조작키 설정
def controlButtonSetting():
    pass

# 설정 초기화
def settingInit():
    pass

# 설정 저장
def settingSave():
    pass



if __name__=='__main__':
    # 화면 설정
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("UNO Game")
    startScreen()


