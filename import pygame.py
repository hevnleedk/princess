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
blue = (173, 216, 230)

# 한글 폰트 설정 (시스템에 설치된 폰트 경로를 지정해야 합니다//)
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows용 맑은 고딕 폰트
font = pygame.font.Font(font_path, 36)

# 캐릭터 클래스
class Character:
    def __init__(self, name, image_paths):
        self.name = name
        self.age_year = 17
        self.age_month = 3
        self.health = 100
        self.intelligence = 50
        self.charm = 50
        self.message = ""
        self.images = [pygame.image.load(image_path) for image_path in image_paths]
        self.images = [pygame.transform.scale(image, (200, 300)) for image in self.images]

    def update_stats(self, health_change, intelligence_change, charm_change):
        self.health += health_change
        self.intelligence += intelligence_change
        self.charm += charm_change

        # 랜덤 값에 따라 메시지 설정
        effect = max(health_change, intelligence_change, charm_change)
        if effect > 7:
            self.message = f"효과가 굉장했다! (+{max(health_change, intelligence_change, charm_change)})"
        elif effect > 3:
            self.message = f"그럭저럭 이해했다! (+{max(health_change, intelligence_change, charm_change)})"
        else:
            self.message = f"오늘은 컨디션이 안좋네~ (+{max(health_change, intelligence_change, charm_change)})"

    def update_age(self):
        self.age_month += 1
        if self.age_month > 12:
            self.age_month = 1
            self.age_year += 1

    def is_ending(self):
        return self.age_year == 19 and self.age_month == 12

    def get_image(self):
        if self.age_year == 17:
            return self.images[0]
        elif self.age_year == 18:
            return self.images[1]
        elif self.age_year == 19:
            return self.images[2]
        return self.images[0]

    def get_ending(self):
        if self.health > 80 and self.intelligence > 80 and self.charm > 80:
            return "여왕이 되었다!"
        elif self.intelligence > 70:
            return "학자가 되었다!"
        elif self.charm > 70:
            return "배우가 되었다!"
        elif self.health > 70:
            return "운동선수가 되었다!"
        else:
            return "평범한 사람이 되었다."

# 캐릭터 생성 (캐릭터 이미지 경로를 지정하세요)
image_paths = ["character_image_1.png", "character_image_2.png", "character_image_3.png"]
princess = Character("Princess", image_paths)

# 버튼 클래스
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, blue, self.rect, border_radius=10)
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
while running:
    screen.fill(white)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not ending:
            for button in buttons:
                if button.is_clicked(event):
                    if button.action == "study":
                        change = random.randint(1, 10)
                        princess.update_stats(0, change, 0)
                    elif button.action == "rest":
                        change = random.randint(1, 10)
                        princess.update_stats(change, 0, 0)
                    elif button.action == "exercise":
                        change = random.randint(1, 10)
                        princess.update_stats(0, 0, change)
                    princess.update_age()
                    
                    if princess.is_ending():
                        ending = True
    
    if ending:
        # 엔딩 화면
        screen.fill(white)
        ending_text = font.render(princess.get_ending(), True, black)
        screen.blit(ending_text, (screen_width // 2 - ending_text.get_width() // 2, screen_height // 2 - ending_text.get_height() // 2))
        pygame.display.flip()
    else:
        # 캐릭터 정보 표시
        screen.blit(princess.get_image(), (550, 50))

        name_text = font.render(f"이름: {princess.name}", True, black)
        screen.blit(name_text, (50, 50))
        
        age_text = font.render(f"나이: {princess.age_year}년 {princess.age_month}월", True, black)
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