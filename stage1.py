import pygame
from pathlib import Path

import pygame.locals
from utilities import resizeObject

import random
 

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 736

white = (255,255,255)
brown = (111, 78, 55)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Time")

font_path = Path("assets") / "font" / "PressStart2P.ttf"
large_font = pygame.font.Font(font_path, 32)
small_font = pygame.font.Font(font_path, 18)

#define game variables
running = True

#img paths
chara_board_path = Path("assets") / "ui_elements" / "box.png"
chara_frame_path = Path("assets") / "ui_elements" / "frame.png"
distance_tracker_path = Path("assets") / "ui_elements" / "distance tracker.png"
inventory_path = Path("assets") / "ui_elements" / "inventory.png"






chara_board = pygame.image.load(chara_board_path)
chara_board = resizeObject(chara_board,6)

chara_frame = pygame.image.load(chara_frame_path)
chara_frame = resizeObject(chara_frame,3)

distance_tracker = pygame.image.load(distance_tracker_path)
distance_tracker = resizeObject(distance_tracker, 5.5)

inventory_img = pygame.image.load(inventory_path)
inventory_img = resizeObject(inventory_img, 2)




class HealthBar():
  def __init__(self):
    self.max_health = 12
    self.current_health = 12
    self.x = 290
    self.y = 60
    self.images = []
    for i in range(1,4):
      path = Path("assets") / "ui_elements" / f"heart{i}.png"
      img = pygame.image.load(path)
      img = resizeObject(img, 4)
      self.images.append(img)

  def draw(self):
    num_of_full_hearts = self.current_health // 2
    num_of_half_hearts = self.current_health % 2
    num_of_empty_hearts = (self.max_health / 2) - num_of_full_hearts - num_of_half_hearts

    for i in range(num_of_full_hearts):
      screen.blit(self.images[0], (self.x, self.y))
      self.x += 40;
    
    if num_of_half_hearts:
      screen.blit(self.images[1], (self.x, self.y))
      self.x += 40;

    for i in range(int(num_of_empty_hearts)):
      screen.blit(self.images[2], (self.x, self.y))
      self.x += 40;

    self.x = 290

  def takeDamage(self, amount):
    if self.current_health > 0:
      self.current_health -= amount

  def heal(self, amount):
    if self.current_health < self.max_health:
      self.current_health += amount

class StaminaBar():
  def __init__(self):
    self.max_stamina = 15
    self.current_stamina = 15
    self.x = 300
    self.y = 115
    self.images = []
    for i in range(1,3):
      path = Path("assets") / "ui_elements" / f"stamina{i}.png"
      img = pygame.image.load(path)
      img = resizeObject(img, 3)
      self.images.append(img)

  def draw(self):
    num_of_full_stamina = self.current_stamina
    num_of_empty_stamina = self.max_stamina - self.current_stamina

    for i in range(num_of_full_stamina):
      screen.blit(self.images[0], (self.x, self.y))
      self.x += 15;
    
    for i in range(num_of_empty_stamina):
      screen.blit(self.images[1], (self.x, self.y))
      self.x += 15;

    self.x = 300

  def decreaseStamina(self, amount):
    if self.current_stamina > 0:
      self.current_stamina -= amount

  def increaseStamina(self, amount):
    if self.current_stamina < self.max_stamina:
      self.current_stamina += amount       

class InventoryBar():
  def __init__(self):
    self.image = inventory_img

  def draw(self, coordinate_X, coordinate_y):
    screen.blit(self.image, (coordinate_X, coordinate_y))

class DistanceTracker():
  def __init__(self):
    signboard_path = Path("assets") / "stage_1_bg" / "2 Objects" / "3 Pointer" / "4.png"
    signboard = pygame.image.load(signboard_path)
    signboard = resizeObject(signboard, 3)
    self.distance_covered = -650
    self.milestone_tracker = 0
    self.signboard_img = signboard
    self.distance_tracker_img = distance_tracker
    self.signboard_x = SCREEN_WIDTH
    self.milestone_font = "start"
    self.signboard_active = False

  def updateDistance(self, speed):
    #only renders tracking distance when character reaches started point
    if self.distance_covered < 0:
      distance_font = large_font.render(str("0"), True, brown)
      
    else: 
      distance_font = large_font.render(str(int(self.distance_covered * 0.05)), True, brown)

    if self.distance_covered > 1300:
      self.milestone_font = str(self.milestone_tracker)  

    if self.distance_covered * 0.05 >= self.milestone_tracker and not self.signboard_active:
      self.signboard_active = True
      
    
    #display img
    milestone_font = small_font.render(self.milestone_font, True, brown)
    screen.blit(distance_tracker, (1078,-5))
    screen.blit(distance_font, (1120, 66))
    screen.blit(self.signboard_img, (self.signboard_x, 500))
    screen.blit(milestone_font, (self.signboard_x, 470))

    #update movement
    self.distance_covered += speed    
    self.signboard_x -= speed

    if self.signboard_x < -700:
      self.signboard_x = SCREEN_WIDTH
      self.signboard_active = False
      self.milestone_tracker += 100

class Scenes():
  def __init__(self):
    bg1_path = Path("assets") / "stage_1_bg" / "stage_1_bg.png"
    stage1_bg = pygame.image.load(bg1_path)
    self.scroll_speed = 3
    self.scrolled = 0
    self.stage1_bg_img = resizeObject(stage1_bg, 1.4)
    self.health = HealthBar()
    self.stamina = StaminaBar()
    self.distance = DistanceTracker()
    self.inventory = InventoryBar()
    self.fence = ObstacleManager(self.scroll_speed)


  def emptyBg(self, speed):
    self.scroll_speed = speed
    for i in range(0,3):
      screen.blit(self.stage1_bg_img, (i * self.stage1_bg_img.get_width() - 70 + self.scrolled, -60))

    self.scrolled -= self.scroll_speed

    if abs(self.scrolled) > self.stage1_bg_img.get_width():
      self.scrolled = 0;
  
  def scene1(self, speed):
    self.scroll_speed = speed
    #display UI
    screen.blit(chara_board, (30, 30))
    screen.blit(chara_frame, (55, 45))
    self.health.draw()
    self.stamina.draw()
    self.fence.update(self.scroll_speed)
    self.distance.updateDistance(speed)   #track distance
    self.inventory.draw(308, 575)
  
    #get key pressed
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_UP]:
      self.health.heal(1)
    if key_pressed[pygame.K_DOWN]:
      self.health.takeDamage(1)
    if key_pressed[pygame.K_LEFT]:
      self.stamina.decreaseStamina(1)
    if key_pressed[pygame.K_RIGHT]:
      self.stamina.increaseStamina(1)

class Fence(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    fence_path = Path("assets") / "stage_1_bg" / "2 Objects" / "2 Fence" / "8.png"
    fence_img = pygame.image.load(fence_path)
    fence_img = resizeObject(fence_img, 3)
    self.image = fence_img 
    self.fence_x = x
    self.fence_y = y
    self.rect = fence_img.get_rect(topleft = (x,y))
    self.hit = False

  def update(self, speed):
    self.fence_x -= speed
    self.rect.x = self.fence_x

  def check_collision(self, fin_rect):
        return self.rect.colliderect(fin_rect)
  

class ObstacleManager:
  def __init__(self, scroll_speed):
    self.fence_group = pygame.sprite.Group()
    self.last_fence_time = 0
    base = 1000
    self.min_time = int(3000/scroll_speed)
    self.max_time = int(3500/scroll_speed)
    self.spawn_interval = random.randint(self.min_time, self.max_time)
    self.y_positions = [265,365,465]

  def spawn_fence(self):
    y = random.choice(self.y_positions)
    x = 1300
    fence = Fence(x,y)
    self.fence_group.add(fence)


  def update(self, scroll_speed):
    current_time = pygame.time.get_ticks()
    
    if current_time - self.last_fence_time > self.spawn_interval:
      self.spawn_fence()
      self.last_fence_time = current_time
      self.spawn_interval = random.randint(self.min_time, self.max_time)

    for fence in self.fence_group:
      fence.update(scroll_speed)
      if fence.rect.right < -10:
        fence.kill()

    self.fence_group.draw(screen)

scene = Scenes()

class Fence():
  def __init__(self):
    self.x = 1300
    
    


#define character status      
health = healthBar()
stamina = staminaBar()
distance = distanceTracker()

#start
while running:

  clock.tick(FPS)

  scene.emptyBg(7)
  scene.scene1(7)
  
  
  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False


  pygame.display.update()

pygame.quit()


