import pygame
import sys

pygame.init()

# 색상
black = (0,0,0)
white = (255,255,255)
gray = (200,200,200)
red = (200,0,0)


# 화면 크기
screen_width = 800
screen_height = 600

# 화면 설정
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("UNO Game")

# 게임 종료
def quitGame():
    pygame.quit()
    sys.exit() 

# 텍스트 설정
def text_objects(text,font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()


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

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        screen.fill(white)
        
        # 임시, 버튼을 눌렀을 때 화면이 전환되는 지 확인하는 용도
        largeText = pygame.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("게임 화면",largeText)
        TextRect.center = ((screen_width/2),(screen_height/5))
        screen.blit(TextSurf,TextRect)

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

   
startScreen()

