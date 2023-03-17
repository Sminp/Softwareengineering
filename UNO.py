"""여기가 main공간이야 여기는 가장 간단할수록 좋지"""

from settings import *
import pygame as pg
import sys

pg.init()


# 화면 설정
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption("UNO Game")

# 게임 종료
def quitGame():
    pg.quit()
    sys.exit() 

# 텍스트 설정
def text_objects(text,font):
    textSurface = font.render(text,True,BLACK)
    return textSurface, textSurface.get_rect()


# 시작 화면    
def startScreen():

    start = True

    # 선택된 버튼의 인덱스 저장
    selected_button_index = 0

    while start:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()

            # 방향키로 메뉴 선택 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    if selected_button_index >= 2 :
                        selected_button_index = 0   
                    else:
                        selected_button_index += 1
                elif event.key == pg.K_UP:
                    if selected_button_index <= 0  :
                        selected_button_index = 2   
                    else:
                        selected_button_index -= 1
                elif event.key == pg.K_RETURN:
                    buttons[selected_button_index].action()


        screen.fill(WHITE)

        # 게임 제목
        largeText = pg.font.SysFont(MALGUNGOTHIC,115)
        TextSurf, TextRect = text_objects("UNO GAME",largeText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/5))
        screen.blit(TextSurf,TextRect)

        # 메뉴 버튼 생성 및 그리기
        single_player_button = Button(SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Single Player",action=gameSreen)
        setting_button = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Settings",action=settingScreen)
        quit_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Quit",action=quitGame)

        buttons = [single_player_button, setting_button, quit_button]

        # 방향키로 선택된 버튼 표시
        pg.draw.rect(screen,GRAY,buttons[selected_button_index].rect)
        screen.blit(buttons[selected_button_index].textSurf,buttons[selected_button_index].textRect)
        
        pg.display.update()

# 게임 화면
def gameScreen():

    gameExit = False

    while not gameExit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()
        
        screen.fill(WHITE)
        
        # 임시, 버튼을 눌렀을 때 화면이 전환되는 지 확인하는 용도
        largeText = pg.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("게임 화면",largeText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/5))
        screen.blit(TextSurf,TextRect)

        pg.display.update()

            
# 설정 화면 
def settingScreen():
    
    gameExit = False

    while not gameExit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()

        screen.fill(WHITE)

        # 임시, 버튼을 눌렀을 때 화면이 전환되는 지 확인하는 용도
        largeText = pg.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("설정 화면",largeText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/5))
        screen.blit(TextSurf,TextRect)

        pg.display.update()

# 버튼 클래스
class Button:
    def __init__(self,x,y,width,height,text,font_size=30,font_name='malgungothic', color=WHITE, hover_color=GRAY,action=None):
        self.rect = pg.Rect(x,y,width,height) 
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            # 마우스를 버튼위에 올렸을 때 색깔 변함
            pg.draw.rect(screen, self.hover_color, self.rect) 
            if click[0] == 1 and action != None:
                # 클릭하면 해당 버튼 기능 수행
                action()
        else: 
            pg.draw.rect(screen, self.color, self.rect)

        # 버튼의 text 설정
        font = pg.font.SysFont(font_name,font_size)
        self.textSurf, self.textRect = text_objects(text,font)
        self.textRect.center = ((x + width/2),(y + height/2))
        screen.blit(self.textSurf,self.textRect)

   
startScreen()

