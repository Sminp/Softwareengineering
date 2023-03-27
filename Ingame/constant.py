"""상수 즉 자주 쓰는 것들을 모두 모아서 적어놓는 공간이야 예를 들어 글꼴, 색깔, 카드 번호 이런 것들도 다 적는 공간이야."""

import pygame

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# SCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT)            # 이건 많이 안 쓸 것 같아서 일단 보류

# 글꼴
MALGUNGOTHIC = "malgungothic"

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 80, 0)

# 카드 크기
CARD_HEIGHT = 585 / 5
CARD_WIDTH = 410 / 5
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

# # 카드
# RED_0 = pygame.transform.scale(pygame.image.load("image/card_img/red_0.png"), CARD_SIZE).convert_alpha()
# RED_1 = pygame.transform.scale(pygame.image.load("image/card_img/red_1.png"), CARD_SIZE).convert_alpha()
# RED_2 = pygame.transform.scale(pygame.image.load("image/card_img/red_2.png"), CARD_SIZE).convert_alpha()
# RED_3 = pygame.transform.scale(pygame.image.load("image/card_img/red_3.png"), CARD_SIZE).convert_alpha()
# RED_4 = pygame.transform.scale(pygame.image.load("image/card_img/red_4.png"), CARD_SIZE).convert_alpha()
# RED_5 = pygame.transform.scale(pygame.image.load("image/card_img/red_5.png"), CARD_SIZE).convert_alpha()
# RED_6 = pygame.transform.scale(pygame.image.load("image/card_img/red_6.png"), CARD_SIZE).convert_alpha()
# RED_7 = pygame.transform.scale(pygame.image.load("image/card_img/red_7.png"), CARD_SIZE).convert_alpha()
# RED_8 = pygame.transform.scale(pygame.image.load("image/card_img/red_8.png"), CARD_SIZE).convert_alpha()
# RED_9 = pygame.transform.scale(pygame.image.load("image/card_img/red_9.png"), CARD_SIZE).convert_alpha()
# RED_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/red_change.png"), CARD_SIZE).convert_alpha()
# RED_PASS = pygame.transform.scale(pygame.image.load("image/card_img/red_pass.png"), CARD_SIZE).convert_alpha()
# RED_PLUS_TWO = pygame.transform.scale(pygame.image.load("image/card_img/red_plus_two.png"), CARD_SIZE).convert_alpha()
#
# GREEN_0 = pygame.transform.scale(pygame.image.load("image/card_img/green_0.png"), CARD_SIZE).convert_alpha()
# GREEN_1 = pygame.transform.scale(pygame.image.load("image/card_img/green_1.png"), CARD_SIZE).convert_alpha()
# GREEN_2 = pygame.transform.scale(pygame.image.load("image/card_img/green_2.png"), CARD_SIZE).convert_alpha()
# GREEN_3 = pygame.transform.scale(pygame.image.load("image/card_img/green_3.png"), CARD_SIZE).convert_alpha()
# GREEN_4 = pygame.transform.scale(pygame.image.load("image/card_img/green_4.png"), CARD_SIZE).convert_alpha()
# GREEN_5 = pygame.transform.scale(pygame.image.load("image/card_img/green_5.png"), CARD_SIZE).convert_alpha()
# GREEN_6 = pygame.transform.scale(pygame.image.load("image/card_img/green_6.png"), CARD_SIZE).convert_alpha()
# GREEN_7 = pygame.transform.scale(pygame.image.load("image/card_img/green_7.png"), CARD_SIZE).convert_alpha()
# GREEN_8 = pygame.transform.scale(pygame.image.load("image/card_img/green_8.png"), CARD_SIZE).convert_alpha()
# GREEN_9 = pygame.transform.scale(pygame.image.load("image/card_img/green_9.png"), CARD_SIZE).convert_alpha()
# GREEN_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/green_change.png"), CARD_SIZE).convert_alpha()
# GREEN_PASS = pygame.transform.scale(pygame.image.load("image/card_img/green_pass.png"), CARD_SIZE).convert_alpha()
# GREEN_PLUS_TWO = pygame.transform.scale(pygame.image.load("image/card_img/green_plus_two.png"), CARD_SIZE).convert_alpha()
#
# BLUE_0 = pygame.transform.scale(pygame.image.load("image/card_img/blue_0.png"), CARD_SIZE).convert_alpha()
# BLUE_1 = pygame.transform.scale(pygame.image.load("image/card_img/blue_1.png"), CARD_SIZE).convert_alpha()
# BLUE_2 = pygame.transform.scale(pygame.image.load("image/card_img/blue_2.png"), CARD_SIZE).convert_alpha()
# BLUE_3 = pygame.transform.scale(pygame.image.load("image/card_img/blue_3.png"), CARD_SIZE).convert_alpha()
# BLUE_4 = pygame.transform.scale(pygame.image.load("image/card_img/blue_4.png"), CARD_SIZE).convert_alpha()
# BLUE_5 = pygame.transform.scale(pygame.image.load("image/card_img/blue_5.png"), CARD_SIZE).convert_alpha()
# BLUE_6 = pygame.transform.scale(pygame.image.load("image/card_img/blue_6.png"), CARD_SIZE).convert_alpha()
# BLUE_7 = pygame.transform.scale(pygame.image.load("image/card_img/blue_7.png"), CARD_SIZE).convert_alpha()
# BLUE_8 = pygame.transform.scale(pygame.image.load("image/card_img/blue_8.png"), CARD_SIZE).convert_alpha()
# BLUE_9 = pygame.transform.scale(pygame.image.load("image/card_img/blue_9.png"), CARD_SIZE).convert_alpha()
# BLUE_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/blue_change.png"), CARD_SIZE).convert_alpha()
# BLUE_PASS = pygame.transform.scale(pygame.image.load("image/card_img/blue_pass.png"), CARD_SIZE).convert_alpha()
# BLUE_PLUS_TWO = pygame.transform.scale(pygame.image.load("image/card_img/blue_plus_two.png"), CARD_SIZE).convert_alpha()
#
# BACK = pygame.transform.scale(pygame.image.load("image/card_img/back.png"), CARD_SIZE).convert_alpha()
# WILD = pygame.transform.scale(pygame.image.load("image/card_img/wild.png"), CARD_SIZE).convert_alpha()
# WILD_DRAW_FOUR = pygame.transform.scale(pygame.image.load("image/card_img/wild_draw_four.png"), CARD_SIZE).convert_alpha()