import pygame
from game_functions import *
from constant import *
from settings import *


# 시작 화면    
def start_screen():

    start = True

    # 선택된 버튼의 인덱스 저장
    selected_button_index = 0

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

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


        screen.fill(WHITE)

        # 게임 제목
        large_text = pygame.font.SysFont("malgungothic",115)
        text_surf, text_rect = text_objects("UNO GAME",large_text)
        text_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/5))
        screen.blit(text_surf,text_rect)

        # 메뉴 버튼 생성 및 그리기
        single_player_button = Button(screen,SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Single Player",action=game_screen)
        setting_button = Button(screen,SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Settings",action=setting_screen)
        quit_button = Button(screen,SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Quit",action=quit_game)

        buttons = [single_player_button, setting_button, quit_button]

        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen,GRAY,buttons[selected_button_index].rect)
        screen.blit(buttons[selected_button_index].text_surf,buttons[selected_button_index].text_rect)
        
        pygame.display.update()

# 게임 화면
def game_screen():

    game_exit = False
    player_xy = (480,400)
    player_rect = [(10,100*i+(i+1)*((SCREEN_HEIGHT-500)/6),180,100) for i in range(5)]
    font = pygame.font.Font(None,30)
    clock = pygame.time.Clock()
    clicked = False
    tmr = 0

    # 카드 생성, 반환값 리스트
    uno_deck = build_deck()
    make_dict(uno_deck, CARD_LIST)
    # 카드 무작위 셔플, 반환값 리스트
    uno_deck = shuffle_deck(uno_deck)
    # 게임 카드
    discards = []

    # 0 player, 1 ~ 5 computers
    players = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    # 아마 2차 과제
    # num_players = int(input("player의 수를 입력하세요: "))
    # while num_players < 2 or num_players > 4:
    #     num_players = int(input("2~4 명의 player만 가능합니다. 다시 입력하세요:"))

    # 아마 인원수에 따라 바꿀 듯
    # for player in range(num_players):
    for player in range(2):
        players.append(draw_card(uno_deck, 5))

    # 0 나, 1 컴퓨터 - 게임 차례
    player_turn = 0
    # reverse 방향 전환
    player_direction = 1
    playing = True
    discards.append(uno_deck.pop(0))

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                # 강제 종료
                if event.key == pygame.K_ESCAPE:
                    # 일시정지 함수 적기
                    pause()
 
        screen.fill(GREEN)
        for i in range(len(player_rect)):
            pygame.draw.rect(screen,WHITE,player_rect[i],width=0)

        for i in range(len(player_rect)):
            sur = font.render("player {}".format(i+1),True,BLACK)
            screen.blit(sur,(player_rect[i][0],player_rect[i][1]))
        
        # 마우스 위치
        mouse_x, mouse_y = pygame.mouse.get_pos()
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
        if 50 <= mouse_x <= 50 + CARD_WIDTH and 400 <= mouse_y <= 400 + CARD_HEIGHT and mBtn1 == 1:
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
        screen.blit(text,player_xy)
    

        pygame.display.update()

            
# 설정 화면 
def setting_screen():
    
    game_exit = False

    # 배경음, 효과음 slider
    backgroundsound_slider = Slider(screen, 300, (250,180),(0,100))
    soundeffect_slider = Slider(screen, 300, (250,250),(0,100))


    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            
            backgroundsound_slider.operate(event)
            soundeffect_slider.operate(event)

        screen.fill(WHITE)

        # 설정화면 텍스트 표시
        large_text = pygame.font.SysFont("malgungothic",50)
        text_surf, text_rect = text_objects("설정 화면",large_text)
        text_rect.center = (130,50)
        screen.blit(text_surf,text_rect)

        # 화면 설정 텍스트 표시 ==>> 텍스트 표시 함수를 좀 고쳐야함
        FONT = pygame.font.SysFont("malgungothic",20)
        text = FONT.render("화면 설정" , True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (130,340)
        screen.blit(text, text_rect)

        # 화면 설정 버튼 - 변수명 바꿔야함
        sizefull_button = Button(screen,270, 315, 100, 50, "전체화면",20,color=GRAY, hover_color=YELLOW,action=screen_size)
        size16_button = Button(screen,420, 315, 100, 50, "16:9",20,color=GRAY, hover_color=YELLOW,action=setting_screen)
        size4_button = Button(screen,570, 315, 100, 50, "4:3",20,color=GRAY, hover_color=YELLOW,action=quit_game)


        # 배경음, 효과음 그림
        backgroundsound_slider.draw()
        backgroundsound_slider.text_draw('배경음',(130,180))
        soundeffect_slider.draw()
        soundeffect_slider.text_draw('효과음',(130,250))

        # 조작키 설정, 설정 초기화, 설정 저장 버튼 
        control_button = Button(screen,80, 400, 100, 50, "조작키 설정",20,color=GRAY, hover_color=YELLOW,action=game_screen)
        settinginit_button = Button(screen,80, 500, 100, 50, "설정 초기화",20,color=GRAY, hover_color=YELLOW,action=setting_screen)
        settingsave_button = Button(screen,SCREEN_WIDTH // 2 + 200, 500, 100, 50, "설정 저장",20,color=GRAY, hover_color=YELLOW,action=quit_game)

        buttons = [control_button, settinginit_button, settingsave_button]

        pygame.display.update()




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
#             text_surf, text_rect = text_objects(f'{self.num}',card_text)
#             text_rect.center = (self.x +50, self.y+75)
#             screen.blit(text_surf,text_rect)

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

        pygame.draw.rect(screen, WHITE ,(SCREEN_WIDTH/2-200,SCREEN_HEIGHT/3-100,400,400))
        pygame.draw.rect(screen, BLACK ,(SCREEN_WIDTH/2-200,SCREEN_HEIGHT/3-100,400,400),5)
       
        
        setting_button = Button(screen,SCREEN_WIDTH // 2 - 100, 300, 200, 50, "Settings",action=setting_screen)
        quit_button = Button(screen,SCREEN_WIDTH // 2 - 100, 400, 200, 50, "Quit",action=quit_game)
        buttons = [setting_button, quit_button]

    
        # 방향키로 선택된 버튼 표시
        pygame.draw.rect(screen,GRAY,buttons[selected_button_index].rect)
        screen.blit(buttons[selected_button_index].text_surf,buttons[selected_button_index].text_rect)
       

        large_text = pygame.font.SysFont("malgungothic",50)
        text_surf, text_rect = text_objects("일시 정지",large_text)
        text_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/3))
        screen.blit(text_surf,text_rect)

        pygame.display.update()


if __name__=='__main__':
    pygame.init()
    # 화면 설정
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("UNO Game")
    start_screen()


