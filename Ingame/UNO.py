import pygame
import sys
# from game_functions import *

pygame.init()

# 색상
black = (0,0,0)
white = (255,255,255)
gray = (200,200,200)
red = (200,0,0)
green = (0,80,0)

# 상수
# 카드 리스트 이미지 넣고 인덱스로 접근 (안은 튜플 앞, 뒤)
CARD_LIST = [(pygame.image.load("Ingame/image/UNO-Zeros.png"), pygame.image.load("Ingame/image/UNO-Back.png")),
             (pygame.image.load("Ingame/image/UNO-Front.png"), pygame.image.load("Ingame/image/UNO-Back.png")),
             (pygame.image.load("Ingame/image/UNO-Front.png"), pygame.image.load("Ingame/image/UNO-Back.png"))]

# 카드 크기
CARD_HEIGHT = 585 / 5
CARD_WIDTH = 410 / 5

# 그리고 좌표도 화면 크기 조정 때문에 다 변수로 만들어야 될 것 같아.

# 색깔
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


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
    textSurface = font.render(text,True,black)
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


        screen.fill(white)

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
        pygame.draw.rect(screen,gray,buttons[selected_button_index].rect)
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

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                # 강제 종료
                if event.key == pygame.K_ESCAPE:
                    # 일시정지 함수 적기
                    pass
        
        screen.fill(green)
        for i in range(len(playerRect)):
            pygame.draw.rect(screen,white,playerRect[i],width=0)

        for i in range(len(playerRect)):
            sur = font.render("player {}".format(i+1),True,black)
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

        text = font.render("You",True,black)
        screen.blit(text,playerXY)
    

        pygame.display.update()

            
# 설정 화면 
def settingScreen():
    
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        screen.fill(white)

        # 임시, 버튼을 눌렀을 때 화면이 전환되는 지 확인하는 용도
        largeText = pygame.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("설정 화면",largeText)
        TextRect.center = ((screen_width/2),(screen_height/5))
        screen.blit(TextSurf,TextRect)

        pygame.display.update()

# 버튼 클래스
class Button:
    def __init__(self,x,y,width,height,text,font_size=30,font_name='malgungothic', color=white, hover_color=gray,action=None):
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




if __name__=='__main__':
    # 화면 설정
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("UNO Game")
    startScreen()


