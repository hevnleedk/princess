import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Princess Maker")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# 한글 폰트 설정 (시스템에 설치된 폰트 경로를 지정해야 합니다)
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows용 맑은 고딕 폰트
font = pygame.font.Font(font_path, 36)

# 캐릭터 클래스
class Character:
    def __init__(self, name):
        self.name = name
        self.age_year = 1
        self.haknun = 1
        self.age_month = 3
        self.health = 100
        self.intelligence = 100
        self.charm = 100
        self.message = ""

    def update_stats(self, health_change, intelligence_change, charm_change):
        self.health += health_change
        self.intelligence += intelligence_change
        self.charm += charm_change

    def downgrade_stats(self, health_change, intelligence_change, charm_change):
        self.health -= health_change
        self.intelligence -= intelligence_change
        self.charm -= charm_change

        # 랜덤 값에 따라 메시지 설정
        effect = max(health_change, intelligence_change, charm_change)
        if effect > 7:
            self.message = "효과가 굉장했다!"
        elif effect > 3:
            self.message = "그럭저럭 이해했다!"
        else:
            self.message = "오늘은 컨디션이 안좋네~"

    def update_age(self):
        self.age_month += 1
        if self.age_month > 6:
            self.age_month = 1
            self.haknun += 1
        if self.haknun > 2:
            self.haknun = 1
            self.age_year += 1

    def is_ending(self):
        return self.age_year == 3 and self.age_month == 6

    def are_ending(self):
        return self.health < 0 or self.intelligence < 0 or self.charm < 0

    def get_ending(self):
        if self.health > 130 and self.intelligence > 130 and self.charm > 130:
            return "회계사가 되었다!"
        elif self.intelligence > 120 and self.intelligence > self.charm and self.intelligence > self.health:
            return "대학원생이 되었다!"
        elif self.charm > 120 and self.charm > self.intelligence and self.charm > self.health:
            return "학교마스코트가 되었다!"
        elif self.health > 120 and self.health > self.charm and self.health > self.intelligence:
            return "부사관이 되었다!"
        else:
            return "다시 세무고를 입학하게 되었다."

    def get_anding(self):
        if self.health < 0:
            return "감기에 걸렸다!"
        elif self.intelligence < 0:
            return "퇴학당했다!"
        elif self.charm < 0:
            return "모쏠이 되었다!"

# 캐릭터 생성
princess = Character("Princess")

# 버튼 클래스
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, gray, self.rect)
        text_surface = font.render(self.text, True, black)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

# 버튼 생성
buttons = [
    Button("학업", 50, 400, 200, 50, "study"),
    Button("휴식", 300, 400, 200, 50, "rest"),
    Button("운동", 550, 400, 200, 50, "exercise")
]

# 메인 루프
running = True
ending = False
anding = False

while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not (ending or anding):
            for button in buttons:
                if button.is_clicked(event):
                    if button.action == "study":
                        princess.update_stats(0, random.randint(1, 30), 0)
                        princess.downgrade_stats(random.randint(1, 10), 0, 0)
                    elif button.action == "rest":
                        princess.update_stats(random.randint(1, 30), 0, 0)
                        princess.downgrade_stats(0, 0, random.randint(1, 10))
                    elif button.action == "exercise":
                        princess.update_stats(0, 0, random.randint(1, 30))
                        princess.downgrade_stats(0, random.randint(1, 10), 0)
                    princess.update_age()

                    if princess.are_ending():
                        anding = True

                    if princess.is_ending():
                        ending = True

    # 엔딩 화면
    if anding:
        screen.fill(white)
        ending_text = font.render(princess.get_anding(), True, black)
        screen.blit(ending_text, (screen_width // 2 - ending_text.get_width() // 2, screen_height // 2 - ending_text.get_height() // 2))
        pygame.display.flip()
    elif ending:
        screen.fill(white)
        ending_text = font.render(princess.get_ending(), True, black)
        screen.blit(ending_text, (screen_width // 2 - ending_text.get_width() // 2, screen_height // 2 - ending_text.get_height() // 2))
        pygame.display.flip()
    else:
        # 캐릭터 정보 표시
        name_text = font.render(f"이름: {princess.name}", True, black)
        screen.blit(name_text, (50, 50))

        age_text = font.render(f"나이: {princess.age_year}학년  {princess.haknun}학기", True, black)
        screen.blit(age_text, (50, 100))

        health_text = font.render(f"체력: {princess.health}", True, black)
        screen.blit(health_text, (50, 150))

        intelligence_text = font.render(f"지능: {princess.intelligence}", True, black)
        screen.blit(intelligence_text, (50, 200))

        charm_text = font.render(f"매력: {princess.charm}", True, black)
        screen.blit(charm_text, (50, 250))

        message_text = font.render(princess.message, True, black)
        screen.blit(message_text, (50, 300))

        # 버튼 표시
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

# 잠시 대기 후 종료
pygame.time.wait(5000)
pygame.quit()
sys.exit()

# 아이디어
# 1.게임 시작전 또는 게임이 끝나고 엔딩 화면이 나온 후 시작화면 출력(게임시작 버튼 추가)
# 2.버튼 & 화면 디자인 개선