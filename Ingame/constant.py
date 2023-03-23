"""상수 즉 자주 쓰는 것들을 모두 모아서 적어놓는 공간이야 예를 들어 글꼴, 색깔, 카드 번호 이런 것들도 다 적는 공간이야."""

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 80, 0)

# 카드 리스트 이미지 넣고 인덱스로 접근 (안은 튜플 앞, 뒤)
CARD_IMAGE_LIST = []

for color in ["red", "green", "blue", "yellow"]:
    for i in range(0, 10):
        CARD_IMAGE_LIST.append(f"image/card_img/{color}{i}.png")
    CARD_IMAGE_LIST.append(f"image/card_img/{color}change.png")
    CARD_IMAGE_LIST.append(f"image/card_img/{color}pass.png")
    CARD_IMAGE_LIST.append(f"image/card_img/{color}plus2.png")

CARD_IMAGE_LIST.append("image/card_img/wild.png")
CARD_IMAGE_LIST.append("image/card_img/wilddrawfour.png")
CARD_IMAGE_LIST.append("image/card_img/back.png")

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# SCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT)            # 이건 많이 안 쓸 것 같아서 일단 보류


# 글꼴 정하기
MALGUNGOTHIC = "malgungothic"

# 카드 크기
CARD_HEIGHT = 585 / 5
CARD_WIDTH = 410 / 5
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

"""카드 변환하는거 코사인 함수로 스케일링한 뒤에 뒤 이미지 변환하는 것 구현하기"""
