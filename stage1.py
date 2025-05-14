import pygame
from pathlib import Path

import pygame.locals
from utilities import resizeObject

import random
from utilities import getImage

import pygame
from characterMovementAll import CharacterAnimation

import pygame.mixer
from PIL import Image

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


    
class Score():
  def __init__(self):
    self.name = None
    self.time = None


class LeaderBoard():
  def __init__(self):
    self.scores = []
    self.accepting_username = False
    self.done_accepting_username = False
    self.username = ""

    path = Path("assets") / "ui_elements" / "leaderboard.png"
    img = pygame.image.load(path)
    self.img = resizeObject(img, 5)

    path = Path("assets") / "ui_elements" / "box.png"
    img = pygame.image.load(path)
    self.input_img = resizeObject(img, 7)

    self.load_file()
    self.sort()

  def load_file(self):
    try:
      with open(Path("leaderboard.txt"), "r") as file:
        for line in file:
          score = Score()
          placeholder = line.split(",")
          score.name = placeholder[0]
          score.time = placeholder[1].strip()
          self.scores.append(score)
    except FileNotFoundError:
      print("File not found")
  
  def sort(self):
    n = len(self.scores)
    for i in range(n):
      for j in range(0, n- i - 1):
        if float(self.scores[j].time) > float(self.scores[j+1].time):
          self.scores[j], self.scores[j + 1] = self.scores[j + 1], self.scores[j]
            
  
  def get_username(self):
    if not self.done_accepting_username:
      get_username_font =  large_font.render("Username", True, (211, 211, 211))
      currently_typing = large_font.render(self.username, True, brown)
      screen.blit(self.input_img, (335,280))
      self.accepting_username = True

      if (len(self.username) == 0):
        screen.blit(get_username_font, (405, 350))

      else:
        screen.blit(currently_typing, (405, 350))




  def get_input(self, event):
    if self.accepting_username == False:
      return
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_BACKSPACE:
        self.username = self.username[:-1]

      elif event.key == pygame.K_RETURN:
        print(self.username)
        self.accepting_username = False
        self.done_accepting_username = True
      
      elif event.unicode.isalnum():
        self.username += event.unicode
     
  def save_score(self, time):
    with open("leaderboard.txt", "a") as file:
      file.write(f"\n{self.username},{time}")

  def show_leaderboard(self):
    font = large_font.render("Leaderboard", True, brown)
    screen.blit(self.img, (380, 58))
    screen.blit(font, (474,110))

    for score in range(len(self.scores)):
      place = str(score + 1) + "."
      name = self.scores[score].name
      time = str(self.scores[score].time)

      place_display = small_font.render(place, True, brown)
      name_display = small_font.render(name, True, brown)
      time_display = small_font.render(time, True, brown)

      screen.blit(place_display, (430, 185 + 40 * score))
      screen.blit(name_display, (500, 185 + 40 * score))
      screen.blit(time_display, (775, 185 + 40 * score))
      

    

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

    sound_path = Path("assets") / "audio" / "take damage.mp3"
    sound_path2 = Path("assets") / "audio" / "heal.mp3"
    self.take_damage_sound_effect = pygame.mixer.Sound(sound_path)
    self.take_damage_sound_effect.set_volume(1)
    self.heal_sound_effect = pygame.mixer.Sound(sound_path2)

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
    self.take_damage_sound_effect.play()

  def heal(self, amount):
    if self.current_health < self.max_health:
      self.current_health += amount
    self.heal_sound_effect.play()

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
    self.hover_sound_effect = pygame.mixer.Sound(Path("assets") / "audio" / "hover.wav" )
    self.clicked_sound_effect = pygame.mixer.Sound(Path("assets") / "audio" / "click2.mp3")
    self.pickup_sound_effect = self.clicked_sound_effect
    self.slots = []
    self.items = [None, None, None, None, None, None, None, None]
    self.currently_hovering_slot = False
    potionImages = Potions(0,0)
    
    for slot in range(7):
      slot_rect = pygame.Rect(322 + (slot * 96), 590, 79, 79)
      self.slots.append(slot_rect)

    self.potion_images = {i: potionImages.animation_list[i][0] for i in range(5)}


  def draw(self, coordinate_X, coordinate_y):
    screen.blit(self.image, (coordinate_X, coordinate_y))
    for slot_index in range(7):
      if self.items[slot_index] != None:
        screen.blit(self.potion_images[self.items[slot_index]], (self.slots[slot_index].x + 15, self.slots[slot_index].y +15))



  def handle_hover(self):
    mouse_pos = pygame.mouse.get_pos()
    hovering_any_slot = False
    currently_hovering_slot = None
    
    for slot_index, slot_rect in enumerate(self.slots):
        if slot_rect.collidepoint(mouse_pos):
            hovering_any_slot = True
            currently_hovering_slot = slot_index
            break
    
    # Play sound only when we hover over a NEW slot
    if hovering_any_slot:
        if self.currently_hovering_slot != currently_hovering_slot:
            self.hover_sound_effect.play()
            #print(f"Now hovering over slot {currently_hovering_slot}")

    self.currently_hovering_slot = currently_hovering_slot if hovering_any_slot else None

  def handle_click(self, event):
     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      for slot_index, slot_rect in enumerate(self.slots):
        if slot_rect.collidepoint(pygame.mouse.get_pos()) and self.items[slot_index] != None:
            print("clicked")
            self.clicked_sound_effect.play()
            self.use_potion(slot_index)

  def add_potion(self, potion_type):
    for slot in range(len(self.slots)):
      if self.items[slot] == None:
        self.items[slot] = potion_type
        self.pickup_sound_effect.play()
        print(f"Added potion of type {potion_type} to slot {slot}")
        return True
      
    print("inventory full")
    return False
  
  def use_potion(self, item_index):
     self.items[item_index] = None
     print("used potion")
     return True
  
    
    
     

  
class Potions(pygame.sprite.Sprite):
  def __init__(self, y, type):
    super().__init__()
    paths = ["blue.png", "purple.png", "red.png", "yellow.png", "green.png"]
    self.spritesheets = []
    self.animation_list = []
    self.animation_index = 0
    self.potion_type = type
    self.last_update_time = pygame.time.get_ticks()
    self.x = 1300
    self.y = y
    self.rect = pygame.Rect(self.x, self.y, 16, 16)

    for potion in range(5):
      spritesheet = pygame.image.load(Path("assets") / "item" / paths[potion])
      self.spritesheets.append(spritesheet)

    self.extract_frames()

  def extract_frames(self):
    for potion in range(5):
      placeholder = []
      for row in range(3):
        cropped = pygame.Surface((48,16), pygame.SRCALPHA)
        cropped.blit(self.spritesheets[potion], (0, 0), pygame.Rect(0, row * 16, 48, 16))
        for frame in range(3):
            img = getImage(cropped, frame, 16, 16, 3)
            placeholder.append(img)
      self.animation_list.append(placeholder)

  def animation(self, speed):
    self.x -= speed 
    cooldown = 300

    current_time = pygame.time.get_ticks()
    if current_time - self.last_update_time > cooldown:
        self.animation_index += 1
        self.last_update_time = current_time
        if self.animation_index >= 8:
          self.animation_index = 0
     
    self.rect = pygame.Rect(self.x, self.y, 48, 48)
    pygame.draw.rect(screen, (255,0,0), self.rect, 3)
    
    screen.blit(self.animation_list[self.potion_type][self.animation_index], (self.x, self.y))
 
     

class PotionManager:
  def __init__(self, fence_group=None, mushroom_group=None, inventory=None):
    self.potion_group = pygame.sprite.Group()
    self.last_spawned_time = 0
    self.spawn_interval = 3000
    self.y_positions = [275,375,475]
    self.fence_group = fence_group
    self.mushroom_group = mushroom_group
    self.inventory = inventory

  def try_spawn(self):
      """Attempts to spawn a potion if it doesn't collide with obstacles"""
      # Check if it's time to spawn a new potion
      current_time = pygame.time.get_ticks()
      if current_time - self.last_spawned_time < self.spawn_interval:
          return  # Not time to spawn yet
          
      # Try to create a new potion
      new_potion = Potions(random.choice(self.y_positions), random.randint(0, 4))
      
      # Check for collisions
      if not (pygame.sprite.spritecollide(new_potion, self.fence_group, False) or 
              pygame.sprite.spritecollide(new_potion, self.mushroom_group, False) or 
              pygame.sprite.spritecollide(new_potion, self.potion_group, False)):
          # No collisions, add to group
          self.potion_group.add(new_potion)
          self.last_spawned_time = current_time
  def check_collisions(self):
      # Check collisions between potions and obstacles
      for fence in self.fence_group:
          if pygame.sprite.spritecollide(fence, self.potion_group, True):
              fence.kill()

      for mushroom in self.mushroom_group:
          if pygame.sprite.spritecollide(mushroom, self.potion_group, True):
              mushroom.kill()

  def update(self, scroll_speed):
    self.try_spawn()
    self.check_collisions()

    for potion in self.potion_group:
      potion.animation(scroll_speed)

    for potion in list(self.potion_group):
      if potion.x < -50: 
          potion.kill()

  def pick_up_potion(self, finn):
    for potion in self.potion_group:
      if pygame.sprite.spritecollide(potion, pygame.sprite.Group(finn), True):
        self.inventory.add_potion(potion.potion_type)
        potion.kill()

  



class DialogueBox():
  def __init__(self):
    dialogue_box_path = Path("assets") / "ui_elements" / "Sprite sheets" / "Dialouge UI" / "Premade dialog box  big.png"
    dialogue_box = pygame.image.load(dialogue_box_path)
    self.dialogue_img = resizeObject(dialogue_box, 3)
    self.text_y = 300
    self.script = []
    self.counter = 0
    self.active_text = 0
    self.done = False
    self.visible = True

    #sound effect
    sound_path = Path("assets") / "audio" / "Text Sound Effect.wav"
    self.sound_effect = pygame.mixer.Sound(sound_path)
    self.sound_effect.set_volume(0.7)
    self.last_char_count = 0

  def draw(self, script_dict):
    self.script = script_dict
    character = script_dict[self.active_text]["speaker"]
    line = script_dict[self.active_text]["line"]

    #set character potrait
    potrait_path = ""
    if character == "Finn":
      potrait_path = Path("assets") / "character" / "Finn Potrait.png"
    elif character == "Ice King":
      potrait_path = Path("assets") / "character" / "Ice King Potrait.png"
    elif character == "Princess Bubblegum":
      potrait_path = Path("assets") / "character" / "Princess Bubblegum Potrait.png"
    elif character == "Jake":
       potrait_path = Path("assets") / "character" / "Jake Potrait.png"

    img = Image.open(potrait_path)
    img.save(potrait_path, icc_profile=None)
    potrait_img = pygame.image.load(potrait_path)
    potrait_img = resizeObject(potrait_img, 0.6)
    
    #setting up fonts
    font_path = Path("assets") / "font" / "PressStart2P.ttf"
    name_font = pygame.font.Font(font_path, 26)
    text_font = pygame.font.Font(font_path, 18)

    #only runs when set to visible
    if self.visible:
      speed = 3 #type writer effect speed


      #render character name, dialogue box, character potrait
      character_name = name_font.render(character, True, brown)
      screen.blit(self.dialogue_img, (194, 540))
      screen.blit(character_name, (390,565))
      screen.blit(potrait_img, (203, 550))

      #preprocess text for warping
      words = line.split(" ")
      lines = []
      line = ""
      max_width = 700

      for word in words:
          test_line = line + word + " "
          test_surface = text_font.render(test_line, True, brown)
          if test_surface.get_width() > max_width:
              lines.append(line)
              line = word + " "
          else:
              line = test_line
      if line:
          lines.append(line)

      #updating counter
      if self.counter < speed * len(line):
          self.counter += 1
          if self.counter > self.last_char_count and self.counter % 6 == 0:
            self.sound_effect.play()
      elif self.counter >= speed * len(line):
          self.done = True

      text = text_font.render(line[0:self.counter // speed], True, brown)  
      screen.blit(text, (400, 627))


  def handle_input(self, event):
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and self.done:
          if self.active_text < len(self.script) - 1:
              self.active_text += 1
              self.counter = 0
              self.done = False
          else:
              self.visible = False 






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
    self.dialogue = DialogueBox()

    self.finnSR = Mouse()

    # Step 1: Create all manager objects without dependencies first
    self.fence = FenceManager(self.scroll_speed)
    self.mushroom = MushroomManager(None, None)  # Temporarily pass None
    self.potion = PotionManager(None, None, self.inventory)  # Temporarily pass None

    # Step 2: After all objects are created, set their group references
    self.mushroom.fence_group = self.fence.fence_group
    self.mushroom.potion_group = self.potion.potion_group
    self.potion.mushroom_group = self.mushroom.mushroom_group
    self.potion.fence_group = self.fence.fence_group
    
    # Wallace
    Blue = (0, 162, 232)
    unwanted_colors = [Blue]
    self.cutscene_state = 0
    self.cutscene_start_time = pygame.time.get_ticks()
    self.special_effect_visible = False
    self.gameplay_started = False

    finn_path = Path("assets") / "character" / "Finn_Running.png"
    pb_path = Path("assets") / "character" / "Princess_Bubblegum.png"
    ice_king_path = Path("assets") / "character" / "Ice_King.png"
    special_effect_path = Path("assets") / "character" / "Special_effect.png"

    self.finn = CharacterAnimation(finn_path, [10, 10, 8], [66, 75.3, 83.5], [88, 88, 88, 88], 60, unwanted_colors, [50, 300], scale=1)
    self.pb = CharacterAnimation(pb_path, [8, 8, 5], [52, 52, 63.8], [120, 120, 120], 60, unwanted_colors, [200, 300], scale=1)
    self.ice_king = CharacterAnimation(ice_king_path, [6, 7, 5], [106, 143, 131.25], [150, 150, 150], 60, unwanted_colors, [1500, 250], scale=1)
    self.special_effect = CharacterAnimation(special_effect_path, [4, 5], [50, 100], [100, 100], 60, unwanted_colors, [100,250], scale=2)


  def emptyBg(self, speed):
    self.scroll_speed = speed
    for i in range(0,3):
      screen.blit(self.stage1_bg_img, (i * self.stage1_bg_img.get_width() - 70 + self.scrolled, -60))

    self.scrolled -= self.scroll_speed

    if abs(self.scrolled) > self.stage1_bg_img.get_width():
      self.scrolled = 0
  
  def level1(self, speed, spawn_mushroom, num_of_mushroom = 1):
    self.scroll_speed = speed
    #display UI
    screen.blit(chara_board, (30, 30))
    screen.blit(chara_frame, (55, 45))

    #finn potrait
    finn_potrait_path = Path("assets") / "character" / "Finn Potrait.PNG"
    finn_img = Image.open(finn_potrait_path)
    finn_img.save(finn_potrait_path, icc_profile = None)
    finn_img = pygame.image.load(finn_potrait_path)
    finn_img = resizeObject(finn_img, 0.4)
    screen.blit(finn_img, (61, 60))
    self.health.draw()
    self.stamina.draw()
    self.fence.update(self.scroll_speed)  #spawn fences
    self.distance.updateDistance(speed)   #track distance
    self.inventory.draw(308, 575)
    if spawn_mushroom:
      self.mushroom.update(num_of_mushroom, speed) #spawn mushroom
    self.potion.update(speed)
    self.inventory.handle_hover()
    self.finnSR.draw()    #DELETE LTR
    self.potion.pick_up_potion(self.finnSR)
    self.mushroom.killed(self.finnSR)

    # script = [{"speaker" : "Ice King", "line" : "Helllo"},
    #           {"speaker" : "Ice King", "line" : "My name is Ice King"},
    #           {"speaker" : "Princess Bubblegum", "line" : "Helloooo"},
    #           {"speaker" : "Princess Bubblegum", "line" : "My name is pb!"},
    #           {"speaker" : "Finn", "line" : "Helloooo"},
    #           {"speaker" : "Finn", "line" : "My name is Finn!"},
    #           {"speaker" : "Jake", "line" : "Helloooo"},
    #           {"speaker" : "Jake", "line" : "My name is Jake!"}]
    # self.dialogue.draw(script)
  
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

  def cutscene1(self):
    self.now = pygame.time.get_ticks()
    if self.cutscene_state == 0:
        if self.finn.action != 0:
            self.finn.set_action(0)
        self.finn.move(dx=1)

        if self.pb.action != 0:
            self.pb.set_action(0)
        self.pb.move(dx=1)

        if self.finn.pos[0] >= 300:
            self.cutscene_state = 1
            self.cutscene_start_time = self.now

    elif self.cutscene_state == 1:
        if self.pb.action != 1:
            self.pb.set_action(1)
        if self.now - self.cutscene_start_time > 5000:
            self.cutscene_state = 2
            self.cutscene_start_time = self.now
            self.ice_king.pos = [-100, -150]

    elif self.cutscene_state == 2:
        if self.ice_king.action != 0:
            self.ice_king.set_action(0)
        self.ice_king.move(dx=4, dy=2)
        if self.ice_king.pos[0] >= self.pb.pos[0] - 50:
            self.cutscene_state = 3
            self.cutscene_start_time = self.now

    elif self.cutscene_state == 3:
        if self.ice_king.action != 1:
            self.ice_king.set_action(1)
        if self.pb.action != 2:
            self.pb.set_action(2)
        if not self.special_effect_visible:
            self.special_effect.set_action(0)
            self.special_effect_visible = True
            self.special_effect.pos = [self.pb.pos[0], self.pb.pos[1] - 10]
        if self.now - self.cutscene_start_time > 1000:
            self.pb.visible = False
            self.special_effect_visible = False
            self.cutscene_state = 4
            self.cutscene_start_time = self.now

    elif self.cutscene_state == 4:
        if self.ice_king.action != 2:
            self.ice_king.set_action(2)
        self.ice_king.move(dx=5, dy=-1)
        if self.ice_king.pos[0] > SCREEN_WIDTH:
            self.cutscene_state = 5
            self.cutscene_start_time = self.now

    elif self.cutscene_state == 5:
        if self.finn.action != 2:
            self.finn.set_action(2)
        if self.now - self.cutscene_start_time > 2000:
            self.cutscene_state = 6
            self.cutscene_start_time = self.now

    elif self.cutscene_state == 6:
        self.gameplay_started = True
        self.cutscene_state = 7

class Fence(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    fence_path = Path("assets") / "stage_1_bg" / "2 Objects" / "2 Fence" / "8.png"
    fence_img = pygame.image.load(fence_path)
    fence_img = resizeObject(fence_img, 3)
    self.image = fence_img 
    self.fence_x = x
    self.fence_y = y
    self.rect = fence_img.get_rect(topleft = (self.fence_x,self.fence_y))
    self.hit = False

  def update(self, speed):
    self.fence_x -= speed
    self.rect.x = self.fence_x
    pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)  #test

  def check_collision(self, fin_rect):
        return self.rect.colliderect(fin_rect)
  
  
class Mushroom(pygame.sprite.Sprite):
  def __init__(self, y):
    super().__init__()
    self.run_spritesheet = Path("assets") / "enemy" / "mushroom" / "Mushroom-Run.png"
    self.attack_spritesheet = Path("assets") / "enemy" / "mushroom" / "Mushroom-Attack.png"
    self.die_spritesheet = Path("assets") / "enemy" / "mushroom" / "Mushroom-Die.png"
    spritesheets = [pygame.image.load(self.run_spritesheet).convert_alpha(),
                     pygame.image.load(self.attack_spritesheet).convert_alpha(), 
                     pygame.image.load(self.die_spritesheet).convert_alpha()]
    
    self.img = getImage(spritesheets[0], 0, 80, 64, 1.7)
    self.animation_frames = [7,9,4]
    self.animation_list = []
    self.animation_index = [0,0,0]
    self.last_update_time = 0
    self.x = 1300
    self.y = y
    self.rect = pygame.Rect((self.x + 30), (self.y + 45), 70 , 64)

    for animation in range(len(spritesheets)):
      placeholder = []
      for frame in range(self.animation_frames[animation]):
        img = getImage(spritesheets[animation], frame, 80, 64, 1.7)
        placeholder.append(img)
        #screen.blit(img, (200,200))
      self.animation_list.append(placeholder)



  def animation(self, speed, action):
      self.x -= speed
      cooldown = 100  # Reduced cooldown for faster animation
      
      current_time = pygame.time.get_ticks()
      if current_time - self.last_update_time > cooldown:
          self.animation_index[action] += 1
          self.last_update_time = current_time
          if self.animation_index[action] >= self.animation_frames[action]:
              self.animation_index[action] = 0
      
      self.rect = pygame.Rect((self.x + 30), (self.y + 45), 70 , 64)

      screen.blit(self.animation_list[action][self.animation_index[action]], (self.x, self.y))
      pygame.draw.rect(screen, (255, 0, 0), self.rect, 3) #test



class Mouse(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    ori = pygame.image.load(Path("assets") / "ui_elements" / "mouse.png")
    self.img = resizeObject(ori, 2)
    self.x = 0
    self.y = 0
    self.rect = pygame.Rect(self.x + 20, self.y, 100, 107)

  def get_input(self, event):
    mouse_pos = pygame.mouse.get_pos()

    self.x = mouse_pos[0]
    self.y = mouse_pos[1]
    self.rect = pygame.Rect(self.x + 20 , self.y, 50, 50)
    
  def draw(self):
    pygame.draw.rect(screen, (255,0,0), self.rect, 3)
    screen.blit(self.img, (self.x, self.y))
   
    
class MushroomManager:
  def __init__(self, fence_group=None, potion_group=None):
    self.mushroom_group = pygame.sprite.Group()
    self.last_spawned_time = 0
    self.spawn_interval = 3000
    self.y_positions = [215,315,415]
    self.max_mushroom = 2
    self.fence_group = fence_group
    self.potion_group = potion_group

  def spawn(self):
    new_mushroom = Mushroom(random.choice(self.y_positions))
    return new_mushroom

  def update(self, max_mushroom, scroll_speed):
    self.max_mushroom = max_mushroom
    if len(self.mushroom_group) < self.max_mushroom:
      mushroom = self.spawn()
      if not (
          pygame.sprite.spritecollide(mushroom, self.fence_group, False) or
          pygame.sprite.spritecollide(mushroom, self.mushroom_group, False) or
          pygame.sprite.spritecollide(mushroom, self.potion_group, False)
      ):
        self.mushroom_group.add(mushroom)

    for fence in self.fence_group:
       if (pygame.sprite.spritecollide(fence, self.mushroom_group, False)):
          fence.kill()

    for mushroom in self.mushroom_group:
      mushroom.animation(scroll_speed, 0)
      if mushroom.x < -100:
         mushroom.kill()
  
  def killed(self, finn):
    for mushroom in self.mushroom_group:
      if pygame.sprite.spritecollide(mushroom, pygame.sprite.Group(finn), True):
        print("killed")
        mushroom.animation(0, 1)
        mushroom.kill()
     
      



class FenceManager:
  def __init__(self, scroll_speed):
    self.fence_group = pygame.sprite.Group()
    self.last_fence_time = 0
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
      if fence.fence_x < -50:
        fence.kill()

    self.fence_group.draw(screen) 

scene = Scenes()

#start
while running:
  pygame.mouse.set_visible(0)
  clock.tick(FPS)


  scene.emptyBg(10)
  scene.level1(10, True, 2)
# event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    
    scene.dialogue.handle_input(event)
    scene.inventory.handle_click(event)
    scene.finnSR.get_input(event)
    

  pygame.display.update()


pygame.quit()


