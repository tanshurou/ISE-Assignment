import math
import pygame
from pathlib import Path
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

#  Main Menu and Cutscene Variable
game_state = "menu"  # Other states: "username_input", "cutscene", "playing", "leaderboard"
menu_bg = pygame.image.load("assets/stage_1_bg/mainmenu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

tutorial_image = pygame.image.load("assets/stage_1_bg/Tutorial.png").convert_alpha()
tutorial_image = pygame.transform.scale(tutorial_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

cutscene1_img = pygame.image.load("assets/stage_1_bg/cutscene1.png").convert()
cutscene2_img = pygame.image.load("assets/stage_1_bg/cutscene2.png").convert()
cutscene3_img = pygame.image.load("assets/stage_1_bg/cutscene3.png").convert()

cutscene1_img = pygame.transform.scale(cutscene1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cutscene2_img = pygame.transform.scale(cutscene2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cutscene3_img = pygame.transform.scale(cutscene3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Snowflake(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.x = random.randint(0, SCREEN_WIDTH)
    self.y = random.randint(-50, -10)
    self.speed_y = random.uniform(1, 3)
    self.size = random.randint(2, 4)
    self.color = (255, 255, 255)

  def update(self):
    self.y += self.speed_y
    if self.y > SCREEN_HEIGHT:
        self.y = random.randint(-50, -10)
        self.x = random.randint(0, SCREEN_WIDTH)

  def draw(self, surface):
    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class Button:
  def __init__(self, x, y, image=None, scale=1, text="", font=None, text_color=(111, 78, 55)):
      if image:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
      else:
        self.image = None
        self.rect = pygame.Rect(x, y, 200, 40)

      self.clicked = False
      self.text = text
      self.font = font
      self.text_color = text_color
      if self.text and self.font:
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(midleft=(self.rect.x + 20, self.rect.centery))
      else:
        self.text_surf = None

  def draw(self, surface):
    action = False
    mouse_pos = pygame.mouse.get_pos()

    if self.rect.collidepoint(mouse_pos):
      if pygame.mouse.get_pressed()[0] and not self.clicked:
        self.clicked = True
        action = True
    if not pygame.mouse.get_pressed()[0]:
      self.clicked = False

    if self.image:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    if self.text_surf:
      outline_color = (100, 80, 50)
      for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        outline = self.font.render(self.text, True, outline_color)
        surface.blit(outline, self.text_rect.move(dx, dy))
      surface.blit(self.text_surf, self.text_rect)
    return action

start_button = Button(900, 300, image=None, text="PLAY", font=large_font, text_color=(255, 220, 140))
leaderboard_button = Button(900, 400, image=None, text="LEADERBOARD", font=large_font, text_color=(255, 220, 140))
exit_button = Button(900, 500, image=None, text="EXIT", font=large_font, text_color=(255, 220, 140))
back_button = Button(50, 650, image=None, text="BACK", font=large_font, text_color=(255, 220, 140))
next_button = Button(1100, 650, image=None, text="NEXT", font=large_font, text_color=(255, 220, 140))

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
      if scene.finn.invincible_buff:
          return
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
      return False
  
  def use_potion(self, item_index):
      potion_type = self.items[item_index]
      self.items[item_index] = None

      self.current_effect_type = potion_type
      self.effect_active = True
      self.animation_index = 0
      self.last_update_time = pygame.time.get_ticks()
      self.effect_slot_index = item_index

      # === Trigger EffectManager Logic ===
      if potion_type == 0:  # Blue potion
          scene.effects.trigger_effect("speed_boost")
      elif potion_type == 1:  # Purple potion
          scene.effects.trigger_effect("bullet_buff")
      elif potion_type == 2:  # Red potion
          scene.effects.trigger_effect("heal")
      elif potion_type == 3:  # Yellow potion
          scene.effects.trigger_effect("defense_boost")
      elif potion_type == 4:  # Green potion
          scene.effects.trigger_effect("stamina")
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
    full_line = script_dict[self.active_text]["line"]

    if character == "Ice King" and not scene.snow_active:
      scene.snow_active = True
      scene.shake_duration = 1500
      scene.shake_start_time = pygame.time.get_ticks()
      scene.shake_intensity = 10

    # Set potrait image based on speaker
    potrait_path = ""
    if character == "Finn":
        potrait_path = Path("assets") / "character" / "Finn Potrait.png"
    elif character == "Ice King":
        potrait_path = Path("assets") / "character" / "Ice King Potrait.png"
    elif character == "Princess Bubblegum":
        potrait_path = Path("assets") / "character" / "Princess Bubblegum Potrait.png"
    elif character == "Jake":
        potrait_path = Path("assets") / "character" / "Jake Potrait.png"
    else:
        potrait_path = Path("assets") / "character" / "Unknown Potrait.png"

    potrait_img = pygame.image.load(potrait_path)
    potrait_img = resizeObject(potrait_img, 0.6)

    font_path = Path("assets") / "font" / "PressStart2P.ttf"
    name_font = pygame.font.Font(font_path, 26)
    text_font = pygame.font.Font(font_path, 18)

    if self.visible:
        speed = 3  # characters per update
        character_name = name_font.render(character, True, brown)
        screen.blit(self.dialogue_img, (194, 540))
        screen.blit(character_name, (390, 565))
        screen.blit(potrait_img, (203, 550))

        # Reveal characters gradually
        visible_text = full_line[0:self.counter // speed]

        # === Proper word wrapping ===
        max_width = 700
        words = visible_text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_surface = text_font.render(test_line, True, brown)
            if test_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        # Draw lines
        for i, l in enumerate(lines):
            text = text_font.render(l, True, brown)
            screen.blit(text, (400, 627 + i * 24))  # Adjust vertical spacing if needed

        # === Update counter & sound ===
        if self.counter < speed * len(full_line):
            self.counter += 1
            if self.counter > self.last_char_count and self.counter % 6 == 0:
                self.sound_effect.play()
        elif self.counter >= speed * len(full_line):
            self.done = True
        
        if scene.snow_active:
          for flake in scene.snowflakes:
              flake.update()
              flake.draw(screen)

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
    self.speed_milestone = 300
    self.max_base_speed = 10
    self.stage1_bg_img = resizeObject(stage1_bg, 1.4)
    self.distance = DistanceTracker()
    self.inventory = InventoryBar()
    self.dialogue = DialogueBox()
    self.effects = EffectManager()
    self.leaderboard = LeaderBoard()
    self.mouse = Mouse()
    self.health_bar = HealthBar()
    self.stamina_bar = StaminaBar()
    self.finn = Finn(x=100, y=310, health_bar=self.health_bar, stamina_bar=self.stamina_bar)
    self.effects.set_finn(self.finn)

    self.clock = pygame.time.Clock()
    self.game_finished = False
    self.game_over = False
    self.paused = False

    self.timer_start = pygame.time.get_ticks()
    self.elapsed_time = 0
    self.timer_active = True
    self.pause_start_time = 0
    self.total_paused_time = 0
    self.game_started = False
    self.warmup_duration = 2000
    self.warmup_start = None
    self.in_warmup = True
    self.timer_font = pygame.font.Font(Path("assets") / "font" / "PressStart2P.ttf", 24)

    self.menu_music = pygame.mixer.Sound(Path("assets") / "audio" / "Intro.mp3")
    self.menu_music.set_volume(0.5)

    self.dialogue.visible = True
    self.dialogue.done = False
    self.dialogue.active_text = 0
    self.dialogue.counter = 0

    self.shake_intensity = 0
    self.shake_duration = 0
    self.shake_start_time = 0
    self.snowflakes = [Snowflake() for _ in range(60)]
    self.snow_active = False
    
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
      offset_x, offset_y = self.get_shake_offset()
      for i in range(0, 3):
          screen.blit(self.stage1_bg_img, (i * self.stage1_bg_img.get_width() - 70 + self.scrolled + offset_x, -60 + offset_y))
      self.scrolled -= self.scroll_speed

      if abs(self.scrolled) > self.stage1_bg_img.get_width():
          self.scrolled = 0

  def level1(self, speed, spawn_mushroom, num_of_mushroom = 1):
    self.scroll_speed = speed
    self.emptyBg(speed)
    #display UI
    screen.blit(chara_board, (30 + offset_x, 30 + offset_y))
    screen.blit(chara_frame, (55 + offset_x, 45 + offset_y)) 
    if self.distance.distance_covered * 0.05 >= 3000 and not self.game_finished:
      self.game_finished = True
      self.timer_active = True
      self.timer_start = pygame.time.get_ticks()
      self.timer_active = False
      self.running_sound.stop()
      if self.game_finished:
        self.leaderboard.get_username()
        self.leaderboard.load_file()
        self.leaderboard.sort()
        self.leaderboard.show_leaderboard()

    #finn potrait
    if not self.game_over and not self.game_finished:
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

      if self.finn.health_bar.current_health <= 0:
        self.game_over = True
        self.timer_active = False

      self.mushroom.hit(self.finn.bullet_group, self.finn.bullet_buff)
      self.mushroom.collide(self.finn)
      self.effects.apply_effects()
      self.fence.bullet_hit(self.finn.bullet_group, self.finn.bullet_buff)

      # Smoothly update Finn's base speed toward the max base speed
      target_base_speed = self.max_base_speed
      self.finn.base_speed += (target_base_speed - self.finn.base_speed) * 0.01
      if self.effects.effects["speed_boost"]["active"]:
          target_scroll_speed = self.finn.base_speed * 2
      elif self.finn.running and self.finn.stamina_bar.current_stamina > 0:
          target_scroll_speed = self.finn.base_speed * self.finn.run_multiplier
      else:
          target_scroll_speed = self.finn.base_speed
      self.scroll_speed += (target_scroll_speed - self.scroll_speed) * 0.1

    # Game Finished 
    if self.game_finished and not self.game_over:
      finish_text = self.timer_font.render("FINISH!", True, brown)
      screen.blit(finish_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
    
    # Player Died
    if self.game_over and not self.game_finished:
      font = pygame.font.Font(Path("assets") / "font" / "PressStart2P.ttf", 40)
      game_over_text = font.render("GAME OVER", True, (255, 0, 0))
      restart_text = font.render("Press R to Restart", True, (255, 255, 255))
      self.timer_active = False
      self.running_sound.stop()

      game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
      restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

      screen.blit(game_over_text, game_over_rect)
      screen.blit(restart_text, restart_rect)

    # === STOPWATCH DISPLAY ===
    if self.timer_active and self.game_started:
        self.elapsed_time = pygame.time.get_ticks() - self.timer_start - self.total_paused_time
    seconds = self.elapsed_time // 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    timer_text = self.timer_font.render(f"{minutes:02}:{remaining_seconds:02}", True, brown)
    screen.blit(timer_text, (1100, 130))

  def get_shake_offset(self):
    if self.shake_duration <= 0:
        return 0, 0
    elapsed = pygame.time.get_ticks() - self.shake_start_time
    if elapsed > self.shake_duration:
        self.shake_duration = 0
        return 0, 0
    return random.randint(-self.shake_intensity, self.shake_intensity), random.randint(-self.shake_intensity, self.shake_intensity)

  cutscene_script = [
      {"speaker": "Finn", "line": "Man, what should I get PB for her birthday..."},
      {"speaker": "Jake", "line": "Hmm, get her something totally mathematical!"},
      {"speaker": "Finn", "line": "Yeah... but it has to be *special*, you know?"},
      {"speaker": "Jake", "line": "You could make something — like a sword made of candy!"},
      {"speaker": "Finn", "line": "Haha, nah. Maybe just something from the heart."},
      {"speaker": "Finn", "line": "Wait... you're not invited?"},
      {"speaker": "Jake", "line": "Nah, it’s cool. I told PB I had dog stuff to do."},
      {"speaker": "Finn", "line": "Alright... I’ll bring her the best gift ever."},
      {"speaker": "Finn", "line": "Happy Birthday, PB!"},
      {"speaker": "Princess Bubblegum", "line": "Finn! You came! And... is that a gift?"},
      {"speaker": "Finn", "line": "Yup! Just for you. Hope you like it."},
      {"speaker": "Princess Bubblegum", "line": "You're the sweetest, Finn. Thank you."},
      {"speaker": "Princess Bubblegum", "line": "It’s been a while since we hung out like this."},
      {"speaker": "Finn", "line": "Yeah. I’ve been doing hero stuff, training and stuff."},
      {"speaker": "Ice King", "line": "PB! You're coming with me!"},
      {"speaker": "Finn", "line": "ICE KING!? Not on her birthday!"},
      {"speaker": "Ice King", "line": "Love doesn’t wait, Finn!"},
      {"speaker": "Finn", "line": "You’re gonna regret this... big time!"}
  ]

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
        if self.update_blinking():
            screen.blit(self.animation_list[action][self.animation_index[action]], (self.x, self.y))

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
          self.special_effect.trigger_poison()
      if self.animation_index[4] == 13:
          self.kill()
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
      if not mushroom.dead and mushroom.rect.colliderect(finn.hitbox):
        if finn.invincible_buff:
            mushroom.dead = True  # kill mushroom on contact
        elif not mushroom.collide:
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
    self.fence_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Fence Broke Sound Effect.mp3")

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

  def bullet_hit(self, bullets, bullet_buff):
    for fence in self.fence_group:
      for bullet in bullets:
        if fence.rect.colliderect(bullet.rect) and bullet_buff:
          self.fence_sound.play()
          fence.kill()
          bullets.remove(bullet)
          break 

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
    self.invincible_buff = False
    self.bullet_buff = False

    # Low Health
    self.low_health_blink = False
    self.blink_start_time = 0
    self.blink_interval = 200
    self.blink_visible = True
    self.last_blink_toggle = 0

    # Stamina
    self.running = False
    self.base_speed = self.speed
    self.run_multiplier = 1.7
    self.stamina_deplete_rate = 0.2  # adjust as needed
    self.last_stamina_use_time = pygame.time.get_ticks()


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
    
    if self.running and self.stamina_bar.current_stamina > 0:
      self.speed = self.base_speed * self.run_multiplier
      now = pygame.time.get_ticks()
      if now - self.last_stamina_use_time > 300:
        self.stamina_bar.decreaseStamina(1)
        self.last_stamina_use_time = now
      if not scene.effects.effects["wind_screen"]["active"]:
        scene.effects.effects["wind_screen"]["active"] = True
        scene.effects.effects["wind_screen"]["start_time"] = pygame.time.get_ticks()
        scene.effects.effects["wind_screen"]["positions"] = []
    else:
        self.speed = self.base_speed

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

    # Start blinking if health < 4
    if self.health_bar.current_health < 4:
      if not self.low_health_blink:
          self.low_health_blink = True
          self.blink_start_time = pygame.time.get_ticks()
          self.last_blink_toggle = self.blink_start_time
    else:
      self.low_health_blink = False
      self.blink_visible = True

    # Toggle visibility if blinking
    if self.low_health_blink:
      now = pygame.time.get_ticks()
      if now - self.last_blink_toggle > self.blink_interval:
        self.blink_visible = not self.blink_visible
        self.last_blink_toggle = now

  def draw(self, screen):
    if self.blink_visible:
      screen.blit(self.image, self.rect.topleft)
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
      elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
        self.running = True

    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
          self.running = False

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
      bullet_sprite_path = (
      Path("assets") / "character" / "Effects" / "purple_bullet.png" 
      if self.bullet_buff else Path("assets") / "character" / "Bullet_animation.png")
      is_purple = self.bullet_buff
      frame_size = (50, 50) if not is_purple else (64, 64)
      new_bullet = Bullet(bullet_x, bullet_y, str(bullet_sprite_path), self.BULLET_SPEED, self.unwanted_colors, scale=self.scale, frame_size=frame_size)
      self.bullet_group.add(new_bullet)

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y, image_path, speed, unwanted_colors, scale=1, collision_scale=0.5, frame_size=(50,50)):
      super().__init__()

      # Bullet Setup
      self.scale = scale
      self.collision_scale = collision_scale
      self.sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
      self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
      self.animation_list = []
      self.frame_width, self.frame_height = frame_size
      self.frame_width = 50 if "Bullet_animation" in image_path else 64
      self.frame_height = 50 if "Bullet_animation" in image_path else 64
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
              img = self.sprite_sheet.get_image(frame_x=step_counter, frame_width=self.frame_width,
                  frame_height=self.frame_height, scale=self.scale, colours=self.unwanted_colors)
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

class EffectManager():
  def __init__(self):
    # ---- Buff Setup and Poison----
    wind_sheet = pygame.image.load(Path("assets") / "character" / "Effects" / "wind_screen.png").convert_alpha()
    wind_frames = [getImage(wind_sheet, i, 64, 64, 3) for i in range(9)]
    self.effects = {
      "poisoned": {
          "active": False,"start_time": 0,"duration": 1000,"cooldown": 0,
          "frames": [],"index": 0,"path": None,"scale": 0,"frame_count": 0,
          "frame_size": (0, 0),"action": self.no_action,"cleanup": self.no_cleanup},

      "bullet_buff": {
          "active": False, "start_time": 0,"duration": 5000,"cooldown": 150, "frames": [],"index": 0,
          "path": Path("assets") / "character" / "Effects" / "purple_potion.png", "scale": 4, "frame_count": 10,
          "frame_size": (64, 64), "action": self.enable_bullet_buff,
          "cleanup": self.disable_bullet_buff},

      "heal": {
          "active": False,"start_time": 0,"duration": 2250,"cooldown": 100,"frames": [],"index": 0,
          "path": Path("assets") / "character" / "Effects" / "red_potion.png","scale": 3,"frame_count": 10,
          "frame_size": (64, 64),"action": self.apply_heal,
          "cleanup": self.no_cleanup},
      
      "stamina": {"active": False, "start_time": 0, "duration": 2000, "cooldown": 120, "frames": [], "index": 0,
          "path": Path("assets") / "character" / "Effects" / "green_potion.png", "scale": 2, "frame_count": 10,
          "frame_size": (64, 64), "action": self.apply_stamina, "cleanup": self.no_cleanup},

      "speed_boost": {
          "active": False, "start_time": 0, "duration": 3000, "cooldown": 100, "frames": [], "index": 0,
          "path": Path("assets") / "character" / "Effects" / "blue_potion.png", "scale": 3, "frame_count": 10, 
          "frame_size": (64, 64), "action": self.enable_blue_buff, "cleanup": self.disable_blue_buff},

      "defense_boost": {"active": False, "start_time": 0, "duration": 3000, "cooldown": 100, "frames": [], "index": 0,
          "path": Path("assets") / "character" / "Effects" / "yellow_potion.png", "scale": 3, "frame_count": 10,
          "frame_size": (64, 64), "action": self.enable_defense_boost, "cleanup": self.disable_defense_boost},
          
      "wind_screen": {"active": False, "start_time": 0, "duration": None, "cooldown": 100, "frames": wind_frames, "index": 0, 
          "last_update": 0, "positions": [], "action": self.no_action, "cleanup": self.no_cleanup}}

    # Load frames
    for key, effect in self.effects.items():
      if "path" not in effect or "frame_count" not in effect or effect["frame_count"] == 0:
          continue
      sheet = pygame.image.load(effect["path"]).convert_alpha()
      frames = [getImage(sheet, i, *effect["frame_size"], effect["scale"]) for i in range(effect["frame_count"])]
      effect["frames"] = frames

  def set_finn(self, finn):
    self.finn_ref = finn

  def trigger_effect(self, effect_key):
    for key, effect in self.effects.items():
      if key != "poisoned" and effect["active"]:
        effect["active"] = False
        effect["cleanup"]()

    effect = self.effects.get(effect_key)
    if effect:
      effect["active"] = True
      effect["start_time"] = pygame.time.get_ticks()
      effect["index"] = 0
      effect["action"]()

    if effect_key == "speed_boost":
      wind = self.effects["wind_screen"]
      wind["active"] = True
      wind["start_time"] = pygame.time.get_ticks()
      wind["positions"] = []

  def poisoned(self):
    time_ms = pygame.time.get_ticks()
    temp = screen.copy()
    angle = math.sin(time_ms / 200) * 3
    scale = 1 + math.sin(time_ms / 300) * 0.02
    new_size = (int(screen.get_width() * scale), int(screen.get_height() * scale))
    temp = pygame.transform.smoothscale(temp, new_size)
    temp = pygame.transform.rotate(temp, angle)
    rect = temp.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.fill((0, 0, 0))
    screen.blit(temp, rect.topleft)
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 255, 0, 80))
    screen.blit(overlay, (0, 0))

  def apply_effects(self):
    now = pygame.time.get_ticks()
    for key, effect in self.effects.items():
      if key == "wind_screen":
          self.apply_wind_effect()
          continue

      if effect["active"]:
        elapsed = now - effect["start_time"]
        if elapsed > effect["duration"]:
          effect["active"] = False
          effect["cleanup"]()
          continue

        if key == "poisoned":
          self.poisoned()
          continue

        if not effect["frames"]:
          continue

        if now - effect.get("last_update", 0) > effect["cooldown"]:
          effect["index"] = (effect["index"] + 1) % len(effect["frames"])
          effect["last_update"] = now

        if self.finn_ref:
          frame = effect["frames"][effect["index"]]
          x = self.finn_ref.rect.centerx - frame.get_width() // 2
          y = self.finn_ref.rect.centery - frame.get_height() // 2
          screen.blit(frame, (x, y))

  def apply_wind_effect(self):
    wind = self.effects["wind_screen"]
    now = pygame.time.get_ticks()
    
    if (not self.effects["speed_boost"]["active"] and (not self.finn_ref.running or self.finn_ref.stamina_bar.current_stamina <= 0)):
        wind["active"] = False
        return

    if now - wind["last_update"] > wind["cooldown"]:
      wind["index"] = (wind["index"] + 1) % len(wind["frames"])
      wind["last_update"] = now
      wind["positions"].append([SCREEN_WIDTH, random.randint(100, 450)])

    frame = wind["frames"][wind["index"]]
    for pos in list(wind["positions"]):
      pos[0] -= 20
      screen.blit(frame, (pos[0], pos[1]))
      if pos[0] < -frame.get_width():
          wind["positions"].remove(pos)

  def trigger_poison(self):
      poison = self.effects["poisoned"]
      poison["active"] = True
      poison["start_time"] = pygame.time.get_ticks()

  # === Action and Cleanup Functions ===
  def no_action(self):
    pass

  def no_cleanup(self):
    pass

  def enable_bullet_buff(self):
    self.finn_ref.bullet_buff = True

  def disable_bullet_buff(self):
    self.finn_ref.bullet_buff = False

  def apply_heal(self):
    self.finn_ref.health_bar.heal(6)

  def apply_stamina(self):
    self.finn_ref.stamina_bar.increaseStamina(3)

  def enable_blue_buff(self):
    self.finn_ref.base_speed *= 2
    self.finn_ref.invincible_buff = True

  def disable_blue_buff(self):
    self.finn_ref.base_speed /= 2
    self.finn_ref.invincible_buff = False
  
  def enable_defense_boost(self):
    self.finn_ref.invincible_buff = True

  def disable_defense_boost(self):
    self.finn_ref.invincible_buff = False

scene = Scenes()
running = True

while running:
  pygame.mouse.set_visible(False)
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    scene.mouse.get_input(event)

    # === Handle input depending on game state ===
    if game_state == "menu":
      start_button.clicked = False
      leaderboard_button.clicked = False
      exit_button.clicked = False

    elif game_state == "username_input":
      scene.leaderboard.get_input(event)

    elif game_state == "playing":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          scene.paused = not scene.paused
          if scene.paused:
            scene.pause_start_time = pygame.time.get_ticks()
            scene.timer_active = False
            pygame.mixer.pause()
          else:
            paused_duration = pygame.time.get_ticks() - scene.pause_start_time
            scene.total_paused_time += paused_duration
            scene.timer_active = True
            pygame.mixer.unpause()

        elif event.key == pygame.K_r and scene.game_over:
          scene = Scenes()
          game_state = "playing"
          scene.timer_start = pygame.time.get_ticks()
          scene.warmup_start = pygame.time.get_ticks()
          scene.game_started = True
          scene.in_warmup = True
          scene.game_over = False
          scene.game_finished = False
          scene.total_paused_time = 0
          scene.running_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Game Running Sound Effect.mp3")
          scene.running_sound.play(loops=-1)
          scene.running_sound.set_volume(0.5)
          continue

      if scene.paused:
        screen.fill((0, 0, 0))
        pause_font = large_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_font, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
        pygame.display.update()
        continue

      else:
        scene.dialogue.handle_input(event)
        scene.inventory.handle_click(event)
        scene.finn.handle_input(event)

  # === Update screen depending on game state ===
  if game_state == "menu":
    screen.fill((0, 0, 0))
    screen.blit(menu_bg, (0, 0))
    if not pygame.mixer.get_busy():
      scene.menu_music.play(loops=-1)

    if start_button.draw(screen):
      scene.menu_music.stop()
      game_state = "username_input"
      scene.leaderboard.accepting_username = True
      scene.leaderboard.done_accepting_username = False
      scene.leaderboard.username = ""
    if leaderboard_button.draw(screen):
      scene.menu_music.stop()
      game_state = "leaderboard"
    if exit_button.draw(screen):
      running = False

  elif game_state == "username_input":
    screen.fill((0, 0, 0))
    scene.leaderboard.get_username()
    if scene.leaderboard.done_accepting_username:
      game_state = "cutscene"
    if back_button.draw(screen):
      scene.menu_music.play(loops=-1)
      game_state = "menu"
      scene.leaderboard.accepting_username = False
      scene.leaderboard.done_accepting_username = False
      scene.leaderboard.username = ""

  elif game_state == "cutscene":
    offset_x, offset_y = scene.get_shake_offset()
    if scene.dialogue.active_text <= 7:
        screen.blit(cutscene1_img, (0 + offset_x, 0 + offset_y))
    elif 8 <= scene.dialogue.active_text <= 13:
        screen.blit(cutscene2_img, (0 + offset_x, 0 + offset_y))
    else:
        screen.blit(cutscene3_img, (0 + offset_x, 0 + offset_y))
    scene.dialogue.draw(scene.cutscene_script)

    if scene.dialogue.visible:
      if next_button.draw(screen) and scene.dialogue.done:
        scene.dialogue.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

      if back_button.draw(screen) and scene.dialogue.active_text > 0:
        scene.dialogue.active_text -= 1
        scene.dialogue.counter = 0
        scene.dialogue.done = False
    else:
      game_state = "tutorial"

  elif game_state == "tutorial":
    screen.blit(tutorial_image, (0, 0))
    if next_button.draw(screen):
      # Start game
      scene.timer_start = pygame.time.get_ticks()
      scene.warmup_start = pygame.time.get_ticks()
      scene.game_started = True
      scene.in_warmup = True
      scene.running_sound = pygame.mixer.Sound(Path("assets") / "audio" / "Game Running Sound Effect.mp3")
      scene.running_sound.play(loops=-1)
      scene.running_sound.set_volume(0.5)
      game_state = "playing"

  elif game_state == "leaderboard":
    screen.fill((0, 0, 0))
    scene.leaderboard.show_leaderboard()
    if back_button.draw(screen):
      game_state = "menu"

  elif game_state == "playing":
    if not scene.paused:
      scene.finn.update()
      scene.level1(speed=scene.scroll_speed, spawn_mushroom=True, num_of_mushroom=2)

  scene.mouse.draw()
  pygame.display.update()

pygame.quit()