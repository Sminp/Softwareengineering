import pygame
import sys
from game_functions import *
from constant import *
from settings import *

img_basic_address = './image/'


# 텍스트 구현
def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.SysFont(text_font, text_size)
    new_text = new_font.render(message, pygame.K_0, text_color)  # pygame.K_0가 의미하는 것은?
    return new_text


def background_img_load(filename: str, size=(SCREEN_WIDTH, SCREEN_HEIGHT)) -> object:
    background_img = pygame.image.load(filename)
    return pygame.transform.scale(background_img, (size[0], size[1]))


def terminate():
    pygame.quit()
    sys.exit()


class UNOGame():
    """UNOGame 시작화면 및 설정화면을 나타냅니다."""

    def __init__(self):
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background_color = WHITE
        self.font = MALGUNGOTHIC
        self.player_num = 2
        self.difficulty = 1
        self.story_screen = False
        self.screen.fill(self.background_color)
        self.mouse_pos = pygame.mouse.get_pos()
        self.keysetting = 1
        self.menu = True
        pygame.display.update()
        

    # 시작 화면
    def main_menu(self):
        pygame.init()
        self.screen.blit(background_img_load("./image/title_image/title_background.jpg"), (0, 0))

        selected = 0

        while self.menu:
            # 안정적으로 소리가 나오기 위한 코드 - 이해하면 지우기
            # pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()
            # 효과음 넣기 - 해결하면 지우기
            # sound = pygame.mixer.Sound('./sound/menu.wav')
            self.screen.blit(background_img_load("./image/title_image/title_background.jpg"), (0, 0))
            normal_button = Button(self.screen, self.screen_width*(1/4), self.screen_height*(5/8), "./image/title_image/title_menu_image/normalmode_button.png", 100, 230)
            story_button = Button(self.screen,self.screen_width*(1/4)+100, self.screen_height*(5/8),"./image/title_image/title_menu_image/storymode_button.png",100,230)
            menu_button = Button(self.screen, self.screen_width*(1/4)+200, self.screen_height*(5/8), "./image/title_image/title_menu_image/setting_button.png", 100, 230)
            end_button = Button(self.screen, self.screen_width*(1/4)+300, self.screen_height*(5/8), "./image/title_image/title_menu_image/end_button.png", 100, 230)
            button_list = [normal_button, story_button, menu_button, end_button]
            normal_button.show_button()
            story_button.show_button()
            menu_button.show_button()
            end_button.show_button()
            self.mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, YELLOW,
                             [button_list[selected].x, button_list[selected].y, button_list[selected].width,
                              button_list[selected].height], 5)

            # 이벤트를 발생시키는 입력
            for event in pygame.event.get():
                # 창 버튼
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if self.keysetting == 1:
                        if event.key == pygame.K_LEFT:
                            # sound.play()
                            if selected <= 0:
                                selected = 0
                            else:
                                selected = selected - 1
                        elif event.key == pygame.K_RIGHT:
                            if selected >= 3:
                                selected = 3
                            else:
                                selected += 1
                    if self.keysetting == 2:
                        if event.key == pygame.K_a:
                            # sound.play()
                            if selected <= 0:
                                selected = 0
                            else:
                                selected = selected - 1
                        elif event.key == pygame.K_d:
                            if selected >= 2:
                                selected = 2
                            else:
                                selected += 1
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            # self.lobby_screen()
                            self.story()
                        elif selected == 1:
                            self.setting_screen()
                        else:
                            pygame.quit()
                            sys.exit()
                # 마우스 입력
                if event.type == pygame.MOUSEBUTTONUP:
                    if button_list[0].x <= self.mouse_pos[0] <= button_list[0].width + button_list[0].x and \
                            button_list[
                                0].y <= self.mouse_pos[1] <= button_list[0].y + button_list[0].height:
                        self.lobby_screen()
                    if button_list[1].x <= self.mouse_pos[0] <= button_list[1].width + button_list[1].x and \
                            button_list[
                                1].y <= self.mouse_pos[1] <= button_list[1].y + button_list[1].height:
                        self.setting_screen()
                    if button_list[2].x <= self.mouse_pos[0] <= button_list[2].width + button_list[2].x and \
                            button_list[
                                2].y <= self.mouse_pos[1] <= button_list[2].y + button_list[2].height:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            pygame.display.set_caption("UNO!")

    def lobby_screen(self):

        pygame.init()

        self.screen.blit(background_img_load("./image/playing_background.png"), (0, 0))

        font = pygame.font.SysFont(self.font, 30)
        name_text = "player"
        text_surface = font.render(name_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.screen_width *(3/5), self.screen_height *(2/3)))

        computer_rect = []
        for i in range(5):
            rect = pygame.Rect(0, 100 * i + (i + 1) * ((self.screen_height - 500) / 6), self.screen_width/5, self.screen_height/6)
            if i == 0:
                label = "computer1"
            else:
                label = "add"
            computer_rect.append([rect, label])

        # 아직 게임 시작 버튼이 없어서 못 넣음 
        gamestart_button = Button(self.screen, self.screen_width*(2/5), self.screen_height*(1/4), "./image/playingImage/gamestartbutton.png", 300, 150)
        gamestart_button.show_button()

        input_active = False
        lobby = True

        while lobby:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if text_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False

                    if gamestart_button.x <= mouse_pos[
                        0] <= gamestart_button.width + gamestart_button.x and gamestart_button.y <= mouse_pos[
                        1] <= gamestart_button.y + gamestart_button.height:
                        result = 1
                        for rect, text in computer_rect:
                            if text != "add":
                                result += 1
                        uno_ = Game(result,player_name=name_text)
                        uno_.startgame()

                    for i in range(len(computer_rect)):
                        if i == 0:
                            continue
                        else:
                            if computer_rect[i][0].collidepoint(event.pos):
                                if computer_rect[i][1] == "add" and computer_rect[i - 1][1] != "add":
                                    computer_rect[i][1] = "computer{}".format(i + 1)
                                else:
                                    if i == 4:
                                        computer_rect[i][1] = "add"
                                    else:
                                        if computer_rect[i + 1][1] == "add":
                                            computer_rect[i][1] = "add"

                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            name_text = name_text[:-1]
                        else:
                            name_text += event.unicode
                        text_surface = font.render(name_text, True, WHITE)
                        text_rect.size = text_surface.get_size()

            self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
            self.screen.blit(text_surface, text_rect)
            gamestart_button.show_button()

            for rect, label in computer_rect:
                pygame.draw.rect(self.screen, WHITE, rect)
                label_surface = font.render(label, True, BLACK)
                self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

            if input_active:
                pygame.draw.line(self.screen, WHITE, (text_rect.x + text_rect.w, text_rect.y),
                                 (text_rect.x + text_rect.w, text_rect.y + text_rect.h), 2)
            else:
                self.screen.blit(background_img_load("./image/PlayingBackground.png"), (0, 0))
                self.screen.blit(text_surface, text_rect)
                gamestart_button.show_button()
                for rect, label in computer_rect:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    label_surface = font.render(label, True, BLACK)
                    self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

            pygame.display.update()

    def setting_screen(self):

        pygame.init()
        setting = True
        selected = 1
        
        rect = pygame.Rect(self.screen_width*(8/11), self.screen_height*(7/11), 50, 50)

        # 배경음, 효과음 slider
        
        backgrounder_slider = Slider(self.screen, self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(4/13)), (0, 100))
        sound_effect_slider = Slider(self.screen, self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(6/15)), (0, 100))

        while setting:
        
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                    
                backgrounder_slider.operate(event)
                sound_effect_slider.operate(event)

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
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if sizefull_button.get_rect().collidepoint(mouse_pos): 
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
                    elif size16_button.get_rect().collidepoint(mouse_pos):
                        print("zmf")
                        self.screen_width = 1280
                        self.screen_height = 720
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                        backgrounder_slider.set_value(self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(4/13)))
                        sound_effect_slider.set_value(self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(6/15)))
                        rect.x = self.screen_width*(8/11)
                        rect.y = self.screen_height*(7/11)
                    elif size4_button.get_rect().collidepoint(mouse_pos):
                        self.screen_width = 800
                        self.screen_height = 600
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                        backgrounder_slider.set_value(self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(4/13)))
                        sound_effect_slider.set_value(self.screen_width/2, (self.screen_width*(3/10), self.screen_height*(6/15)))
                        rect.x = self.screen_width*(8/11)
                        rect.y = self.screen_height*(7/11)
                    elif control_button.get_rect().collidepoint(mouse_pos):
                        self.key_select_screen()
                    elif close_button.get_rect().collidepoint(mouse_pos):
                        self.main_menu()
                        
                    elif rect.collidepoint(mouse_pos):
                        if rect.x == int(self.screen_width*(8/11)):
                            rect.x += 50
                            rect= pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                        elif rect.x == int(self.screen_width*(8/11)) + 50:
                            rect.x -= 50
                            rect= pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                       

            
            self.screen.blit(background_img_load("./image/setting image/settingbackground.jpg"), (0,0))
            pygame.draw.rect(self.screen, WHITE, (self.screen_width*(1/9), self.screen_height*(2/8),self.screen_width*(7/9), self.screen_height*(6/10)))
            
            

            # 설정화면 텍스트 표시

            setting_text = text_format("SETTING", MALGUNGOTHIC, 35, WHITE)
            self.screen.blit(setting_text, (self.screen_width*(1/8), self.screen_height*(1/7)))

            # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야 함
            screen_setting_text = text_format("화면크기", MALGUNGOTHIC, 20, BLACK)
            self.screen.blit(screen_setting_text, (self.screen_width*(1/8), self.screen_height*(8/15)))

            # 화면 설정 버튼 - 변수명 바꿔야 함
            close_button = Button(self.screen, self.screen_width*(5/6), self.screen_height*(3/11), "./image/setting image/settingclose.png", 20, 20)
            sizefull_button = Button(self.screen, self.screen_width*(3/10), self.screen_height*(1/2), "./image/setting image/full.jpg", 100, 50)
            size16_button = Button(self.screen, self.screen_width*(5/10), self.screen_height*(1/2), "./image/setting image/169.jpg", 100, 50)
            size4_button = Button(self.screen, self.screen_width*(7/10), self.screen_height*(1/2), "./image/setting image/43.jpg", 100, 50)
            close_button.show_button()
            sizefull_button.show_button()
            size16_button.show_button()
            size4_button.show_button()

            # 배경음, 효과음 그림
            backgrounder_slider.draw()
            backgrounder_slider.draw_value('배경음', (self.screen_width*(1/8), self.screen_height*(2/7)))
            sound_effect_slider.draw()
            sound_effect_slider.draw_value('효과음', (self.screen_width*(1/8), self.screen_height*(3/8)))

            # 조작키 설정, 설정 초기화, 설정 저장 버튼
            control_button = Button(self.screen, self.screen_width*(1/8), self.screen_height*(7/11), "./image/setting image/keysetting.jpg", 100, 50)
            settinginit_button = Button(self.screen, self.screen_width*(1/8), self.screen_height*(6/8), "./image/setting image/settinginit.jpg", 100, 50)
            settingsave_button = Button(self.screen, self.screen_width*(8/11), self.screen_height*(6/8), "./image/setting image/settingsave.jpg", 100, 50)
            control_button.show_button()
            settinginit_button.show_button()
            settingsave_button.show_button()
            buttons = [control_button, settinginit_button, settingsave_button]
            
            settingcolor_button = Button(self.screen, self.screen_width*(8/11), self.screen_height*(7/11), "./image/setting image/rect.jpg", 100, 50)
            settingcolor_button.show_button()
            pygame.draw.rect(self.screen, BLACK, rect)

            pygame.display.update()
            
    def key_select_screen(self):
        key_select = True
        
        setting_key1 = Button(self.screen,self.screen_width*(1/3), self.screen_height*(1/3), "./image/button_img.png", 50, 50)
        setting_key2 = Button(self.screen,self.screen_width*(1/3), self.screen_height*(2/3), "./image/button_img.png", 50, 50)
        
        while key_select:
            pygame.draw.rect(self.screen, WHITE, (self.screen_width*(1/9), self.screen_height*(2/8),self.screen_width*(7/9), self.screen_height*(6/10)))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if setting_key1.get_rect().collidepoint(mouse_pos):
                        self.keysetting = 1
                        key_select = False
                    elif setting_key2.get_rect().collidepoint(mouse_pos):
                        self.keysetting = 2
                        key_select = False
                        
            setting_key1.show_button()
            setting_key2.show_button()
                        
            pygame.display.update()
                    
    #스토리모드
    def story(self):

        pygame.init()
        self.story = True

        font = pygame.font.SysFont(self.font, 50)
        text = "스토리 모드"
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 5, self.screen_height // 10))

        story_map = [pygame.Rect((i * 200 + 50, self.screen_height // 2 - 25, 50, 50)) for i in range(4)]

        while self.story:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(story_map)):
                        if story_map[i].collidepoint(event.pos):
                            if i == 0:
                                self.yes_no(2,2)
                            elif i == 1:
                                self.yes_no(3,3)
                            elif i == 2:
                                self.yes_no(2,4)
                            else:
                                self.yes_no(3,5)      

            self.screen.fill(WHITE)
            self.screen.blit(text_surface, text_rect)
            for rect in story_map:
                pygame.draw.rect(self.screen, BLACK, rect)

            pygame.display.update()

    # 지역 선택하면 플레이할 건지 물어보는 창
    def yes_no(self,player_num,difficulty):
        yes_no = True
        self.story_screen = False
        
        yes_button = Button(self.screen, self.screen_width*(3/7), self.screen_height*(2/5), "./image/button_img.png", 100, 50)
        no_button = Button(self.screen, self.screen_width*(3/7), self.screen_height*(2/5)+100, "./image/button_img.png", 100, 50)

        while yes_no:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭시 다시 시작
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button.get_rect().collidepoint(mouse_pos):
                        self.player_num = player_num
                        self.difficulty = difficulty
                        uno = Game(self.player_num, self.difficulty)
                        uno.startgame()
                        yes_no = False
                    elif no_button.get_rect().collidepoint(mouse_pos):
                        self.story_screen = True
                        yes_no = False
            pygame.draw.rect(self.screen, WHITE, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400))
            pygame.draw.rect(self.screen, BLACK, (self.screen_width / 2 - 200, self.screen_height / 3 - 100, 400, 400), 5)
            ask_text = text_format("대전을 시작하겠습니까?", MALGUNGOTHIC, 30, BLACK)
            ask_text_rect = ask_text.get_rect(center=(self.screen_width/2,self.screen_height/3))
            yes_button.show_button()
            no_button.show_button()
            self.screen.blit(ask_text, ask_text_rect)

            pygame.display.update()


# 버튼 클래스 안에 하이라이트 그림 넣으면 안되려나?
# 버튼 클래스
class Button:
    def __init__(self, screen, x, y, img, width, height):
        self.screen = screen
        # self.rect = pygame.Rect(x,y, 30, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = (x,y)

        self.img = pygame.transform.scale(pygame.image.load(img), [width, height])
        self.rect = self.img.get_rect()
        self.rect.center = self.position
        self.cliked_num = 0

    def show_button(self):
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

    def cliked(self):
        self.screen.blit(self.img, (self.x, self.y -5))
        self.cliked_num += 1

    def check_cliked_num(self):
        pass
    
    def get_rect(self):
        return self.rect
    
    


if __name__ == '__main__':
    uno = UNOGame()
    uno.main_menu()
