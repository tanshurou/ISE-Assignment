import math
import pygame
from pathlib import Path

import pygame.locals
from utilities import resizeObject

import random
from utilities import getImage

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
      self.base_x = 290  # Base position (starting point)
      self.y = 60
      self.heart_spacing = 40  # Space between hearts
      self.images = []
      for i in range(1, 4):
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
      # Ensure health is within bounds
      self.current_health = max(0, min(self.current_health, self.max_health))
      
      # Calculate hearts
      num_of_full_hearts = self.current_health // 2
      num_of_half_hearts = self.current_health % 2
      num_of_empty_hearts = int(self.max_health // 2) - num_of_full_hearts - num_of_half_hearts
  
      
      # Reset x position at the start of drawing
      current_x = self.base_x
      
      # Draw full hearts
      for i in range(num_of_full_hearts):
          screen.blit(self.images[0], (current_x, self.y))
          current_x += self.heart_spacing
      
      # Draw half heart if needed
      if num_of_half_hearts > 0:
          screen.blit(self.images[1], (current_x, self.y))
          current_x += self.heart_spacing

      # Draw empty hearts
      for i in range(num_of_empty_hearts):
          screen.blit(self.images[2], (current_x, self.y))
          current_x += self.heart_spacing

  def takeDamage(self, amount):
      if self.current_health > 0:
          self.current_health = max(0, self.current_health - amount)
          self.take_damage_sound_effect.play()

  def heal(self, amount):
      if self.current_health < self.max_health:
          self.current_health = min(self.max_health, self.current_health + amount)
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
      self.hover_sound_effect = pygame.mixer.Sound(Path("assets") / "audio" / "hover.wav")
      self.clicked_sound_effect = pygame.mixer.Sound(Path("assets") / "audio" / "click2.mp3")
      self.pickup_sound_effect = self.clicked_sound_effect
      self.slots = []
      self.items = [None, None, None, None, None, None, None, None]
      self.currently_hovering_slot = False
      potionImages = Potions(0, 0)

      #use potion animation
      paths = ["use_blue_potion.png", "use_purple_potion.png", "use_red_potion.png", "use_yellow_potion.png", "use_green_potion.png"]
      
      self.spritesheets = []
      self.animation_list = []
      self.animation_index = 0
      self.last_update_time = pygame.time.get_ticks()
      self.effect_active = False
      self.current_effect_type = None  # Track which potion effect is active
      self.effect_slot_index = None    # Track which slot the effect is appearing on

      for effect in range(5):
        spritesheet = pygame.image.load(Path("assets") / "character" / "Effects" / paths[effect])
        placeholder = []
        for frame in range(9):
          img = getImage(spritesheet, frame, 64, 64, 2)
          placeholder.append(img)

        self.animation_list.append(placeholder)
          

      
      # Create inventory slots
      for slot in range(7):
          slot_rect = pygame.Rect(322 + (slot * 96), 590, 79, 79)
          self.slots.append(slot_rect)

      # Store all animation frames for each potion type
      self.potion_animations = potionImages.animation_list
      
      # Animation variables
      self.current_frame = 0
      self.animation_speed = 0.1  # Adjust for faster/slower animation
      self.last_update = pygame.time.get_ticks()
      self.frame_count = 8  # Total frames per potion (3 rows * 3 frames)

  def draw(self, coordinate_X, coordinate_y):
      screen.blit(self.image, (coordinate_X, coordinate_y))
      # Draw potions in slots with current animation frame
      for slot_index in range(7):
          if self.items[slot_index] is not None:
              potion_type = self.items[slot_index]
              # Get current animation frame for this potion type
              current_potion_frame = self.potion_animations[potion_type][self.current_frame]
              
              # Center the potion in the slot
              screen.blit(current_potion_frame, 
                          (self.slots[slot_index].x + (self.slots[slot_index].width - current_potion_frame.get_width()) // 2,
                          self.slots[slot_index].y + (self.slots[slot_index].height - current_potion_frame.get_height()) // 2))
      
      # If an effect is active, draw the effect animation
      if self.effect_active and self.current_effect_type is not None:
          self.use_potion_animation()

  def update_animation(self):
      # Update animation frame based on time
      current_time = pygame.time.get_ticks()
      if current_time - self.last_update > 1000 * self.animation_speed:
          self.last_update = current_time
          self.current_frame = (self.current_frame + 1) % self.frame_count
  
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
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          for slot_index, slot_rect in enumerate(self.slots):
              if slot_rect.collidepoint(pygame.mouse.get_pos()) and self.items[slot_index] is not None:
                  self.clicked_sound_effect.play()
                  self.use_potion(slot_index)

  def add_potion(self, potion_type):
      for slot in range(len(self.slots)):
          if self.items[slot] is None:
              self.items[slot] = potion_type
              self.pickup_sound_effect.play()
              return True
          
      print("inventory full")
      return False
  
  def use_potion(self, item_index):
      # Store the potion type before removing it
      potion_type = self.items[item_index]
      self.items[item_index] = None
      
      # Set the current effect type and activate effect
      self.current_effect_type = potion_type
      self.effect_active = True
      self.animation_index = 0  # Reset animation frame counter
      self.last_update_time = pygame.time.get_ticks()  # Reset timer
      self.effect_slot_index = item_index  # Store which slot the effect should appear in
      
      return True
  
  def use_potion_animation(self):
      # Only proceed if an effect is active
      if not self.effect_active or self.effect_slot_index is None:
          return
          
      cooldown = 100  # Animation speed in milliseconds
      current_time = pygame.time.get_ticks()
      
      # Update animation frame when cooldown has elapsed
      if current_time - self.last_update_time > cooldown:
          self.animation_index += 1
          self.last_update_time = current_time
          
      # End animation after all frames have been shown
      if self.animation_index >= 9:
          self.effect_active = False
          self.current_effect_type = None
          self.effect_slot_index = None
          return
      
      # Get the correct animation frame based on potion type and current index
      if 0 <= self.current_effect_type < 5:  # Make sure it's a valid potion type
          current_frame = self.animation_list[self.current_effect_type][self.animation_index]
          
          # Use the slot position for the effect
          slot_rect = self.slots[self.effect_slot_index]
          
          # Draw the effect centered on the slot
          x = slot_rect.x + (slot_rect.width - current_frame.get_width()) // 2
          y = slot_rect.y + (slot_rect.height - current_frame.get_height()) // 2
          
          # Render the effect
          screen.blit(current_frame, (x, y))
        
     
  
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
      if potion.rect.colliderect(finn.hitbox):
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
    self.distance = DistanceTracker()
    self.inventory = InventoryBar()
    self.dialogue = DialogueBox()
    self.effects = EffectManager()

    self.mouse = Mouse()
    self.finn = Finn(x=100, y=310, health_bar=health_bar, stamina_bar=stamina_bar)

    # Step 1: Create all manager objects without dependencies first
    self.fence = FenceManager(self.scroll_speed)
    self.mushroom = MushroomManager(self.effects, None, None)  # Temporarily pass None
    self.potion = PotionManager(None, None, self.inventory)  # Temporarily pass None

    # Step 2: After all objects are created, set their group references
    self.mushroom.fence_group = self.fence.fence_group
    self.mushroom.potion_group = self.potion.potion_group
    self.potion.mushroom_group = self.mushroom.mushroom_group
    self.potion.fence_group = self.fence.fence_group

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
    finn_potrait_path = Path("assets") / "character" / "Finn Potrait.png"
    finn_img = pygame.image.load(finn_potrait_path)
    finn_img = resizeObject(finn_img, 0.4)
    screen.blit(finn_img, (61, 60))
    self.finn.health_bar.draw()
    self.finn.stamina_bar.draw()
    self.fence.update(self.scroll_speed, self.finn)  #spawn fences
    self.distance.updateDistance(speed)   #track distance
    self.inventory.update_animation()
    self.inventory.draw(308, 575)
    if spawn_mushroom:
      self.mushroom.update(num_of_mushroom, speed) #spawn mushroom
    self.potion.update(speed)
    self.inventory.handle_hover()
    self.mouse.draw()    #DELETE LTR
    self.potion.pick_up_potion(self.finn)
    self.finn.update
    self.finn.draw(screen)
    self.mushroom.hit(self.finn.bullet_group, self.finn.bullet_buff)
    self.mushroom.collide(self.finn)
    self.effects.apply_effects()

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



class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fence_path = Path("assets") / "stage_1_bg" / "2 Objects" / "2 Fence" / "8.png"
        fence_img = pygame.image.load(fence_path)
        fence_img = resizeObject(fence_img, 3)
        self.image = fence_img 
        self.original_image = self.image.copy()
        self.fence_x = x
        self.fence_y = y
        self.rect = fence_img.get_rect(topleft=(self.fence_x, self.fence_y))
        
        # Blinking parameters
        self.hit = False
        self.blink_start_time = 0
        self.blink_duration = 1000  # Total duration for all blinks (1 second)
        self.blink_frequency = 100  # Time for one on/off cycle (100ms = 10 blinks per second)
        self.blink_intensity = 255  # Full white (255, 255, 255)

    def update(self, speed):
        self.fence_x -= speed
        self.rect.x = self.fence_x

        current_time = pygame.time.get_ticks()

        if self.hit and current_time - self.blink_start_time < self.blink_duration:
            # Calculate if we're in an "on" phase of the blink cycle
            # This creates a square wave pattern that alternates between TRUE and FALSE
            blink_phase = ((current_time - self.blink_start_time) // (self.blink_frequency // 2)) % 2
            
            if blink_phase == 0:
                # "ON" phase - Show white version
                self.image = self.original_image.copy()
                # Create a white surface with high opacity
                white_surface = pygame.Surface(self.image.get_size()).convert_alpha()
                white_surface.fill((255, 255, 255, 220))  # Almost solid white (220/255 opacity)
                self.image.blit(white_surface, (0, 0))
            else:
                # "OFF" phase - Show original
                self.image = self.original_image.copy()
        else:
            # Blinking complete or not blinking
            self.image = self.original_image.copy()
            self.hit = False  # Reset hit flag after blink is done
        
    def blink(self):
        self.hit = True
        self.blink_start_time = pygame.time.get_ticks()
     
        
  
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, y, effect_manager):
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
        self.animation_index = [0,0,0,0,0]
        self.explode_animation = []
        self.poison_animation = []
        self.last_update_time = 0
        self.explode_animation_last_update_time = 0
        self.collide_animation_update_time = 0
        self.x = 1300
        self.y = y
        self.rect = pygame.Rect((self.x + 30), (self.y + 45), 70 , 64)
        self.dead = False
        self.collide = False
        self.health = 2
        self.special_effect = effect_manager
        
        # Blink effect variables
        self.is_blinking = False
        self.blink_duration = 500  # Total blinking time in milliseconds
        self.blink_start_time = 0
        self.blink_interval = 100  # Time between blink toggling in milliseconds
        self.blink_visible = True  # Flag to toggle visibility during blinking
        self.last_blink_toggle = 0
        
        for animation in range(len(spritesheets)):
            placeholder = []
            for frame in range(self.animation_frames[animation]):
                img = getImage(spritesheets[animation], frame, 80, 64, 1.7)
                placeholder.append(img)
                #screen.blit(img, (200,200))
            self.animation_list.append(placeholder)
        
        explode_path = Path("assets") / "character" / "Effects" / "Mushroom die.png"
        poison_path = Path("assets") / "character" / "Effects" / "hit_by_mushroom.png"
        explode_img = pygame.image.load(explode_path)
        poison_img = pygame.image.load(poison_path)
        
        for frame in range(14):
            img = getImage(explode_img, frame, 64, 64, 2.5)
            img2 = getImage(poison_img, frame, 64, 64, 2.5)
            self.explode_animation.append(img)
            self.poison_animation.append(img2)

    def take_damage(self, bullet_buff):
        if bullet_buff == True:
            self.health -= 2
        else:
            self.health -= 1
        print(self.health)
        
        # Start blinking effect when taking damage
        self.start_blinking()
        
        if self.health <= 0:
            self.dead = True
    
    def start_blinking(self):
        self.is_blinking = True
        self.blink_start_time = pygame.time.get_ticks()
        self.blink_visible = True
        self.last_blink_toggle = self.blink_start_time
    
    def update_blinking(self):
        if not self.is_blinking:
            return True  # If not blinking, always visible
        
        current_time = pygame.time.get_ticks()
        
        # Check if blinking duration is over
        if current_time - self.blink_start_time > self.blink_duration:
            self.is_blinking = False
            return True  # Blinking finished, sprite should be visible
        
        # Toggle visibility based on blink interval
        if current_time - self.last_blink_toggle > self.blink_interval:
            self.blink_visible = not self.blink_visible
            self.last_blink_toggle = current_time
        
        return self.blink_visible  # Return current visibility state

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
    
        if self.dead == False and self.collide == False:
            # Only draw if the sprite should be visible during blinking
            if self.update_blinking():
                screen.blit(self.animation_list[action][self.animation_index[action]], (self.x, self.y))
                pygame.draw.rect(screen, (255, 0, 0), self.rect, 3) #test

    def killed(self):
        cooldown = 100
        current_time = pygame.time.get_ticks()
        self.dead = True
        
        if current_time - self.explode_animation_last_update_time > cooldown:
            self.animation_index[3] += 1
            self.explode_animation_last_update_time = current_time
        if self.animation_index[3] == 13:
            self.kill()
        screen.blit(self.explode_animation[self.animation_index[3]], (self.x-20, self.y-30))

    def poison(self):
        cooldown = 100
        current_time = pygame.time.get_ticks()
        self.collide = True
        
        if current_time - self.collide_animation_update_time > cooldown and self.dead == False:
            self.animation_index[4] += 1
            self.collide_animation_update_time = current_time
            self.special_effect.trigger_effect(0)
        if self.animation_index[4] == 13:
            self.kill()
            print("poisoned")
        screen.blit(self.poison_animation[self.animation_index[4]], (self.x-20, self.y-30))
     

     

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
  def __init__(self, effect_manager, fence_group=None, potion_group=None):
    self.mushroom_group = pygame.sprite.Group()
    self.last_spawned_time = 0
    self.spawn_interval = 3000
    self.y_positions = [215,315,415]
    self.max_mushroom = 2
    self.fence_group = fence_group
    self.potion_group = potion_group
    self.effect_manager = effect_manager
    self.last_collide = 0

  def spawn(self):
    new_mushroom = Mushroom(random.choice(self.y_positions), self.effect_manager)
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
      if mushroom.dead == True:
         mushroom.killed()
      if mushroom.collide == True:
         mushroom.poison()
      if mushroom.x < -100:
         mushroom.kill()

  def hit(self, bullet, bullet_buff):
    for mushroom in self.mushroom_group:
      if pygame.sprite.spritecollide(mushroom, pygame.sprite.Group(bullet), True):
        mushroom.take_damage(bullet_buff)

  def collide(self, finn):
    current_time = pygame.time.get_ticks()
    for mushroom in self.mushroom_group:
      # Only check collision if the mushroom is alive (not dead or in death animation)
      if not mushroom.dead and not mushroom.collide and mushroom.rect.colliderect(finn.hitbox):
        mushroom.collide = True
        if current_time - self.last_collide > 100:
           self.last_collide = current_time
           finn.health_bar.takeDamage(3)

      



class FenceManager:
  def __init__(self, scroll_speed):
    self.fence_group = pygame.sprite.Group()
    self.last_fence_time = 0
    self.min_time = int(3000/scroll_speed)
    self.max_time = int(3500/scroll_speed)
    self.spawn_interval = random.randint(self.min_time, self.max_time)
    self.y_positions = [265,365,465]
    self.last_collision = 0

  def spawn_fence(self):
    y = random.choice(self.y_positions)
    x = 1300
    fence = Fence(x,y)
    self.fence_group.add(fence)


  def update(self, scroll_speed, finn):
    current_time = pygame.time.get_ticks()
    
    if current_time - self.last_fence_time > self.spawn_interval:
      self.spawn_fence()
      self.last_fence_time = current_time
      self.spawn_interval = random.randint(self.min_time, self.max_time)
    
    for fence in self.fence_group:
      fence.update(scroll_speed)
      if fence.fence_x < -50:
        fence.kill()
      if fence.rect.colliderect(finn.hitbox) and current_time - self.last_collision > 500:
         self.last_collision = current_time
         finn.health_bar.takeDamage(2)
         fence.blink()

    self.fence_group.draw(screen) 

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_x, frame_width, frame_height, scale, colours):
        img = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        img.blit(self.sheet, (0, 0), (frame_x * frame_width, 0, frame_width, frame_height))
        img = pygame.transform.scale(img, (int(frame_width * scale), int(frame_height * scale)))

        for x in range(img.get_width()):
            for y in range(img.get_height()):
                if img.get_at((x, y))[:3] in colours:
                    img.set_at((x, y), (0, 0, 0, 0))
        return img


class Finn(pygame.sprite.Sprite):
  def __init__(self, x, y, health_bar, stamina_bar, scale=1.2):
    super().__init__()
    # Finn Setup
    self.scale = scale
    self.finn_path = Path("assets") / "character" / "Finn_Running.png"
    self.unwanted_colors = [(0, 162, 232)]
    self.sprite_sheet_image = pygame.image.load(self.finn_path).convert_alpha()
    self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
    self.animation_list = []
    self.frame_width = [66, 75.3, 83.5]
    self.frame_height = [88, 88, 88]
    self.cooldown = 100
    self.frame = 0
    self.finn_action = 0
    self.last_update = pygame.time.get_ticks() - self.cooldown - 1
    self.load_frames([10, 10, 8])
    self.image = self.animation_list[self.finn_action][self.frame]
    self.pos = [x, y]
    self.rect = self.image.get_rect(topleft=(x, y))  # Only for image blit

    # Customizable collision box
    self.hitbox_offset_x = 20
    self.hitbox_offset_y = 55
    self.hitbox_width = 50
    self.hitbox_height = 20
    self.update_hitbox()

    # Finn Jumping Mechanic
    self.is_jumping = False
    self.jump_velocity = -10 * self.scale
    self.gravity = 0.5 * self.scale
    self.finn_y_velocity = 0

    # Audio for Finn
    self.jump_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Jump Sound Effect Finn.mp3")
    self.shoot_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Shoot Sound Effect Finn.mp3")

    # Bullet Setup
    self.bullet_group = pygame.sprite.Group()
    self.BULLET_SPEED = int(10 * self.scale) 
    self.bullet_path = Path("assets") / "character" / "Bullet_animation.png"

    # Lane Setup
    self.lanes = [220, 310, 410]
    self.current_lane = 1
    self.lane_target_y = self.lanes[self.current_lane]

    # Health bar and stamina bar setup
    self.speed = 5 * self.scale
    self.health_bar = HealthBar()
    self.stamina_bar = StaminaBar()
    self.last_shoot_time = 0
    self.shoot_cooldown = 500
    self.set_finn_action(0)

    # Buffs
    self.health_buff = False
    self.stamina_buff = False
    self.speed_buff = False
    self.invicible_buff = False
    self.bullet_buff = False

  def load_frames(self, animation_steps):
    step_counter = 0
    for i, steps in enumerate(animation_steps):
        temp_list = []
        for _ in range(steps):
            img = self.sprite_sheet.get_image(step_counter, self.frame_width[i],  self.frame_height[i], self.scale, self.unwanted_colors)
            temp_list.append(img)
            step_counter += 1
        self.animation_list.append(temp_list)

  def update_hitbox(self):
    self.hitbox = pygame.Rect(self.pos[0] + self.hitbox_offset_x, self.pos[1] + self.hitbox_offset_y, self.hitbox_width, self.hitbox_height)

  def update(self):
    now = pygame.time.get_ticks()
    if now - self.last_update >= self.cooldown:
        self.frame = (self.frame + 1) % len(self.animation_list[self.finn_action])
        self.last_update = now
        if self.frame == 0 and self.finn_action != 0:
            self.set_finn_action(0)

    self.image = self.animation_list[self.finn_action][self.frame]
    self.rect = self.image.get_rect(topleft=(self.pos[0], self.pos[1]))
    self.update_hitbox()

    # Jumping Mechanics
    if not self.is_jumping:
        if self.pos[1] < self.lane_target_y:
            self.pos[1] += self.speed
            if self.pos[1] > self.lane_target_y:
                self.pos[1] = self.lane_target_y
        elif self.pos[1] > self.lane_target_y:
            self.pos[1] -= self.speed
            if self.pos[1] < self.lane_target_y:
                self.pos[1] = self.lane_target_y
    
    if self.is_jumping:
        self.finn_y_velocity += self.gravity
        self.pos[1] += self.finn_y_velocity

    if self.is_jumping and self.pos[1] >= self.lane_target_y - 2:
        self.pos[1] = self.lane_target_y
        self.is_jumping = False
        self.finn_y_velocity = 0
        self.set_finn_action(0)

    for bullet in list(self.bullet_group):
        bullet.update()
        if bullet.rect.x > 2000:
            self.bullet_group.remove(bullet)

  def draw(self, screen):
    screen.blit(self.image, self.rect.topleft)
    pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    for bullet in self.bullet_group:
        bullet.draw(screen)

  def handle_input(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w and self.current_lane > 0:
            self.current_lane -= 1
            self.lane_target_y = self.lanes[self.current_lane]
        elif event.key == pygame.K_s and self.current_lane < len(self.lanes) - 1:
            self.current_lane += 1
            self.lane_target_y = self.lanes[self.current_lane]
        elif event.key == pygame.K_SPACE and not self.is_jumping:
            self.is_jumping = True
            self.finn_y_velocity = self.jump_velocity
            self.set_finn_action(1)
            self.jump_sound.play()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shoot_cooldown:
            self.set_finn_action(2)
            self.shoot_bullet()
            self.shoot_sound.play()
            self.last_shoot_time = current_time

  def set_finn_action(self, action_index):
    if action_index < len(self.animation_list):
        self.finn_action = action_index
        self.frame = 0
        self.last_update = pygame.time.get_ticks() - self.cooldown - 1

  def shoot_bullet(self):
    bullet_x = self.pos[0] + int(40 * self.scale)
    bullet_y = self.pos[1] + int(25 * self.scale)
    new_bullet = Bullet(bullet_x, bullet_y, str(self.bullet_path), self.BULLET_SPEED, self.unwanted_colors, scale=self.scale)
    self.bullet_group.add(new_bullet)

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y, image_path, speed, unwanted_colors, scale=1, collision_scale=0.5):
      super().__init__()

      # Bullet Setup
      self.scale = scale
      self.collision_scale = collision_scale
      self.sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
      self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
      self.animation_list = []
      self.frame_width = 50
      self.frame_height = 50
      self.unwanted_colors = unwanted_colors
      self.cooldown = 100
      self.frame = 0
      self.action = 0
      self.last_update = pygame.time.get_ticks() - self.cooldown - 1
      self.load_frames([4])
      self.image = self.animation_list[self.action][self.frame]
      self.rect = self.image.get_rect(topleft=(x, y))
      self.speed = speed
      self.update_collision_rect()


  def update_collision_rect(self):
      width = int(self.rect.width * self.collision_scale)
      height = int(self.rect.height * self.collision_scale)
      self.collision_rect = pygame.Rect(0, 0, width, height)
      self.collision_rect.topleft = self.rect.center

  def load_frames(self, animation_steps):
      step_counter = 0
      for steps in animation_steps:
          temp_list = []
          for _ in range(steps):
              img = self.sprite_sheet.get_image(
                  frame_x=step_counter, frame_width=self.frame_width,
                  frame_height=self.frame_height, scale=self.scale, colours=self.unwanted_colors
              )
              temp_list.append(img)
              step_counter += 1
          self.animation_list.append(temp_list)

  def update(self):
      self.rect.x += self.speed
      self.update_collision_rect()
      now = pygame.time.get_ticks()
      if now - self.last_update >= self.cooldown:
          self.frame = (self.frame + 1) % len(self.animation_list[self.action])
          self.image = self.animation_list[self.action][self.frame]
          self.last_update = now

  def draw(self, screen):
      screen.blit(self.image, self.rect.topleft)
      pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)


class EffectManager():
  def __init__(self):
      self.start_time = [0]
      self.effect_duration = [1000]
      self.last_updated_time = [0]
      self.effect_applied = [0]

  def trigger_effect(self, effect):
      # Set the effect as active
      self.effect_applied[0] = 1
      # IMPORTANT: Update the last updated time when triggering
      self.last_updated_time[0] = pygame.time.get_ticks()

  def poisoned(self):
      time_ms = pygame.time.get_ticks()
      # Get a temporary copy of the current screen
      temp = screen.copy()

      # Calculate rotation and scale using sine wave
      angle = math.sin(time_ms / 200) * 3  # degrees
      scale = 1 + math.sin(time_ms / 300) * 0.02

      # Scale surface
      new_size = (int(screen.get_width() * scale), int(screen.get_height() * scale))
      temp = pygame.transform.smoothscale(temp, new_size)

      # Rotate surface
      temp = pygame.transform.rotate(temp, angle)

      # Center it back on screen
      rect = temp.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

      # Clear and blit
      screen.fill((0, 0, 0))
      screen.blit(temp, rect.topleft)

      # Optional: add green overlay
      overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
      overlay.fill((0, 255, 0, 80))
      screen.blit(overlay, (0, 0))

  def apply_effects(self):
    if self.effect_applied[0] == 1:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_updated_time[0]
        
        if elapsed_time < self.effect_duration[0]:
            self.poisoned()
        else:
            # Fixed: Use = for assignment, not == for comparison
            print("Effect duration expired, resetting")
            self.effect_applied[0] = 0
            # Fixed: Use = for assignment, not == for comparison
            # Also, make sure to index the list properly
            self.last_updated_time[0] = 0
    
      
      
  


health_bar = HealthBar()
stamina_bar = StaminaBar()

scene = Scenes()
running = True
clock = pygame.time.Clock()
running_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Game Running Sound Effect.mp3")
running_sound.play()

#start
while running:
  pygame.mouse.set_visible(False)
  clock.tick(FPS)
  scene.emptyBg(10)
  scene.level1(10, True, 2)
  scene.finn.update()

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

      scene.mouse.get_input(event)
      scene.dialogue.handle_input(event)
      scene.inventory.handle_click(event)
      scene.finn.handle_input(event)
      
  pygame.display.update()

pygame.quit()