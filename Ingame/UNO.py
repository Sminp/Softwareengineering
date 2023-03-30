import pygame
import sys
from game_functions import *
from constant import *
from settings import *
import math

img_basic_address = './image/'


class UNOGame():
    """UNOGame 시작화면 밑 설정화면을 나타냅니다."""

    def __init__(self):
        pygame.init()
        # self.background = pygame.image.load("Ingame/image/TitleImage/TitleBackground.jpg")
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.background_Color = WHITE
        self.playernum = 2
        self.difficulty = 1
        self.font = MALGUNGOTHIC
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(self.background_Color)
        # self.screen.blit(self.background, (0, 0))
        self.mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()

    # 텍스트 구현
    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.SysFont(textFont, textSize)
        newText = newFont.render(message, pygame.K_0, textColor)
        return newText

    # 시작 화면
    def main_menu(self):
        pygame.init()
        self.screen_background_img = pygame.image.load("./image/TitleImage/TitleBackground.jpg")
        self.background = pygame.transform.scale(self.screen_background_img, (800, 600))
        self.screen.blit(self.background, (0, 0))

        # 기본 버튼이 1 (왼쪽 시작 버튼) - 해결하면 지우기
        selected = 1

        menu = True

        # 좌표, 크기 다 바꿔야함
        start_button = Button(self.screen, 300, 500, "./image/TitleImage/StartButton.png",100, 100)

        menu_button = Button(self.screen, 400, 500, "./image/TitleImage/MenuButton.png", 100, 100)

        end_button = Button(self.screen, 500, 500, "./image/TitleImage/EndButton.png", 100, 100)
        button_list = [start_button, menu_button, end_button]
        
        while menu:
            # 안정적으로 소리가 나오기 위한 코드 - 이해하면 지우기
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # 효과음 넣기 - 해결하면 지우기
            # sound = pygame.mixer.Sound('./sound/menu.wav')

            # 이벤트를 발생시키는 입력
            for event in pygame.event.get():
                # 창 버튼
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # 마우스 입력
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos= pygame.mouse.get_pos()
                    if button_list[0].x <= mouse_pos[0] <= button_list[0].width + button_list[0].x and button_list[0].y <= mouse_pos[1] <= button_list[0].y+button_list[0].height:
                        self.lobby_screen()
                    if button_list[1].x <= mouse_pos[0] <= button_list[1].width + button_list[1].x and button_list[1].y <= mouse_pos[1] <= button_list[1].y+button_list[1].height:
                        self.setting_screen()
                    if button_list[2].x <= mouse_pos[0] <= button_list[2].width + button_list[2].x and button_list[2].y <= mouse_pos[1] <= button_list[2].y+button_list[2].height:
                        pygame.quit()
                        sys.exit()
                        


            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")

    def lobby_screen(self):
    
        pygame.init()

        self.background = pygame.image.load("./image/PlayingBackground.png")
        self.background = pygame.transform.scale(self.background,(800,700))
        self.screen.blit(self.background,(0,0))

        font = pygame.font.SysFont("malgungothic", 25)
        text = "player"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen_width // 2 + 70, self.screen_height // 2 + 150))

        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0,100*i+(i+1)*((self.screen_height-500)/6),150,110)
            if i == 0:
                label = "computer1"
            else:
                label = "add"
            computer_rect.append([rect,label])

        # 아직 게임 시작 버튼이 없어서 못 넣음 
        gamestart_button = Button(self.screen, 350, 150, "./image/button_img.png", 200, 100)
        
        input_active = False
        lobby = True

        while lobby:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos= pygame.mouse.get_pos()
                    if text_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False

                    if gamestart_button.x <= mouse_pos[0] <= gamestart_button.width + gamestart_button.x and gamestart_button.y <= mouse_pos[1] <= gamestart_button.y+gamestart_button.height:
                        result = 1
                        for rect,text in computer_rect:
                          if text != "add":
                              result += 1
                        uno = game(result)
                        uno.startgame() 
            

                        
                    for i in range(len(computer_rect)):
                        if i == 0 :
                            continue
                        else:
                            if computer_rect[i][0].collidepoint(event.pos):
                                if computer_rect[i][1] == "add" and computer_rect[i-1][1] != "add":
                                    computer_rect[i][1]  = "computer{}".format(i+1)
                                else:
                                    if i == 4:
                                        computer_rect[i][1] = "add"
                                    else:
                                        if computer_rect[i+1][1] == "add":
                                            computer_rect[i][1] = "add"
                    
  
                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                        text_surface = font.render(text, True, BLACK)
                        text_rect.size = text_surface.get_size()

            self.screen.blit(self.background,(0,0))
            self.screen.blit(text_surface, text_rect)
            gamestart_button.show_botton()


            for rect, label in computer_rect:
                pygame.draw.rect(self.screen,WHITE,rect)
                label_surface = font.render(label, True, BLACK)
                self.screen.blit(label_surface,(rect.x + 10 , rect.y +10))

            if input_active:
                pygame.draw.line(self.screen,BLACK,(text_rect.x+text_rect.w,text_rect.y),(text_rect.x+text_rect.w,text_rect.y+text_rect.h),2)
            else:
                self.screen.blit(self.background,(0,0))
                self.screen.blit(text_surface, text_rect)
                gamestart_button.show_botton()
                for rect, label in computer_rect:
                    pygame.draw.rect(self.screen,WHITE,rect)
                    label_surface = font.render(label, True, BLACK)
                    self.screen.blit(label_surface,(rect.x + 10 , rect.y +10))

            pygame.display.update()

    def setting_screen(self):
        game_exit = False

        # 배경음, 효과음 slider
        backgroundsound_slider = Slider(self.screen, 300, (250, 180), (0, 100))
        soundeffect_slider = Slider(self.screen, 300, (250, 250), (0, 100))

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                backgroundsound_slider.operate(event)
                soundeffect_slider.operate(event)

                # 키보드 버튼
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # sound.play()
                        if selected <= 1:
                            selected = 1
                        else:
                            selected = selected 
                    elif event.key == pygame.K_RIGHT:
                        # sound.play()
                        if selected >= 3:
                            selected = 3
                        else:
                            selected = selected + 1
                    if event.key == pygame.K_RETURN:
                        if selected <= 1:
                            # 버튼 입력 후 시작 함수 실행 - 해결하면 지우기
                            pass
                        if selected == 2:
                            # 버튼 입력 후 설정 함수 실행 - 해결하면 지우기
                            pass
                        if selected >= 3:
                            # 버튼 입력 후 시작 함수 실행 - 해결하면 지우기
                            pass

            self.screen.fill(WHITE)

            # 설정화면 텍스트 표시

            setting_text=self.text_format("설정 화면",MALGUNGOTHIC,50,BLACK)
            self.screen.blit(setting_text,(80,50))

            # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야 함
            screen_setting_text=self.text_format("화면설정",MALGUNGOTHIC,50,BLACK)
            self.screen.blit(screen_setting_text,(80, 300))

            # 화면 설정 버튼 - 변수명 바꿔야 함
            gamestart_button = Button(self.screen, 600, 50, "./image/button_img.png", 100, 50)
            sizefull_button = Button(self.screen, 270, 315, "./image/button_img.png", 100, 50)
            size16_button = Button(self.screen, 420, 315, "./image/button_img.png", 100, 50)
            size4_button = Button(self.screen, 570, 315, "./image/button_img.png", 100, 50)

            # 배경음, 효과음 그림
            backgroundsound_slider.draw()
            backgroundsound_slider.draw_value('배경음', (130, 180))
            soundeffect_slider.draw()
            soundeffect_slider.draw_value('효과음', (130, 250))

            # 조작키 설정, 설정 초기화, 설정 저장 버튼
            control_button = Button(self.screen, 80, 400, "./image/button_img.png", 100, 50)
            settinginit_button = Button(self.screen, 80, 500, "./image/button_img.png", 100, 50)
            settingsave_button = Button(self.screen, SCREEN_WIDTH // 2 + 200, 500, "./image/button_img.png", 100, 50)
            buttons = [control_button, settinginit_button, settingsave_button]

            pygame.display.update()


# 버트 클래스
# 버튼 클래스
class Button:
    def __init__(self, screen, x, y, img, width, height):
        self.screen = screen
        # self.rect = pygame.Rect(x,y, 30, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.img = pygame.transform.scale(pygame.image.load(img), [width, height])
        # self.action = action

        self.screen.blit(self.img, (x, y))

    def show_botton(self):
        self.screen.blit(self.img, (self.x, self.y))

        # mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        # if x + width > mouse[0] > x and y + height > mouse[1] > y:
        #     # 마우스를 버튼위에 올렸을 때 색깔 변함
        #     pygame.draw.rect(screen, self.hover_color, self.rect)
        #     if click[0] == 1 and action != None:
        #         # 클릭하면 해당 버튼 기능 수행
        #         action()
        # else:
        #     pygame.draw.rect(screen, self.color, self.rect)

        # 버튼의 text 설정
        # font = pygame.font.SysFont(font_name,font_size)
        # self.textSurf = font.render(text,True,BLACK)
        # self.textRect = self.textSurf.get_rect()
        # self.textRect.center = ((x + width/2),(y + height/2))
        # screen.blit(self.textSurf, self.textRect)



# 카드 뒤집는 애니메이션 구현
"""
        # 타이머 설정
        tmr += 1
        if tmr == 90:
            tmr = 0
        # 타이머 계산도 다시
        txt = font.render(str(10 - tmr // 10 - 1), True, WHITE)
        screen.blit(txt, [400, 10])
        clock.tick(30)

        # 이거는 전환하는 거 확인하려고 만든거
        if tmr < 45:
            selected_img = pygame.image.load(CARD_IMAGE_LIST[-1])
            img_before = pygame.transform.scale(selected_img,
                                                [CARD_WIDTH * math.cos(math.radians(tmr * 2)), CARD_HEIGHT])
            img_before_rect = img_before.get_rect()
            screen.blit(img_before, [350 + tmr * 2 / 45 * 50, 200])
        else:
            up_img = pygame.image.load(uno_deck_dic[discards[-1]])
            img_after = pygame.transform.scale(up_img,
                                               [CARD_WIDTH * math.sin(math.radians(tmr * 2 - 90)), CARD_HEIGHT])
            img_after_rect = img_after.get_rect()
            # 와 계산은 나중에
            screen.blit(img_after, [450 + 20 - tmr * 2 / 45 * 10, 200])
"""


if __name__ == '__main__':
    uno = UNOGame()
    uno.main_menu()

    # uno = game()
    # uno.startgame()
