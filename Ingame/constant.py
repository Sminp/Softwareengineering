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

VERMILION = (227, 66, 52)
BLUISH_GREEN = (13, 152, 186)
C_BLUE = (0, 0, 255)


# 배경화면
TITLE_BACKGROUND = "./image/title_image/title_background.bmp"
GAME_BACKGROUND = "./image/playing_image/playing_background.png"
SETTING_BACKGROUND = "./image/setting_image/setting_background.jpg"
MAP_BACKGROUND = "./image/map_image/map_background.jpg"

# 카드 크기
CARD_WIDTH = 60
CARD_HEIGHT = 80
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

# 소리
TITLE_BGM = './sound/title_bgm.mp3'
SELECT_BGM = './sound/select_sound.mp3'
PLAYING_BGM = './sound/playing_bgm.mp3'
STOTYMODE_BGM = './sound/storymode_bgm.mp3'

# 버튼 리스트
NORMALMODE_BUTTON = "./image/title_image/normalmode_button.png"
MULTI_BUTTON = "./image/title_image/multimode_button.png"
STORYMODE_BUTTON = "./image/title_image/storymode_button.png"
ACHV_BUTTON = "./image/title_image/achv_button.png"
SETTING_BUTTON = "./image/title_image/setting_button.png"
END_BUTTON = "./image/title_image/end_button.png"
TITLE_MENU_BUTTONS = [NORMALMODE_BUTTON, MULTI_BUTTON,
                      STORYMODE_BUTTON, ACHV_BUTTON, SETTING_BUTTON, END_BUTTON]

NORMALMODE_HIGHLIGHT = "./image/title_image/normalmode_highlight.png"
MULTIMODE_HIGHLIGHT = "./image/title_image/multimode_highlight.png"
STORYMODE_HIGHLIGHT = "./image/title_image/storymode_highlight.png"
ACHV_HIGHLIGHT = "./image/title_image/achv_highlight.png"
SETTING_HIGHLIGHT = "./image/title_image/setting_highlight.png"
END_HIGHLIGHT = "./image/title_image/end_highlight.png"
TITLE_MENU_HIGHLIGHTS = [NORMALMODE_HIGHLIGHT, MULTIMODE_HIGHLIGHT,
                         STORYMODE_HIGHLIGHT, ACHV_HIGHLIGHT, SETTING_HIGHLIGHT, END_HIGHLIGHT]

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
LOCK_MACAU_BUTTON = "./image/map_image/lock_macau.png"
LOCK_SINGAPORE_BUTTON = "./image/map_image/lock_singapore.png"
LOCK_KOREA_BUTTON = "./image/map_image/lock_korea.png"

STORYMODE_MENU_BUTTONS = [AMERICA_BUTTON,
                          [MACAU_BUTTON, LOCK_MACAU_BUTTON], [SINGAPORE_BUTTON, LOCK_SINGAPORE_BUTTON], [KOREA_BUTTON, LOCK_KOREA_BUTTON]]

YES_BUTTON = "./image/map_image/story_yes.jpg"
NO_BUTTON = "./image/map_image/story_no.jpg"

YESNO_BUTTONS = [YES_BUTTON, NO_BUTTON]

UNO_BUTTON = "./image/playing_image/uno_button.png"
UNO_BUTTON_HIGHLIGHT = "./image/playing_image/uno_button_highlight.png"

MAKEROOM_BUTTON = "./image/multi_image/makeroom_button.jpg"
ROOMENTER_BUTTON = "./image/multi_image/roomenter_button.jpg"


# 업적 목록
SINGLE_WIN = "./image/achv_image/singlewin_banner.png"
AMERICA_WIN = "./image/achv_image/americawin_banner.png"
MACAU_WIN = "./image/achv_image/macauwin_banner.png"
SINGAPORE_WIN = "./image/achv_image/singaporewin_banner.png"
KOREA_WIN = "./image/achv_image/koreawin_banner.png"
SPEED_MASTER = "./image/achv_image/speedmaster_banner.png"
NO_SKILL_WIN = "./image/achv_image/noskillwin_banner.png"
TURTLE_WIN = "./image/achv_image/turtlewin_banner.png"
FIRST_PLAY = "./image/achv_image/firstplay_banner.png"
CARD_COLLECTOR = "./image/achv_image/cardcollector_banner.png"
SKILL_MASTER = "./image/achv_image/skillmaster_banner.png"
ACHV_LIST = [SINGLE_WIN, AMERICA_WIN, MACAU_WIN, SINGAPORE_WIN, KOREA_WIN,
             SPEED_MASTER, NO_SKILL_WIN, TURTLE_WIN, FIRST_PLAY, CARD_COLLECTOR, SKILL_MASTER]

# 게임 중 업적 알림
SINGLE_WIN_ALARM = "./image/achv_image/singlewin_alarm.png"
AMERICA_WIN_ALARM = "./image/achv_image/americawin_alarm.png"
MACAU_WIN_ALARM = "./image/achv_image/macauwin_alarm.png"
SINGAPORE_WIN_ALARM = "./image/achv_image/singaporewin_alarm.png"
KOREA_WIN_ALARM = "./image/achv_image/koreawin_alarm.png"
SPEED_MASTER_ALARM = "./image/achv_image/speedmaster_alarm.png"
NO_SKILL_WIN_ALARM = "./image/achv_image/noskillwin_alarm.png"
TURTLE_WIN_ALARM = "./image/achv_image/turtlewin_alarm.png"
FIRST_PLAY_ALARM = "./image/achv_image/firstplay_alarm.png"
CARD_COLLECTOR_ALARM = "./image/achv_image/cardcollector_alarm.png"
SKILL_MASTER_ALARM = "./image/achv_image/skillmaster_alarm.png"
ACHV_ALARM_LIST = [SINGLE_WIN_ALARM, AMERICA_WIN_ALARM, MACAU_WIN_ALARM, SINGAPORE_WIN_ALARM, KOREA_WIN_ALARM,
                   SPEED_MASTER_ALARM, NO_SKILL_WIN_ALARM, TURTLE_WIN_ALARM, FIRST_PLAY_ALARM, CARD_COLLECTOR_ALARM, SKILL_MASTER_ALARM]

ACHV_COMPLETED = "./image/achv_image/achv_completed.png"

# 기술카드 사용 시 표시 이미지
PASS = "./image/playing_image/pass.png"
REVERSE = "./image/playing_image/reverse.png"
PLUS_TWO = "./image/playing_image/plus_two.png"
PLUS_FOUR = "./image/playing_image/plus_four.png"
CHANGE = "./image/playing_image/change.png"


# 카드
CARD_TYPE = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'wild'}
CARD_SKILL = {11: '_pass', 12: '_reverse', 13: '_plus_two',
              14: '_basic', 15: '_plus_four', 16: '_change'}

TIME = 10

ERROR_MSG = "./image/multi_image/error_message.png"
IP_FALSE_MSG = "./image/multi_image/ip_false.png"


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
