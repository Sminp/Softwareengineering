"""상수 즉 자주 쓰는 것들을 모두 모아서 적어놓는 공간이야 예를 들어 글꼴, 색깔, 카드 번호 이런 것들도 다 적는 공간이야."""

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 글꼴
MALGUNGOTHIC = "malgungothic"
BERLIN = 'Berlin Sans FB'

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 84, 255)

# 카드 크기
CARD_WIDTH = 60
CARD_HEIGHT = 80
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

# 소리


# 버튼 리스트
NORMALMODE_BUTTON = "./image/title_image/normalmode_button.png"
STORYMODE_BUTTON = "./image/title_image/storymode_button.png"
SETTING_BUTTON = "./image/title_image/setting_button.png"
END_BUTTON = "./image/title_image/end_button.png"
TITLE_MENU_BUTTONS = [NORMALMODE_BUTTON,
                      STORYMODE_BUTTON, SETTING_BUTTON, END_BUTTON]

GAMESTART_BUTTON = "./image/playing_image/game_start_button.png"

# close_button = Button(self.screen, self.screen_width * (5 / 6), self.screen_height * (3 / 11),"", 20, 20)
CLOSE_BUTTON = "./image/setting_image/settingclose.png"
SIZEFULL_BUTTON = "./image/setting_image/full.jpg"
SIZE16_BUTTON = "./image/setting_image/169.jpg"
SIZE4_BUTTON = "./image/setting_image/43.jpg"

SIZE_BUTTONS = [SIZEFULL_BUTTON, SIZE16_BUTTON, SIZE4_BUTTON]

SETTING_CLOSE_BUTTON = "./image/setting_image/settingclose.png"
SETTING_KEY_BUTTON = "./image/setting_image/key_setting.jpg"
SETTING_INIT_BUTTON = "./image/setting_image/settinginit.jpg"
SETTINGKEY_ARROW_BUTTON = "./image/setting_image/settingkey_arrow.png"
SETTINGKEY__WASD_BUTTON = "./image/setting_image/settingkey_wasd.png"
SETTING_SAVE_BUTTON = "./image/setting_image/settingsave.jpg"
SETTING_RECT = "./image/setting_image/rect.jpg"

SLIDER_TEXT = ["전체 소리", "배경음악", "효과음"]

AMERICA_BUTTON = "./image/map_image/america.png"
MACAU_BUTTON = "./image/map_image/macau.png"
SINGAPORE_BUTTON = "./image/map_image/singapore.png"
KOREA_BUTTON = "./image/map_image/korea.png"

STORYMODE_MENU_BUTTONS = [AMERICA_BUTTON,
                          MACAU_BUTTON, SINGAPORE_BUTTON, KOREA_BUTTON]

YES_BUTTON = "./image/map_image/story_yes.jpg"
NO_BUTTON = "./image/map_image/story_no.jpg"

YESNO_BUTTONS = [YES_BUTTON, NO_BUTTON]

UNO_BUTTON = "./image/playing_image/uno_button.png"

# 카드
CARD_TYPE = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'wild'}
CARD_SKILL = {11: '_pass', 12: '_reverse', 13: '_plus_two',
              14: '_basic', 15: '_plus_four', 16: '_change'}


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
# RED_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/red_reverse.png"), CARD_SIZE).convert_alpha()
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
# GREEN_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/green_reverse.png"), CARD_SIZE).convert_alpha()
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
# BLUE_CHANGE = pygame.transform.scale(pygame.image.load("image/card_img/blue_reverse.png"), CARD_SIZE).convert_alpha()
# BLUE_PASS = pygame.transform.scale(pygame.image.load("image/card_img/blue_pass.png"), CARD_SIZE).convert_alpha()
# BLUE_PLUS_TWO = pygame.transform.scale(pygame.image.load("image/card_img/blue_plus_two.png"), CARD_SIZE).convert_alpha()
#
# BACK = pygame.transform.scale(pygame.image.load("image/card_img/back.png"), CARD_SIZE).convert_alpha()
# WILD = pygame.transform.scale(pygame.image.load("image/card_img/wild.png"), CARD_SIZE).convert_alpha()
# WILD_DRAW_FOUR = pygame.transform.scale(pygame.image.load("image/card_img/wild_plus_four.png"), CARD_SIZE).convert_alpha()
