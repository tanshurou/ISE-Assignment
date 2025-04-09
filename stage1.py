import pygame
from pathlib import Path
from utilities import resizeObject
 

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
scrolled = 0
scroll_speed = 3

#img paths
bg1_path = Path("assets") / "stage_1_bg" / "stage_1_bg.png"
signboard_path = Path("assets") / "stage_1_bg" / "2 Objects" / "3 Pointer" / "4.png"
chara_board_path = Path("assets") / "ui_elements" / "box.png"
chara_frame_path = Path("assets") / "ui_elements" / "frame.png"
distance_tracker_path = Path("assets") / "ui_elements" / "distance tracker.png"

#Load Images
stage1_bg = pygame.image.load(bg1_path)
stage1_bg = resizeObject(stage1_bg, 1.4)

signboard = pygame.image.load(signboard_path)
signboard = resizeObject(signboard, 3)

chara_board = pygame.image.load(chara_board_path)
chara_board = resizeObject(chara_board,6)

chara_frame = pygame.image.load(chara_frame_path)
chara_frame = resizeObject(chara_frame,3)

distance_tracker = pygame.image.load(distance_tracker_path)
distance_tracker = resizeObject(distance_tracker, 5.5)

class healthBar():
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

class staminaBar():
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

class distanceTracker():
  def __init__(self):
    self.distance_covered = -650
    self.milestone_tracker = 0
    self.signboard_img = signboard
    self.distance_tracker_img = distance_tracker
    self.signboard_x = SCREEN_WIDTH
    self.milestone_font = "start"
    self.signboard_active = False

  def updateDistance(self):
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
    screen.blit(signboard, (self.signboard_x, 500))
    screen.blit(milestone_font, (self.signboard_x, 470))

    #update movement
    self.distance_covered += scroll_speed     
    self.signboard_x -= scroll_speed

    if self.signboard_x < -700:
      self.signboard_x = SCREEN_WIDTH
      self.signboard_active = False
      self.milestone_tracker += 100


    


#define character status      
health = healthBar()
stamina = staminaBar()
distance = distanceTracker()

#start
while running:

  clock.tick(FPS)

  #display bg
  for i in range(0, 3):
    screen.blit(stage1_bg, (i * stage1_bg.get_width() - 70 + scrolled, -60))

  scrolled -= scroll_speed

  if abs(scrolled) > stage1_bg.get_width():
    scrolled = 0;
  
  #display UI
  screen.blit(chara_board, (30, 30))
  screen.blit(chara_frame, (55, 45))
  health.draw()
  stamina.draw()

  #track distance
  distance.updateDistance()
  
  



  #get key pressed
  key_pressed = pygame.key.get_pressed()

  if key_pressed[pygame.K_UP]:
    health.heal(1)
  if key_pressed[pygame.K_DOWN]:
    health.takeDamage(1)
  if key_pressed[pygame.K_LEFT]:
    stamina.decreaseStamina(1)
  if key_pressed[pygame.K_RIGHT]:
    stamina.increaseStamina(1)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False


  pygame.display.update()

pygame.quit()


