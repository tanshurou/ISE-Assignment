import pygame
import spritesheet1
import random
import math
from pathlib import Path
dialogue_queue = []
current_dialogue = None

# ─── module‐level state ──────────────────────────────────────────
dialogue_queue           = []
current_dialogue         = None

# flags used by nested functions & classes
game_over                = False
victory_sound_played     = False
fireworks_played         = False
game_over_sound_played   = False
fight_started            = False
# ────────────────────────────────────────────────────────────────

def run_stage2(screen):
    global fight_started, game_over, victory_sound_played, fireworks_played, game_over_sound_played
    fight_started = False
    game_over = False
    victory_sound_played = False
    fireworks_played = False
    game_over_sound_played = False
    
    ICEBALL_SECOND_EVENT = pygame.USEREVENT + 1
    SECOND_SOUND_DELAY = 5000  # milliseconds

    # ------------------------------
    # Initialization
    # ------------------------------
   
    
    SFX_VOLUME   = 0.3
    MUSIC_VOLUME = 0.3
    
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 736
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Finn vs Ice King Boss")
    clock = pygame.time.Clock()
    FPS = 90
    SPIKE_BLOCK_DIST = 300

    # ------------------------------
    # Resource Paths    
    # ------------------------------
    BASE = Path("assets") / "stage2_assets"

    background = pygame.image.load(BASE / "Ice_Background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    backgroundColor = (0, 0, 0)

    finn_sheet           = spritesheet1.SpriteSheet(pygame.image.load(BASE / "Finn_Running.png").convert_alpha())
    ice_king_sheet_image = pygame.image.load(BASE / "Ice King movements.png").convert_alpha()
    death                = pygame.image.load(BASE / "ice king death.png").convert_alpha()
    boss_powers          = pygame.image.load(BASE / "snowball effects.png").convert_alpha()
    powers2              = pygame.image.load(BASE / "ice spikes.png").convert_alpha()
    finalpowers          = pygame.image.load(BASE / "ice cubes.png").convert_alpha()
    barrier              = pygame.image.load(BASE / "wall.png").convert_alpha()
    rock_img             = pygame.image.load(BASE / "falling rock.png").convert()
    slash_img            = pygame.image.load(BASE / "sword swing effect.png").convert_alpha()
    hit_img              = pygame.image.load(BASE / "sword hit effect.png").convert_alpha()
    clash_img            = pygame.image.load(BASE / "clashing effect.png").convert_alpha()
    explosion_img        = pygame.image.load(BASE / "explosion effect.png").convert_alpha()
    tutorial_images = [
        pygame.image.load(BASE / "control tutorials.jpg").convert(),
        pygame.image.load(BASE / "snowball tutorial.png").convert(),
        pygame.image.load(BASE / "ice spike tutorial.png").convert(),
        pygame.image.load(BASE / "ice cube tutorial.png").convert()
    ]
    cutscene_images = [
        pygame.image.load(BASE / "finn face mountain cutscene.png").convert(),
        pygame.image.load(BASE / "finn go up mountain cutscene.png").convert(),
        pygame.image.load(BASE / "finn face ice king cutscene.png").convert()
    ]
    cutscene_images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in cutscene_images]
    final_cutscene = pygame.image.load(BASE / "finn saves PB cutscene.png").convert()
    final_cutscene = pygame.transform.scale(final_cutscene, (SCREEN_WIDTH, SCREEN_HEIGHT))
    victory_screen = pygame.image.load(BASE / "victory screen.png").convert()
    victory_screen = pygame.transform.scale(victory_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    iceking_health_full  = pygame.transform.scale(
        pygame.image.load(BASE / "stamina1.png").convert_alpha(), (20, 40)
    )
    iceking_health_empty = pygame.transform.scale(
        pygame.image.load(BASE / "stamina2.png").convert_alpha(), (20, 40)
    )
    rock_img.set_colorkey((0, 0, 0))
    rock_chunk_img = rock_img.convert_alpha()
    rock_chunk_img.fill((100, 200, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
    finn_img             = pygame.image.load(BASE / "finn_icon.PNG").convert_alpha()
    finn_icon            = pygame.transform.scale(finn_img, (110, 110))
    ice_king_img         = pygame.image.load(BASE / "iceking_icon.PNG").convert_alpha()
    iceking_icon         = pygame.transform.scale(ice_king_img, (110, 110))
    pb_img               = pygame.image.load(BASE / "PB icon.PNG").convert_alpha()
    pb_icon              = pygame.transform.scale(pb_img, (110, 110))
    dialog_box           = pygame.image.load(BASE / "Premade dialog box medium.png").convert_alpha()
    dialogue_box_img     = pygame.transform.scale(dialog_box, (800, 150))
    dialog_font          = pygame.font.Font(BASE / "PressStart2P.ttf", 12)
    tutorial_font        = pygame.font.Font(BASE / "PressStart2P.ttf", 24)
    text_font            = pygame.font.Font(BASE / "PressStart2P.ttf", 18)
    # Load Finn’s sword SFX
    sword_swoosh_sound = pygame.mixer.Sound(BASE / "mixkit-metal-hit-woosh-1485.wav")
    sword_swoosh_sound.set_volume(SFX_VOLUME)
    sword_hit_sound    = pygame.mixer.Sound(BASE / "mixkit-dagger-woosh-1487.wav")
    sword_hit_sound.set_volume(SFX_VOLUME)
    metal_strike_sound = pygame.mixer.Sound(BASE / "mixkit-metallic-sword-strike-2160.wav")
    metal_strike_sound.set_volume(SFX_VOLUME)
    #Ice King sound effect
    ice_cube_sound = pygame.mixer.Sound(BASE / "Ice Cube sound.mp3")
    ice_cube_sound.set_volume(SFX_VOLUME)
    ice_ball_sound = pygame.mixer.Sound(BASE / "Ice ball sound.mp3")
    ice_ball_sound.set_volume(SFX_VOLUME)
    ice_spike_sound = pygame.mixer.Sound(BASE / "Ice Spike sound.mp3")
    ice_spike_sound.set_volume(SFX_VOLUME)
    #Stage 2 cutscene sound effect
    cutscene_drone_sound = pygame.mixer.Sound(BASE / "drone-high-tension-and-suspense-background-162365.mp3")
    cutscene_drone_sound.set_volume(SFX_VOLUME) 
    dialogue_bgm = pygame.mixer.Sound(BASE / "merx-market-song-33936.mp3")
    dialogue_bgm.set_volume(SFX_VOLUME)
    click_sound = pygame.mixer.Sound(BASE / "ui-button-click-8-341030.mp3")
    click_sound.set_volume(SFX_VOLUME)
    victory_sound = pygame.mixer.Sound(BASE / "orchestral-win-331233.mp3")
    victory_sound.set_volume(MUSIC_VOLUME)  
    fireworks_sound = pygame.mixer.Sound(BASE / "fireworks-29629.mp3")
    fireworks_sound.set_volume(1)  
    game_over_sound = pygame.mixer.Sound(BASE / "kl-peach-game-over-iii-142453.mp3")
    game_over_sound.set_volume(SFX_VOLUME)
    restart_sound = pygame.mixer.Sound(BASE/"button-124476.mp3")
    restart_sound.set_volume(1)
    new_victory_sound = pygame.mixer.Sound(BASE / "goodresult-82807.mp3")
    new_victory_sound.set_volume(MUSIC_VOLUME)  

    boss_ss   = spritesheet1.SpriteSheet(ice_king_sheet_image)
    abilities = spritesheet1.SpriteSheet(boss_powers)
    spikes_ss = spritesheet1.SpriteSheet(powers2)
    cubes_ss  = spritesheet1.SpriteSheet(finalpowers)
    defeat_ss = spritesheet1.SpriteSheet(death)
    wall_ss   = spritesheet1.SpriteSheet(barrier)
    swing_ss  = spritesheet1.SpriteSheet(slash_img)
    hit_ss    = spritesheet1.SpriteSheet(hit_img)
    clash_ss  = spritesheet1.SpriteSheet(clash_img)
    explode_ss = spritesheet1.SpriteSheet(explosion_img)

    # ------------------------------
    # Helper to resize images
    # ------------------------------
    def resizeObject(img, scale):
        w, h = img.get_width(), img.get_height()
        return pygame.transform.scale(img, (int(w*scale), int(h*scale)))

    # ------------------------------
    # HealthBar UI
    # ------------------------------
    class HealthBar():
        def __init__(self):
            self.max_health = 12
            self.current_health = 12
            self.x = 100
            self.y = 50
            self.images = []
            for i in range(1,4):
                img = pygame.image.load(BASE / f"heart{i}.png").convert_alpha()
                img = resizeObject(img, 4)
                self.images.append(img)

            self.take_damage_sound_effect = pygame.mixer.Sound(BASE / "take damage.mp3")
            self.take_damage_sound_effect.set_volume(SFX_VOLUME)
            self.heal_sound_effect        = pygame.mixer.Sound(BASE / "heal.mp3")
            self.heal_sound_effect.set_volume(SFX_VOLUME)

        def draw(self, surf):
            full = self.current_health // 2
            half = self.current_health % 2
            empty = (self.max_health // 2) - full - half
            x = self.x
            for _ in range(full):
                surf.blit(self.images[0], (x, self.y)); x += 40
            if half:
                surf.blit(self.images[1], (x, self.y)); x += 40
            for _ in range(empty):
                surf.blit(self.images[2], (x, self.y)); x += 40
            health_ratio = self.current_health / self.max_health
            percentage = int(health_ratio * 100)
            font = pygame.font.Font(BASE / "PressStart2P.ttf", 18)
            text = font.render(f"{percentage}%", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + 120, self.y - 20))
            surf.blit(text, text_rect)

        def takeDamage(self, amount):
            if self.current_health > 0:
                self.current_health = max(0, self.current_health - amount)
                self.take_damage_sound_effect.play()

        def heal(self, amount):
            if self.current_health < self.max_health:
                self.current_health = min(self.max_health, self.current_health + amount)
                self.heal_sound_effect.play()

    # Instantiate HealthBar
    health_bar = HealthBar()

    # ------------------------------
    # Finn Animation Setup
    # ------------------------------
    UNWANTED_COLORS = [
        (0,255,80),(0,128,128),(0,129,128),(0,129,127),(0,130,127),
        (0,254,80),(0,253,79),(0,253,80),(0,252,79),
        (0,254,81),(0,253,81),(0,250,79),(0,251,79),
        (0,162,232)
    ]

    finn_steps    = [10, 10, 10, 10, 7]  # Right, Left, Down, Up, Attack
    attack_sizes  = [
        (67.5,175),(67.5,175),(67.9,175),
        (68.5,175),(69,175),(69.4,175),(69.4,175)
    ]

    Finn_animations = []
    frame_counter   = 0
    for action_idx, count in enumerate(finn_steps):
        frames = []
        for i in range(count):
            if action_idx == 4:
                w, h = attack_sizes[i]
                img = finn_sheet.get_image(frame_counter, w, h, 1.5, UNWANTED_COLORS)
            elif action_idx == 2:
                img = finn_sheet.get_image(frame_counter, 66.48, 92, 1.5, UNWANTED_COLORS)
            elif action_idx == 3:
                img = finn_sheet.get_image(frame_counter, 64.55, 92, 1.5, UNWANTED_COLORS)
            else:
                img = finn_sheet.get_image(frame_counter, 66, 88, 1.5, UNWANTED_COLORS)
            frames.append(img)
            frame_counter += 1
        Finn_animations.append(frames)

    finn_x, finn_y       = 100, 600
    finn_speed           = 4
    finn_slow_speed      = 2 
    finn_action          = 0
    finn_frame           = 0
    finn_attacking       = False
    finn_last_update     = pygame.time.get_ticks()
    Finn_animation_cd    = 100
    attack_damage_done   = False
    finn_slowed          = False
    slow_start_time      = 0
    slow_duration        = 2000
    finn_blocked         = False
    freeze_duration      = 3000
    freeze_start_time    = 0
    finn_flash           = False
    flash_start_time     = 0
    flash_duration       = 500 
    tutorial_active      = True
    tutorial_stage       = 0
    
    death_screen_time    = None

    # ------------------------------
    # Ice King & Effects Classes
    # ------------------------------
    class IceKing:
        def __init__(self):
            self.max_health = 5000
            self.current_health = 5000

        def take_damage(self, amount):
            self.current_health = max(0, self.current_health - amount)

        def draw_health_bar(self, surf):
            total_segments = 12
            segment_width = iceking_health_full.get_width()
            spacing = 5  # optional spacing between segments
            start_x = SCREEN_WIDTH - (segment_width + spacing) * total_segments - 100
            y = 50

            health_ratio = self.current_health / self.max_health
            full_segments = int(health_ratio * total_segments)

            for i in range(total_segments):
                x = start_x + i * (segment_width + spacing)
                if i < full_segments:
                    surf.blit(iceking_health_full, (x, y))
                else:
                    surf.blit(iceking_health_empty, (x, y))
            
            percentage = int(health_ratio * 100)
            font = pygame.font.Font(BASE / "PressStart2P.ttf", 18)
            text = font.render(f"{percentage}%", True, (255, 255, 255))
            text_rect = text.get_rect(center=(start_x + (segment_width + spacing) * total_segments // 2, y - 20))
            surf.blit(text, text_rect)

    class IceKingGlow:
        def __init__(self):
            self.radius = 90
            self.alpha = 150  # fixed alpha
            self.pulse_speed = 1.5
            self.scale = 1.0
            self.growing = True

            # Pre-draw the circle with fixed alpha
            self.base_image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(
                self.base_image,
                (25, 230, 230, self.alpha),  # Solid color with fixed alpha
                (self.radius, self.radius),
                self.radius
            )

        def update(self):
            # Pulse radius (scale only), no alpha changes
            if self.growing:
                self.scale += 0.005 * self.pulse_speed
                if self.scale >= 1.1:
                    self.growing = False
            else:
                self.scale -= 0.005 * self.pulse_speed
                if self.scale <= 0.9:
                    self.growing = True

        def draw(self, surface, center_x, center_y):
            self.update()
            # Scale without re-blending alpha
            scaled = pygame.transform.smoothscale(
                self.base_image,
                (
                    int(self.base_image.get_width() * self.scale),
                    int(self.base_image.get_height() * self.scale)
                )
            )
            rect = scaled.get_rect(center=(center_x, center_y))
            surface.blit(scaled, rect.topleft)

    class Snowball:
        
        def __init__(self, x, y, fly_frames, impact_frames):
            self.x, self.y = x, y; self.speed = 7
            self.fly, self.impact = fly_frames, impact_frames
            self.frame = 0
            self.image = fly_frames[0]
            self.rect = self.image.get_rect(topleft=(x,y))
            self.has_collided = False
            self.collision_time = 0
            self.timer = pygame.time.get_ticks()
            self.delay = 100

        def update(self, targets):
            
            global game_over, finn_slowed, finn_speed, slow_start_time
            if game_over:
                return

            if not self.has_collided:
                self.x -= self.speed
                self.rect.x = self.x

                if self.x < 0:
                    self.has_collided = True
                    self.collision_time = pygame.time.get_ticks()

                for t in targets:
                    if self.rect.colliderect(t):
                        self.has_collided = True
                        self.collision_time = pygame.time.get_ticks()

                        if not game_over:  # Prevent duplicate handling
                            health_bar.takeDamage(1)

                            if health_bar.current_health <= 0:
                                pygame.mixer.music.stop()
                                
                                game_over = True

                            global finn_slowed, finn_speed, slow_start_time
                            finn_slowed = True
                            finn_speed = finn_slow_speed
                            slow_start_time = pygame.time.get_ticks()
                        break

                self.image = self.fly[0]

            else:
                now = pygame.time.get_ticks()
                if now - self.timer > self.delay:
                    self.timer = now
                    if self.frame < len(self.impact) - 1:
                        self.frame += 1
                self.image = self.impact[self.frame]

                if now - self.collision_time > len(self.impact) * self.delay:
                    self.x = -9999

        def draw(self, surf):
            surf.blit(self.image, (self.x, self.y))

    class IceSpikeWarning:
        def __init__(self, x, y, sprite, max_height=400, grow_time=1000):
            self.x, self.y        = x, y
            self.sprite           = sprite
            self.max_height, self.grow_time = max_height, grow_time
            self.start            = pygame.time.get_ticks()
            self.finished         = False

        def update(self):
            if pygame.time.get_ticks() - self.start >= self.grow_time:
                self.finished = True

        def draw(self, surf):
            elapsed = pygame.time.get_ticks() - self.start
            prog    = min(1, elapsed/self.grow_time)
            cur_h   = int(self.max_height * prog)
            scaled  = pygame.transform.scale(self.sprite, (self.sprite.get_width(), cur_h))
            surf.blit(scaled, (self.x-scaled.get_width()//2, self.y-cur_h))

    class SteamParticle:
        def __init__(self, x, y):
            self.x = x + random.randint(-5, 5)
            self.y = y + random.randint(-5, 5)
            self.radius = random.randint(4, 8)
            self.alpha = random.randint(180, 240)
            self.lifetime = random.randint(1500, 1800)
            self.start_time = pygame.time.get_ticks()
            self.color = (210, 255, 255)
            self.rise_speed = random.uniform(0.2, 0.5)
            self.jitter = random.uniform(-0.6, 0.6)

        def update(self):
            now = pygame.time.get_ticks()
            elapsed = now - self.start_time
            if elapsed > self.lifetime:
                return True  # finished
            self.y -= self.rise_speed
            self.x += self.jitter
            self.alpha = int(255 * (1 - elapsed / self.lifetime))
            return False

        def draw(self, surface):
            puff = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(puff, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
            surface.blit(puff, (self.x - self.radius, self.y - self.radius))

    class IcySteamEmitter:
        def __init__(self, x, y, emit_count=25):
            self.particles = [SteamParticle(x, y) for _ in range(emit_count)]

        def update(self):
            for p in self.particles[:]:
                if p.update():
                    self.particles.remove(p)
            return len(self.particles) == 0

        def draw(self, surface):
            for p in self.particles:
                p.draw(surface)

    class IceSpike:
        def __init__(self, x, y, frames, frame_delay=100):
            self.x = x
            self.ground_y = y
            self.frames = frames
            self.idx = 0
            self.spawn = pygame.time.get_ticks()
            self.last = self.spawn
            self.delay = frame_delay
            self.finished = False

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last > self.delay:
                self.last = now
                self.idx += 1
                if self.idx >= len(self.frames):
                    self.finished = True
            return self.finished

        def draw(self, surf):
            img = self.frames[self.idx]
            rect = img.get_rect(midbottom=(self.x, self.ground_y))
            surf.blit(img, rect.topleft)
            return img, rect

    class IceCube:
        def __init__(self, x, y, frames):
            self.x, self.y      = x, y
            self.speed          = 7
            self.frames         = frames
            self.idx            = 0
            self.image          = frames[0]
            self.rect           = self.image.get_rect(topleft=(x,y))
            self.returning      = False
            self.timer          = pygame.time.get_ticks()
            self.delay          = 100

        def update(self, sword_rects, ice_king_rect, finn_attacking):
            global game_over, finn_blocked, freeze_start_time
            if game_over:
                return False  # Exit early if the game is over

            now = pygame.time.get_ticks()

            if not hasattr(self, 'damaged'):
                self.damaged = False

            if not self.returning:
                self.x -= self.speed
                self.rect.x = self.x

                # Reflect if hit by sword
                if finn_attacking:
                    for sr in sword_rects:
                        if self.rect.colliderect(sr):
                            self.returning = True
                            metal_strike_sound.play()

                            global clash_start_frame, clash_anim_frame, clash_last_update
                            if 'clash_start_frame' not in globals():
                                clash_start_frame = 0
                                clash_anim_frame = 0
                                clash_last_update = pygame.time.get_ticks()
                            break

                # Damage Finn if not reflected and not already done
                if self.rect.colliderect(full_rect) and not self.returning and not self.damaged:
                    if not game_over:  # Protect against duplicate death logic
                        health_bar.takeDamage(1)
                        if health_bar.current_health <= 0:
                            pygame.mixer.music.stop()
                            
                            game_over = True

                        global finn_blocked, freeze_start_time
                        finn_blocked = True
                        freeze_start_time = pygame.time.get_ticks()

                    self.damaged = True
                    self.x = -9999
                    self.rect.x = self.x

                # Animate
                if now - self.timer > self.delay and self.idx < len(self.frames) - 1:
                    self.timer = now
                    self.idx += 1
                self.image = self.frames[self.idx]
                return False

            else:
                # Returning to Ice King
                self.x += self.speed
                self.rect.x = self.x

                if now - self.timer > self.delay and self.idx < len(self.frames) - 1:
                    self.timer = now
                    self.idx += 1
                self.image = self.frames[self.idx]

                # Damage Ice King if it hits
                if ice_king_rect and self.rect.colliderect(ice_king_rect):
                    ice_king.take_damage(150)
                    return True

                return False

        def draw(self, surf):
            if 0 <= self.x <= SCREEN_WIDTH:
                surf.blit(self.image, (self.x, self.y))

    class IceCubeTrail:
        def __init__(self, image, x, y, lifetime=300):
            self.image = image.copy()
            self.x = x
            self.y = y
            self.start_time = pygame.time.get_ticks()
            self.lifetime = lifetime
            self.alpha = 180

        def update(self):
            elapsed = pygame.time.get_ticks() - self.start_time
            self.alpha = max(0, 180 - int((elapsed / self.lifetime) * 180))
            return elapsed >= self.lifetime

        def draw(self, surface):
            faded = self.image.copy()
            faded.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(faded, (self.x, self.y))

    class Snowflake:
        def __init__(self):
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(-50, 0)
            self.speed = random.uniform(0.5, 2)
            self.wind  = random.uniform(-1, 1)

        def update(self):
            self.x += self.wind; self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.y = random.randint(-50, 0)
                self.x = random.randint(0, SCREEN_WIDTH)

        def draw(self):
            pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), 4)

    class FallingShard:
        def __init__(self):
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(-300, -50)
            self.speed = random.uniform(10, 18)  # Increased speed
            self.length = random.randint(50, 80)
            self.width = random.randint(6, 10)
            self.color = (200, 240, 255)
            self.alpha = 200

        def update(self):
            self.y += self.speed
            return self.y > SCREEN_HEIGHT

        def draw(self, surface):
            shard_surf = pygame.Surface((self.width, self.length), pygame.SRCALPHA)
            pygame.draw.rect(shard_surf, (*self.color, self.alpha), (0, 0, self.width, self.length))
            surface.blit(shard_surf, (self.x, self.y))

    class SnowChunk:
        def __init__(self):
            self.width = random.randint(50, 100)
            self.height = random.randint(25, 40)
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = random.randint(-250, -60)
            self.speed = random.uniform(8, 14)
            self.alpha = random.randint(220, 255)  # less transparent
            self.color = (240, 250, 255)

        def update(self):
            self.y += self.speed
            return self.y > SCREEN_HEIGHT

        def draw(self, surface):
            scale_factor = 0.5
            new_width = int(rock_chunk_img.get_width() * scale_factor)
            new_height = int(rock_chunk_img.get_height() * scale_factor)
            scaled_rock = pygame.transform.scale(rock_chunk_img, (new_width, new_height))
            surface.blit(scaled_rock, (self.x, self.y))

    class IceShard:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-4, -1)
            self.life = 400  # milliseconds
            self.start_time = pygame.time.get_ticks()
            self.alpha = 255
            self.size = random.randint(3, 6)

        def update(self):
            now = pygame.time.get_ticks()
            elapsed = now - self.start_time

            self.x += self.vx
            self.y += self.vy
            self.vy += 0.2  # gravity
            self.alpha = max(0, 255 - int(255 * (elapsed / self.life)))

            return elapsed >= self.life

        def draw(self, surface):
            shard = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.polygon(shard, (200, 255, 255, self.alpha), [
                (0, 0), (self.size, 0), (self.size // 2, self.size)
            ])
            surface.blit(shard, (self.x, self.y))

    class Icicle:
        def __init__(self, x, delay=1000):
            self.x = x
            self.y = -20  # Just above screen
            self.width = random.randint(10, 14)
            self.height = random.randint(40, 60)
            self.falling = False
            self.spawn_time = pygame.time.get_ticks()
            self.delay = delay
            self.speed = 6
            self.hit_ground = False
            self.alpha = 255

        def update(self):
            now = pygame.time.get_ticks()

            if not self.falling:
                if now - self.spawn_time >= self.delay:
                    self.falling = True
            else:
                self.y += self.speed
                if self.y >= SCREEN_HEIGHT - 10 and not self.hit_ground:  # hit ground
                    self.hit_ground = True
                    for _ in range(random.randint(4, 6)):
                        ice_shards.append(IceShard(self.x + self.width // 2, SCREEN_HEIGHT - 10))

            if self.hit_ground:
                self.alpha -= 20
                if self.alpha <= 0:
                    return True  # remove icicle

            return False

        def draw(self, surface):
            color = (200, 240, 255, self.alpha)
            icicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.polygon(
                icicle_surface,
                color,
                [(self.width // 2, 0), (0, self.height), (self.width, self.height)]
            )
            surface.blit(icicle_surface, (self.x, self.y))

    class GroundCrack:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = random.randint(80, 120)
            self.height = random.randint(20, 30)
            self.alpha = 255
            self.life = 600  # ms
            self.start_time = pygame.time.get_ticks()
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

            # Draw a jagged crack line
            points = [(0, self.height // 2)]
            for i in range(1, 7):
                px = int((self.width / 6) * i)
                py = self.height // 2 + random.randint(-5, 5)
                points.append((px, py))
            pygame.draw.lines(self.image, (26, 72, 82), False, points, 3)

        def update(self):
            elapsed = pygame.time.get_ticks() - self.start_time
            self.alpha = max(0, 255 - int((elapsed / self.life) * 255))
            return elapsed > self.life

        def draw(self, surface):
            img = self.image.copy()
            img.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(img, (self.x, self.y))

    # ------------------------------
    # Build Boss Animations
    # ------------------------------
    idle_animation, attack_animation, spike_animation, defeated_animation = [], [], [], []
    snowball_fly_frames, snowball_impact_frames = [], []
    icespike_frames, cube_frames = [], []
    barrier_frames = []
    slashing_frames = []
    hitting_frames = []
    clashing_frames = []
    explosion_frames = []
    steam_emitters = []

    idle_w, attack_w = 72, 149
    sprite_h         = 76
    scale            = 1.8
    spike_w, spike_h = 139, 100
    snow_w, snow_h, snow_scale = 62, 46, 2
    laser_w, laser_h, laser_scale = 35, 400, 0.8
    cube_w, cube_h, cube_scale = 98, 98, 0.8
    defeated_w, defeated_h = 80, 90
    wall_w, wall_h = 104, 440
    swing_w, swing_h = 70, 72
    hit_w, hit_h = 74, 68
    clash_w, clash_h = 64, 70
    explode_w, explode_h = 64, 70
    remove_colors = [(0,0,0)]

    # Load ice king animations
    for i in reversed(range(10)):
        idle_animation.append(boss_ss.get_image(i, idle_w, sprite_h, scale, remove_colors))
    for i in reversed(range(10,15)):
        attack_animation.append(boss_ss.get_image(i, attack_w, sprite_h, scale, remove_colors))
    for i in reversed(range(20,26)):
        spike_animation.append(boss_ss.get_image(i, spike_w, spike_h, scale, remove_colors))
    for i in reversed(range(8)):
        defeated_animation.append(defeat_ss.get_image(i, defeated_w, defeated_h, scale, remove_colors))

    # Load snowballs
    for i in range(4):
        snowball_fly_frames.append(abilities.get_image(i, snow_w, snow_h, snow_scale, remove_colors))
    snowball_impact_frames = snowball_fly_frames[1:]

    # Load ice spike warnings & frames
    for i in range(1,23):
        icespike_frames.append(spikes_ss.get_image(i, 61.7, 315, 2, remove_colors))
    ice_spike_warning_img = spikes_ss.get_image(0, laser_w, laser_h, laser_scale, remove_colors)

    # Load ice cubes
    for i in range(3):
        cube_frames.append(cubes_ss.get_image(i, cube_w, cube_h, cube_scale, remove_colors))

    for i in range(14):
        barrier_frames.append(wall_ss.get_image(i, wall_w, wall_h, 2, remove_colors))

    for i in range(14):
        slashing_frames.append(swing_ss.get_image(i, swing_w, swing_h, 1.5, remove_colors))

    for i in range(13):
        hitting_frames.append(hit_ss.get_image(i, hit_w, hit_h, 1.5, remove_colors))

    for i in range(14):
        clashing_frames.append(clash_ss.get_image(i, clash_w, clash_h, 1.5, remove_colors))

    for i in range(9):
        explosion_frames.append(explode_ss.get_image(i, explode_w, explode_h, 1.5, remove_colors))

    for i in range(len(tutorial_images)):
        tutorial_images[i] = pygame.transform.scale(tutorial_images[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

    # ------------------------------
    # Phase Logic & Helpers
    # ------------------------------
    ice_king = IceKing()
    ice_king_glow = IceKingGlow()
    snowballs, warnings, spikes, ice_cubes = [], [], [], []
    cube_trails = []
    snowflakes = [Snowflake() for _ in range(50)]
    falling_shards = []
    falling_snow_chunks = []
    icicles = []
    ice_shards = []
    ground_cracks = []

    ice_xpos, ice_ypos, original_ypos = 1075, 450, 450
    ice_speed, ice_ydir = 2, 0

    frame_cd        = 250
    last_update     = pygame.time.get_ticks()
    state_timer     = pygame.time.get_ticks()
    animation_frame = 0

    fight_started   = False
    fight_start     = 0
    phase2_started  = False
    phase3_started  = False
    snow_phase2_start = 0
    cube_phase3_start = 0
    spawned_snow    = False
    spawned_cube    = False
    ice_spike_loops = 0
    shake_timer = 0
    shake_duration = 0  # milliseconds to shake
    shake_magnitude = 20
    fall_effect_duration = 1000  # milliseconds
    ice_king_hit = False
    hit_overlay_duration = 500 
    hit_overlay_start_time = 0
    charging_ice_cube = False
    charging_start_time = 0
    charging_duration = 2500
    charging_started = False
    charging_just_finished = False
    death_start_time = None
    explosion_index = None
    explosion_timer = None
    ice_king_fully_defeated = False
    defeated_target_y = 450
    defeated_drop_speed = 4
    dialogue_queue = []
    current_dialogue = None
    dialogue_start_time = 0
    dialogue_duration = 3000
    parry_dialogue_triggered_this_cycle = False
    defeat_dialogue_shown = False
    pending_phase = None
    phase_dialogue_active = False
    finn_forced_position_x = None
    phase1_dialogue_queued = False
    cutscene_stage = 0
    cutscene_active = True
    cutscene_sound_playing = False
    cutscene_dialogue_shown = False
    final_cutscene_active = False
    final_cutscene_shown = False
    defeat_dialogue_finished = False
    victory_screen_active = False

    tutorial_titles = ["Snowball Attack", "Ice Spike Danger", "Reflect Ice Cubes"]
    tutorial_texts = [
        "Ice King shoots snowballs. Avoid them or you'll be slowed down temporarily.",
        "Spikes erupt from the ground. Watch for the glowing warning and avoid them.",
        "You can reflect ice cubes with your sword. Time your attack and send them flying back!"
    ]
    cutscene_dialogue = {
        "intro": [
            {"speaker": "Finn", "line": "I'm coming to save you, Princess Bubblegum!"}
        ],
        "final": [
            {"speaker": "Princess Bubblegum", "line": "Finn! You saved me!"},
            {"speaker": "Finn", "line": "Alright, now let's go back and celebrate this momentous occasion!"},
            {"speaker": "Finn", "line": "And no you are not invited, Ice King!"}
        ]
    }
    battle_dialogue = {
        "phase1": [
            {"speaker": "Ice King", "line": "You dare challenge the Ice King!?"},
            {"speaker": "Finn", "line": "Yeah! I'm not afraid of your frosty face!"},
            {"speaker": "Ice King", "line": "Then prepare to get frozen in time!"},
            {"speaker": "Finn", "line": "Bring it on, Ice King!"}
        ],
        "phase2": [
            {"speaker": "Ice King", "line": "Witness the wrath of my spikes!"},
            {"speaker": "Finn", "line": "Nothing can stop me when I'm saving my friends, especially not snow cones!"}
        ],
        "phase3": [
            {"speaker": "Ice King", "line": "You've made it this far... but are you brave enough to win her over by winning against me!?"},
            {"speaker": "Finn", "line": "Let's end this once and for all, Ice King!"},
            {"speaker": "Finn", "line": "And I'm ending you with my sword!"},
        ],
        "parry": [
            {"speaker": "Ice King", "line": "Parry this, you crusty do-gooder!", "duration": 1500}
        ],
        "defeat": [
            {"speaker": "Ice King", "line": "Ugh... fine..."},
            {"speaker": "Ice King", "line": "You can have her..."}
        ]
    }

    icon_map = {
        "Finn": finn_icon,
        "Ice King": iceking_icon,
        "Princess Bubblegum": pb_icon
    }

    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        if current_line:
            lines.append(current_line.strip())

        return lines

    def queue_dialogue(script):
        global dialogue_queue
        dialogue_queue.extend(script)

    def draw_dialogue(surface, speaker, line):
        box_width, box_height = dialogue_box_img.get_size()
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = SCREEN_HEIGHT - box_height - 20  # bottom margin

        # Draw dialogue box
        surface.blit(dialogue_box_img, (box_x, box_y))

        # Draw icon
        if speaker in icon_map:
            icon = icon_map[speaker]
            icon_x = box_x + 55
            icon_y = box_y + (box_height - icon.get_height()) // 2 - 10
            surface.blit(icon, (icon_x, icon_y))
        else:
            icon_x = box_x

        # Calculate available space for text
        text_x = icon_x + 180
        max_text_width = box_width - (text_x - box_x) - 40  # right padding
        line_spacing = 28  # Adjust for font size and line height

        # Wrap the line
        wrapped_lines = wrap_text(line, dialog_font, max_text_width)

        # Calculate vertically centered starting Y position
        total_text_height = len(wrapped_lines) * line_spacing
        text_y = box_y + (box_height - total_text_height) // 2 + 15  # +5 fine-tunes baseline

        # Render each line
        for i, text_line in enumerate(wrapped_lines):
            text_surface = dialog_font.render(text_line, True, (50, 20, 20))
            surface.blit(text_surface, (text_x, text_y + i * line_spacing))

    def generate_non_overlapping_positions(count, x_min, x_max, gap, forbidden=None):
        positions, attempts = [], 0
        while len(positions) < count and attempts < 100:
            x = random.randint(x_min, x_max)
            if any(abs(x-p) < gap for p in positions):
                attempts += 1; continue
            if forbidden and forbidden[0] <= x <= forbidden[1]:
                attempts += 1; continue
            positions.append(x)
        return positions

    def phase1(now):
        global fight_started, fight_start, state_timer
        nonlocal animation_frame, last_update, ice_ydir, ice_king_state, ice_ypos
        nonlocal pending_phase, phase_dialogue_active
        # clear any stray warnings/spikes
        warnings.clear()
        spikes.clear()

        # durations (in milliseconds)
        idle_duration   = 3000   # how long to wait before attacking
        attack_duration = 9000   # how long to attack before idling

        # initialize fight
        if not fight_started:
            if pending_phase != "start_phase1":
                return  # wait until it's ready
            fight_started = True
            fight_start = now
            ice_king_state = "idle"
            animation_frame = 0
            state_timer = now
            pygame.mixer.music.load(BASE / "chiptune-medium-boss-218095.mp3")
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            phase_dialogue_active = False

        # idle → attack
        if ice_king_state == "idle" and now - state_timer >= idle_duration:
            ice_king_state  = "attack"
            animation_frame = 0
            state_timer     = now

        # attack → idle after attack_duration
        elif ice_king_state == "attack" and now - state_timer >= attack_duration:
            ice_king_state  = "idle"
            animation_frame = 0
            state_timer     = now

        # while attacking, do the bounce
        elif ice_king_state == "attack":
            if ice_ypos <= 90:
                ice_ydir = 1
            elif ice_ypos >= 450:
                ice_ydir = -1
            ice_ypos += ice_speed * ice_ydir

        # animation + snowball spawn
        if now - last_update >= frame_cd:
            prev = animation_frame
            if ice_king_state == "attack":
                animation_frame = (animation_frame + 1) % len(attack_animation)
                # on frame 4 fire a snowball
                if animation_frame == 4 and prev != 4:
                    snowballs.append(
                        Snowball(
                            ice_xpos - 70,
                            ice_ypos + 30,
                            snowball_fly_frames,
                            snowball_impact_frames
                        )
                    )
                    ice_ball_sound.play()
            else:
                animation_frame = (animation_frame + 1) % len(idle_animation)

            last_update = now

    def handle_dropping_phase(now):
        global ice_king_state, animation_frame, state_timer, last_update, vulnerable_start
        nonlocal ice_ypos
        if ice_ypos < original_ypos:
            ice_ypos += 4
        else:
            ice_ypos, ice_king_state, vulnerable_start, animation_frame, state_timer = original_ypos, "vulnerable", now, 0, now
        if now - last_update >= frame_cd:
            animation_frame = (animation_frame + 1) % len(idle_animation)
            last_update = now

    def handle_vulnerable_phase(now):
        global ice_king_state, animation_frame, last_update, ice_spike_loops, vulnerable_start
        global ice_xpos, ice_ypos

        if now - last_update >= frame_cd:
            animation_frame = (animation_frame + 1) % len(idle_animation)
            last_update     = now

        shiver_offset = int(math.sin(now / 100 * math.pi * 2) * 3)
        current_frame = idle_animation[animation_frame]
        screen.blit(current_frame, (ice_xpos + shiver_offset, ice_ypos))

        if now - vulnerable_start >= 5000:
            ice_king_state   = "phase2"
            ice_spike_loops  = 0  
            animation_frame  = 0
            last_update      = now
        
        return current_frame

    def phase2(now):
        global vulnerable_start
        nonlocal ice_king_state, animation_frame, last_update, ice_spike_loops
        nonlocal snow_phase2_start, spawned_snow, ice_ydir, ice_ypos
        nonlocal warnings, spikes
        nonlocal shake_timer, shake_duration
        if phase_dialogue_active and dialogue_is_blocking:
            return
        # --- SPIKE PHASE ---
        if ice_king_state == "phase2":
            # 1) Spawn 3 rounds of warnings→spikes, then switch to snowball
            if not warnings and not spikes:
                if ice_spike_loops < 3:
                    forbidden_zone = (ice_xpos - 100, ice_xpos + 100)
                    for x in generate_non_overlapping_positions(5, 200, 850, 100, forbidden_zone):
                        warnings.append(IceSpikeWarning(x, 700, ice_spike_warning_img))
                        steam_emitters.append(IcySteamEmitter(x, 700))
                    ice_spike_loops += 1
                else:
                    ice_king_state     = "attack"
                    snow_phase2_start = now
                    animation_frame   = 0
                    last_update       = now
                    return

            # 2) Advance animation
            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(spike_animation)
                last_update     = now

            # 3) Draw the current spike‐attack pose
            frame_idx = animation_frame % len(spike_animation)
            screen.blit(spike_animation[frame_idx], (ice_xpos, ice_ypos))

        # --- SNOWBALL PHASE ---
        elif ice_king_state == "attack":
            # 1) Animate attack
            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(attack_animation)
                last_update     = now

            # 2) Hover up/down
            if ice_ypos <= 90:
                ice_ydir = 1
            elif ice_ypos >= 450:
                ice_ydir = -1
            ice_ypos += ice_speed * ice_ydir

            # 3) Fire snowballs exactly on frame 4
            if animation_frame == 4 and not spawned_snow:
                snowballs.append(Snowball(ice_xpos-100, ice_ypos+40, snowball_fly_frames, snowball_impact_frames))
                snowballs.append(Snowball(ice_xpos-60,  ice_ypos+40, snowball_fly_frames, snowball_impact_frames))
                ice_ball_sound.play()
                pygame.time.set_timer(ICEBALL_SECOND_EVENT, SECOND_SOUND_DELAY, loops=1)
                spawned_snow = True
                
            elif animation_frame != 4:
                spawned_snow = False

            # 4) Draw snowball‐attack pose
            screen.blit(attack_animation[animation_frame], (ice_xpos, ice_ypos))

            # 5) After 5 s → dropping
            if now - snow_phase2_start >= 5000:
                ice_king_state   = "dropping"
                vulnerable_start = now
                animation_frame  = 0
                last_update      = now
                ice_spike_loops  = 0

        # --- DROPPING PHASE (use helper) ---
        elif ice_king_state == "dropping":
            handle_dropping_phase(now)

        # --- VULNERABLE PHASE (use helper) ---
        elif ice_king_state == "vulnerable":
            handle_vulnerable_phase(now)

        # ─── Only spawn & draw ice spikes in Phases 2 & 3 ────────────────────
        if ice_king_state in ("phase2", "phase3"):
            # Turn warnings into real spikes
            for w in warnings[:]:
                w.update()
                if w.finished:
                    ice_spike_sound.play() 
                    spikes.append(IceSpike(w.x, 800, icespike_frames))
                    warnings.remove(w)
                    shake_duration = 3000
                    shake_timer = pygame.time.get_ticks()
                    ground_cracks.append(GroundCrack(w.x - 55, 675))  # Adjust Y to be near spike base

            # Update & draw live spikes
            for sp in spikes[:]:
                if sp.update():
                    spikes.remove(sp)
                else:
                    sp.draw(screen)

    def phase3(now):
        global ice_king_state, animation_frame, last_update, ice_spike_loops
        global cube_phase3_start, spawned_cube, ice_ydir, ice_ypos
        global shake_duration, shake_timer, charging_ice_cube, charging_started, charging_just_finished
        if phase_dialogue_active and dialogue_is_blocking:
            return 
        # Spike Phase 3
        if ice_king_state == "phase3":
            if not warnings and not spikes:
                if ice_spike_loops < 5:
                    fz = (ice_xpos-100, ice_xpos+100)
                    for x in generate_non_overlapping_positions(5,200,850,100,fz):
                        warnings.append(IceSpikeWarning(x,700,ice_spike_warning_img))
                        steam_emitters.append(IcySteamEmitter(x, 700))
                    ice_spike_loops += 1
                else:
                    ice_king_state, cube_phase3_start, animation_frame, last_update = "cube_attack", now, 0, now
                    spawned_cube = False
                    charging_ice_cube = False
                    return
            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(spike_animation)
                last_update = now
            frame_idx = animation_frame % len(spike_animation)
            screen.blit(spike_animation[frame_idx], (ice_xpos, ice_ypos))

        # Ice Cube Attack
        elif ice_king_state == "cube_attack":
            global parry_dialogue_triggered_this_cycle, charging_start_time, dialogue_start_time, current_dialogue, charging_started

            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(attack_animation)
                last_update = now
                if animation_frame == 0:
                    charging_started = False

            if ice_ypos <= 90: ice_ydir = 1
            elif ice_ypos >= 450: ice_ydir = -1
            ice_ypos += ice_speed * ice_ydir

            if animation_frame == 3 and not charging_ice_cube and not charging_started:
                charging_ice_cube = True
                charging_started = True
                charging_start_time = now
                ice_cube_sound.play()

                if not parry_dialogue_triggered_this_cycle:
                    current_dialogue = dict(battle_dialogue["parry"][0])
                    current_dialogue["type"] = "parry"
                    dialogue_start_time = pygame.time.get_ticks()
                    parry_dialogue_triggered_this_cycle = True
            
            if charging_ice_cube:
                elapsed = now - charging_start_time
                if elapsed > charging_duration:
                    charging_ice_cube = False
                    charging_just_finished = True

            if charging_just_finished and animation_frame == 4 and not spawned_cube:
                spawn_count = random.randint(3, 6)  # randomly spawn between 2 and 5 cubes
                spawn_x = ice_xpos + 30
                for i in range(spawn_count):
                    random_y_offset = random.randint(80, SCREEN_HEIGHT - 100)  # vertical randomness
                    spawn_y = random_y_offset
                    ice_cubes.append(IceCube(spawn_x, spawn_y, cube_frames))
                spawned_cube = True
                charging_just_finished = False

            screen.blit(attack_animation[animation_frame], (ice_xpos, ice_ypos))

            print(f"Checking phase reset: now={now}, cube_phase3_start={cube_phase3_start}, elapsed={now - cube_phase3_start}")

            if now - cube_phase3_start >= 5000:
                print("Resetting phase to phase3")
                ice_king_state, animation_frame, last_update, ice_spike_loops = "phase3", 0, now, 0
                parry_dialogue_triggered_this_cycle = False
                spawned_cube = False
                charging_started = False

        # Warnings & Spikes
        for w in warnings[:]:
            w.update()
            if w.finished:
                ice_spike_sound.play() 
                spikes.append(IceSpike(w.x,800,icespike_frames))
                warnings.remove(w)
                shake_duration = 3000
                shake_timer = pygame.time.get_ticks()
                ground_cracks.append(GroundCrack(w.x - 55, 675))  # Adjust Y to be near spike base
        for sp in spikes[:]:
            if sp.update(): spikes.remove(sp)
            else: sp.draw(screen)
        
    def reset_game():
        global health_bar, ice_king, finn_x, finn_y, finn_action, finn_attacking
        global finn_frame, fight_started, game_over, pending_phase, tutorial_active
        global tutorial_stage, phase1_dialogue_queued, dialogue_queue, current_dialogue
        global ice_king_state, snowballs, ice_cubes, spikes, warnings, steam_emitters
        global parry_dialogue_triggered_this_cycle, ice_ypos, animation_frame
        global defeated_dialogue_shown, ice_king_fully_defeated, death_screen_time
        global phase2_started, phase3_started, spawned_snow, spawned_cube
        global ice_spike_loops, snow_phase2_start, cube_phase3_start
        global dialogue_start_time, charging_ice_cube, charging_start_time
        global vulnerable_start, phase_dialogue_active, finn_forced_position_x
        global ice_ydir, ice_speed
        global fireworks_played
        global cutscene_sound_playing
        global dialogue_bgm
        global game_over_sound_played
        global victory_sound_played
        global defeat_dialogue_finished, final_cutscene_active, final_cutscene_shown
        
        
        
        

        # Reset player
        health_bar = HealthBar()
        finn_x, finn_y = 100, 600
        finn_action = 0
        finn_attacking = False
        finn_frame = 0

        # Reset boss
        ice_king = IceKing()
        ice_king_state = "idle"
        animation_frame = 0
        ice_ypos = 450
        ice_ydir = 0
        ice_speed = 2
        ice_king_fully_defeated = False
        defeated_dialogue_shown = False

        # Reset phase flags
        fight_started = False
        game_over = False
        pending_phase = None
        tutorial_active = False  # skip tutorial after reset
        tutorial_stage = 0
        phase1_dialogue_queued = True  # prevent auto-queueing
        parry_dialogue_triggered_this_cycle = False
        phase2_started = False
        phase3_started = False
        spawned_snow = False
        spawned_cube = False
        ice_spike_loops = 0
        snow_phase2_start = 0
        cube_phase3_start = 0
        charging_ice_cube = False
        charging_start_time = 0
        vulnerable_start = 0
        phase_dialogue_active = True
        finn_forced_position_x = None
        death_screen_time = None
        dialogue_start_time = 0
        defeat_dialogue_finished = False
        final_cutscene_active = False
        final_cutscene_shown = False

        # Clear active effects and dialogue
        dialogue_queue.clear()
        current_dialogue = None
        snowballs.clear()
        ice_cubes.clear()
        spikes.clear()
        warnings.clear()
        steam_emitters.clear()

        # Queue phase 1 dialogue immediately
        queue_dialogue(battle_dialogue["phase1"])

        pygame.mixer.music.load(BASE / "chiptune-medium-boss-218095.mp3")
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

    # ------------------------------
    # Main Game Loop
    # ------------------------------
    ice_king_state = "idle"
    phase3_ready = False
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                # 1. Dismiss current dialogue first
                if current_dialogue:
                    current_dialogue = None

                # 2. Then handle cutscene progression
                elif cutscene_active:
                    cutscene_stage += 1
                    cutscene_dialogue_shown = False
                    if cutscene_stage >= len(cutscene_images):
                        cutscene_active = False
                        cutscene_drone_sound.stop()
                        cutscene_sound_playing = False  # reset flag
                        tutorial_active = True
                        current_dialogue = None
                        dialogue_queue.clear()
                        cutscene_dialogue_shown = False
                        dialogue_bgm.fadeout(1000)

                # 3. Handle final cutscene (after defeat)
                elif final_cutscene_active:
                    if not current_dialogue and not dialogue_queue:
                        final_cutscene_active = False
                        victory_screen_active = True

                # 4. Advance tutorial normally
                elif tutorial_active:
                    tutorial_stage += 1
                    if tutorial_stage >= len(tutorial_images):
                        tutorial_active = False
                elif victory_screen_active:
                    running = False
            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_sound.play()
                reset_game()

        if game_over:
            if death_screen_time is None:
                death_screen_time = pygame.time.get_ticks()
            
            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            elif pygame.time.get_ticks() - death_screen_time > 200:
                # Show death overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                font_big = pygame.font.Font(BASE / "PressStart2P.ttf", 48)
                death_text = font_big.render("YOU DIED", True, (255, 0, 0))
                screen.blit(death_text, (SCREEN_WIDTH // 2 - death_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

                font_small = pygame.font.Font(BASE / "PressStart2P.ttf", 18)
                tip = font_small.render("Press R to Restart", True, (255, 255, 255))
                screen.blit(tip, (SCREEN_WIDTH // 2 - tip.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

            pygame.display.flip()
            clock.tick(FPS)
            continue 

        now = pygame.time.get_ticks()
        dialogue_is_blocking = (current_dialogue and current_dialogue.get("type") != "parry")
        phase3_ready = (ice_king_state == "phase3" and not dialogue_is_blocking)
        offset_x, offset_y = 0, 0
        shake_elapsed = pygame.time.get_ticks() - shake_timer
        
        if shake_elapsed < shake_duration:
            offset_x = random.randint(-shake_magnitude, shake_magnitude)
            offset_y = random.randint(-shake_magnitude, shake_magnitude)

            # Only spawn particles for a shorter period
            if shake_elapsed < fall_effect_duration:
                if len(falling_shards) < 20 and random.random() < 0.8:
                    falling_shards.append(FallingShard())
                if len(falling_snow_chunks) < 10 and random.random() < 0.5:
                    falling_snow_chunks.append(SnowChunk())
        screen.fill(backgroundColor)
        if cutscene_active:

            if not cutscene_sound_playing:
                pygame.mixer.music.stop()
                dialogue_bgm.play(-1)  # Loop dialogue music during cutscene
                cutscene_sound_playing = True

            screen.blit(cutscene_images[cutscene_stage], (0, 0))

            if current_dialogue:
                draw_dialogue(screen, current_dialogue["speaker"], current_dialogue["line"])
                if pygame.time.get_ticks() - dialogue_start_time >= current_dialogue.get("duration", 999999):
                    current_dialogue = None

            elif dialogue_queue:
                current_dialogue = dialogue_queue.pop(0)
                dialogue_start_time = pygame.time.get_ticks()

            if cutscene_stage == 0 and not cutscene_dialogue_shown and not current_dialogue and not dialogue_queue:
                queue_dialogue(cutscene_dialogue["intro"])
                cutscene_dialogue_shown = True

            if not cutscene_active and cutscene_sound_playing:
                dialogue_bgm.stop()
                cutscene_sound_playing = False

            pygame.display.flip()
            clock.tick(FPS)
            continue
        if final_cutscene_active:
            screen.blit(final_cutscene, (0, 0))
            if not victory_sound_played:
                fireworks_sound.stop()
                pygame.mixer.music.stop()
                victory_sound.play()
                victory_sound_played = True

            if current_dialogue:
                draw_dialogue(screen, current_dialogue["speaker"], current_dialogue["line"])
                duration = current_dialogue.get("duration", 999999)
                if pygame.time.get_ticks() - dialogue_start_time >= duration:
                    current_dialogue = None

            elif dialogue_queue:
                current_dialogue = dialogue_queue.pop(0)
                dialogue_start_time = pygame.time.get_ticks()

            elif not final_cutscene_shown:
                fireworks_sound.stop()
                queue_dialogue(cutscene_dialogue["final"])
                final_cutscene_shown = True

            # Wait until dialogue finishes, then close final cutscene on click (handled by your event loop)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if victory_screen_active:
            victory_sound.stop()
            new_victory_sound.play()
            screen.blit(victory_screen, (0, 0))

            font_victory = pygame.font.Font(BASE / "PressStart2P.ttf", 24)
            tip = font_victory.render("Click to exit", True, (255, 255, 255))
            screen.blit(tip, (SCREEN_WIDTH // 2 - tip.get_width() // 2, SCREEN_HEIGHT - 35))

            pygame.display.flip()
            clock.tick(FPS)
            continue

        screen.blit(background, (offset_x, offset_y))

        if random.random() < 0.01:  # ~1% chance per frame
            spawn_x = random.randint(100, SCREEN_WIDTH - 100)
            icicles.append(Icicle(spawn_x, delay=random.randint(500, 1500)))

            # ——— Finn Input & Animation ———
        keys = pygame.key.get_pressed()

        # 1) Attack
        if not finn_attacking and keys[pygame.K_SPACE]:
            finn_attacking     = True
            finn_action        = 4
            finn_frame         = 0
            finn_last_update   = now
            attack_damage_done = False
            sword_swoosh_sound.play()

        # 2) Handle attack animation
        if finn_attacking:
            if now - finn_last_update >= Finn_animation_cd:
                finn_last_update += Finn_animation_cd
                finn_frame      += 1
                if finn_frame >= len(Finn_animations[finn_action]):
                    finn_attacking = False
                    finn_action    = 2
                    finn_frame     = 0

        # 3) Movement & directional animation
        else:
            moved      = False
            new_action = finn_action

            if finn_blocked or phase_dialogue_active:
                moved = False
            else:
                # Normal movement handling when Finn is not frozen
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    finn_y -= finn_speed
                    new_action = 3
                    moved = True
                elif keys[pygame.K_s]:
                    finn_y += finn_speed
                    new_action = 2
                    moved = True
                elif keys[pygame.K_a]:
                    finn_x -= finn_speed
                    new_action = 1
                    moved = True
                elif keys[pygame.K_d]:
                    finn_x += finn_speed
                    new_action = 0
                    moved = True

            # Snap to first frame on action change
            if moved and new_action != finn_action:
                finn_action      = new_action
                finn_frame       = 0
                finn_last_update = now

            # Otherwise advance on cooldown
            elif moved and now - finn_last_update >= Finn_animation_cd:
                finn_last_update += Finn_animation_cd
                finn_frame       = (finn_frame + 1) % len(Finn_animations[finn_action])
            idle_ws = Finn_animations[2][0]   # for example, first frame of the down‐run strip

            # pad Finn_animations until you have an entry at index 9
            while len(Finn_animations) < 10:
                Finn_animations.append([idle_ws])

            if not moved:
                # If last move was Up or Down, use action 9 frame 0
                if new_action in (2, 3):
                    finn_action = 9
                    finn_frame  = 0

                # If last move was Left (A), use action 0 frame 1
                elif new_action == 1:
                    finn_action = 1
                    finn_frame  = 0

                # Otherwise (e.g. Right or default), use action 0 frame 0
                else:
                    finn_action = 0
                    finn_frame  = 9
        if finn_slowed:
            if now - slow_start_time >= slow_duration:
                finn_slowed = False
                finn_speed = 4
        # 4) Draw Finn (with invisible walls)
        if not game_over:
            frame_img = Finn_animations[finn_action][finn_frame]
        # Force-move Finn outside spike zone during phase dialogue
        if phase_dialogue_active and finn_forced_position_x is not None:
            finn_x = finn_forced_position_x
        # ── Spike barrier + auto-push during spike phases ──────────────────
        if ice_king_state in ("phase2", "phase3"):
            # get Ice King’s current rect
            boss_img = current[bf]
            ice_rect = boss_img.get_rect(topleft=(ice_xpos, ice_ypos))

            # Compute the full “no-go” zone
            left_bound  = ice_xpos - SPIKE_BLOCK_DIST - 100  # Left boundary of the "danger zone"
            right_bound = ice_xpos + SPIKE_BLOCK_DIST  # Right boundary of the "danger zone"

            shift_amount = 100

            for i in range(2):  # Display the barrier on both sides (left and right)
                if i == 0:  # Left side
                    x_pos = ice_xpos - SPIKE_BLOCK_DIST - 100 + shift_amount  # Adjust to place the barrier at the correct position
                else:  # Right side
                    x_pos = ice_xpos + SPIKE_BLOCK_DIST + shift_amount # Adjust to place the barrier at the correct position

                # Get the current frame for the animation and display it
                frame = barrier_frames[(now // 100) % len(barrier_frames)]  # Cycling through animation frames
                screen.blit(frame, (x_pos, 0))

            # now, **auto-push** Finn back outside the full zone
            if left_bound < finn_x < right_bound:
                if finn_x < ice_rect.centerx:
                    finn_x = left_bound
                else:
                    finn_x = right_bound

        # then clamp to screen edges as usual
        UPPER_Y_LIMIT = 160
        finn_x = max(0, min(finn_x, SCREEN_WIDTH  - frame_img.get_width()))
        finn_y = max(UPPER_Y_LIMIT, min(finn_y, SCREEN_HEIGHT - frame_img.get_height()))

        if finn_flash and now - flash_start_time <= flash_duration:
            # Flash: only draw Finn on even-numbered ticks to create blinking
            if (now // 100) % 2 == 0:
                screen.blit(frame_img, (finn_x, finn_y))
        else:
            screen.blit(frame_img, (finn_x, finn_y))
            finn_flash = False

        if finn_slowed:
            # Create a transparent copy of Finn’s frame
            blue_finn = frame_img.copy()

            # Tint the entire Finn sprite blue
            blue_finn.fill((0, 150, 255, 200), special_flags=pygame.BLEND_RGBA_MULT)

            # Draw the tinted Finn on top
            screen.blit(blue_finn, (finn_x, finn_y))
        full_rect   = frame_img.get_rect(topleft=(finn_x, finn_y))
        if game_over:
            full_rect = pygame.Rect(0, 0, 0, 0)  # Dummy rect to avoid crashes
        player_mask = pygame.mask.from_surface(frame_img)

        if finn_blocked:
            # Apply a light blue overlay to Finn when frozen
            if now - freeze_start_time <= freeze_duration:
                blue_finn = frame_img.copy()
                blue_finn.fill((25, 230, 230, 200), special_flags=pygame.BLEND_RGBA_MULT)  # Light blue overlay
                screen.blit(blue_finn, (finn_x, finn_y))

                # Prevent movement and attacking while frozen
                finn_speed = 0  # Prevent movement
                finn_attacking = False  # Prevent attack
            else:
                # Restore movement and attack ability after freeze duration
                finn_blocked = False
                finn_speed = 4  # Restore normal speed
                freeze_start_time = 0
        
        if not finn_blocked:
            moved = False
            new_action = finn_action

        # Phase transitions
        hp_ratio = ice_king.current_health / ice_king.max_health
        if ice_king.current_health <= 0 and ice_king_state != "dying" and not ice_king_fully_defeated:
            ice_king_state = "dying"
            death_start_time = pygame.time.get_ticks()
            explosion_index = 0
            explosion_timer = death_start_time
            ice_flash_start = death_start_time
            ice_flash_duration = 1500
            current_dialogue = None

        elif hp_ratio <= 0.7 and not phase2_started:
            phase2_started = True
            pending_phase = "phase2"
            queue_dialogue(battle_dialogue["phase2"])
            phase_dialogue_active = True

            left_bound = ice_xpos - SPIKE_BLOCK_DIST - 100
            finn_forced_position_x = left_bound - 10

        elif hp_ratio <= 0.4 and not phase3_started:
            phase3_started = True
            pending_phase = "phase3"
            queue_dialogue(battle_dialogue["phase3"])
            phase_dialogue_active = True

            left_bound = ice_xpos - SPIKE_BLOCK_DIST - 100
            finn_forced_position_x = left_bound - 10

        # drive behavior purely by HP
        if not dialogue_is_blocking:
            if ice_king_state != "defeated":  
                if hp_ratio > 0.7:
                    phase1(now)
                elif hp_ratio > 0.4:
                    phase2(now)
                else:
                    phase3_ready = (
                        ice_king_state in ("phase3", "cube_attack") and
                        not dialogue_is_blocking
                    )
                    if phase3_ready:
                        phase3(now)

        # Ice Spike collision detection (pixel-perfect)
        for sp in spikes[:]:
            img, rect = sp.draw(screen)
            # Create mask for spike and check overlap
            spike_mask = pygame.mask.from_surface(img)
            offset = (full_rect.x - rect.x, full_rect.y - rect.y)
            if spike_mask.overlap(player_mask, offset):
                health_bar.takeDamage(1)
                if health_bar.current_health <= 0:
                    
                    game_over = True
                    pygame.mixer.music.stop()
                spikes.remove(sp)

                finn_flash = True
                flash_start_time = pygame.time.get_ticks()

        for emitter in steam_emitters[:]:
            if emitter.update():
                steam_emitters.remove(emitter)
            else:
                emitter.draw(screen)
        
        for crack in ground_cracks[:]:
            if crack.update():
                ground_cracks.remove(crack)
            else:
                crack.draw(screen)

        if ice_king_state == "dying":
            if not fireworks_played:
                fireworks_sound.play()
                fireworks_played = True
            snowballs.clear()
            ice_cubes.clear()
            warnings.clear()
            spikes.clear()
            steam_emitters.clear()
            cube_trails.clear()
        # Animate idle
            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(idle_animation)
                last_update = now

            # Ice King base frame
            boss_img = idle_animation[animation_frame]
            boss_rect = boss_img.get_rect(topleft=(ice_xpos, ice_ypos))

            # Flashing logic: like Finn, show sprite on/off
            if (now // 100) % 2 == 0:
                screen.blit(boss_img, (ice_xpos, ice_ypos))

            # --- Explosion logic ---
            if 'explosion_index' == None:
                explosion_index = 0
                explosion_timer = now

            if now - explosion_timer >= 100:
                explosion_timer = now
                explosion_index = (explosion_index + 1) % len(explosion_frames)  # loop
                explosion_img = explosion_frames[explosion_index]
                explosion_rect = explosion_img.get_rect(center=(ice_xpos + boss_img.get_width() // 2,
                                                                ice_ypos + boss_img.get_height() // 2))
                screen.blit(explosion_img, explosion_rect.topleft)

            else:
                if explosion_index < len(explosion_frames):
                    explosion_img = explosion_frames[explosion_index]
                    explosion_rect = explosion_img.get_rect(center=(ice_xpos + boss_img.get_width() // 2,
                                                                    ice_ypos + boss_img.get_height() // 2))
                    screen.blit(explosion_img, explosion_rect.topleft)

            # End phase
            if now - death_start_time > 3000:
                ice_king_state = "defeated"
                ice_king_fully_defeated = True
                animation_frame = 0
                last_update = now
                explosion_index = None
                explosion_timer = None

        # Update animation frame if defeated
        if ice_king_state == "defeated":
            if ice_ypos < defeated_target_y:
                ice_ypos += defeated_drop_speed
                if ice_ypos > defeated_target_y:
                    ice_ypos = defeated_target_y
            if now - last_update >= frame_cd:
                animation_frame = (animation_frame + 1) % len(defeated_animation)
                last_update = now

        if ice_king_state == "defeated":
            current = defeated_animation
        elif ice_king_state == "dying":
            current = idle_animation  # Explicitly use idle during death phase
        else:
            if ice_king_state in ["idle", "dropping", "vulnerable"]:
                current = idle_animation
            elif ice_king_state in ["attack", "cube_attack"]:
                current = attack_animation
            elif ice_king_state in ["phase2", "phase3"]:
                current = spike_animation
            else:
                current = idle_animation 

        bf = animation_frame % len(current)
        boss_img = current[bf]
        if (
            charging_ice_cube and 
            ice_king_state == "cube_attack" and 
            phase3_started and 
            hp_ratio <= 0.4
        ):
            ice_king_glow.draw(
                screen,
                ice_xpos + boss_img.get_width() // 2 - 55,
                ice_ypos + boss_img.get_height() // 2 + 10
            )
        # Always draw Ice King unless he's in dying or defeated state
        if ice_king_state == "defeated":
            defeated_frame = defeated_animation[animation_frame % len(defeated_animation)]
            screen.blit(defeated_frame, (ice_xpos, ice_ypos))
        
            if not defeat_dialogue_shown:
                queue_dialogue(battle_dialogue["defeat"])
                defeat_dialogue_shown = True

            if not defeat_dialogue_shown:
                queue_dialogue(battle_dialogue["defeat"])
                defeat_dialogue_shown = True

        elif ice_king_state == "dying":
            pass  # Drawing handled elsewhere

        elif ice_king_state == "vulnerable":
            if phase_dialogue_active and dialogue_is_blocking:
            # Show idle animation during dialogue
                if now - last_update >= frame_cd:
                    animation_frame = (animation_frame + 1) % len(idle_animation)
                    last_update = now
                screen.blit(idle_animation[animation_frame], (ice_xpos, ice_ypos))

        else:
            if phase_dialogue_active and dialogue_is_blocking:
            # Animate idle frame smoothly even during dialogue
                if now - last_update >= frame_cd:
                    animation_frame = (animation_frame + 1) % len(idle_animation)
                    last_update = now
                screen.blit(idle_animation[animation_frame], (ice_xpos, ice_ypos))
            else:
                screen.blit(current[bf], (ice_xpos, ice_ypos))

        ice_rect = boss_img.get_rect(topleft=(ice_xpos, ice_ypos))

        # Draw sword swing effect when attacking
        if finn_attacking and finn_action == 4:
            # Choose a suitable frame for the swing (e.g., frame 3 out of 7)
            swing_frame = min(finn_frame, len(slashing_frames) - 1)
            swing_img = slashing_frames[swing_frame]

            # Determine position relative to Finn's current position
            swing_rect = swing_img.get_rect(center=full_rect.center)
            swing_rect.x += 20  # shift effect to the right
            swing_rect.y -= 50  # shift upward slightly

            screen.blit(swing_img, swing_rect.topleft)

        if finn_attacking and finn_action == 4 and finn_frame == 3 and not attack_damage_done:
            sword_rect = full_rect.inflate(50, -150)
            sword_rect.center = full_rect.center
            sword_rect.y -= 20
            
            if sword_rect.colliderect(ice_rect):
                ice_king.take_damage(400)
                sword_hit_sound.play()
                attack_damage_done = True
                ice_king_hit = True
                hit_overlay_start_time = pygame.time.get_ticks()
                hit_start_frame = finn_frame
            
            if 'hit_anim_frame' not in locals():
                hit_anim_frame = 0
        
        if ice_king_hit:
            if now - hit_overlay_start_time <= hit_overlay_duration:  # Red overlay for a set duration (1.5 seconds)
                # Create a red overlay surface that matches Ice King's sprite size
                red_overlay = boss_img.copy()  # Using the same shape as Ice King's sprite
                red_overlay.fill((255, 0, 0, 200), special_flags=pygame.BLEND_RGBA_MULT)  # Apply semi-transparent red color (alpha 150)

                # Apply the red overlay only where Ice King's sprite is present (using mask)
                screen.blit(red_overlay, (ice_xpos, ice_ypos)) 
            
        if 'hit_start_frame' in locals():
            if 'hit_last_update' not in locals():
                hit_last_update = now

            HIT_FRAME_DELAY = 50

            if now - hit_last_update >= HIT_FRAME_DELAY:
                hit_last_update = now
                hit_anim_frame += 1

            if hit_anim_frame < len(hitting_frames):
                hit_img = hitting_frames[hit_anim_frame]
                hit_rect = hit_img.get_rect(center=ice_rect.center)
                hit_rect.x -= 50
                screen.blit(hit_img, hit_rect.topleft)
            else:
                del hit_start_frame
                del hit_anim_frame
                del hit_last_update

        # Update & draw snowballs
        for sb in snowballs[:]:
            sb.update([full_rect])
            if sb.x < 0 and sb.has_collided:
                snowballs.remove(sb)
            else:
                sb.draw(screen)

        # Reflect & draw ice cubes in phase3
        if ice_king_state in ("phase3", "cube_attack"):
            if finn_attacking and finn_action == 4 and finn_frame == 3:
                atk_rect = full_rect.inflate(50, -20)
                atk_rect.x += 25
                atk_rect.y += 10
                cube_targets = [atk_rect]
            else:
                cube_targets = [full_rect]

            # Draw cube trails first (behind the cubes)
            for trail in cube_trails[:]:
                if trail.update():
                    cube_trails.remove(trail)
                else:
                    trail.draw(screen)

            for cb in ice_cubes[:]:
                if cb.returning:
                    cube_trails.append(IceCubeTrail(cb.image, cb.x, cb.y))

                if cb.update(cube_targets, ice_rect, finn_attacking):
                    ice_cubes.remove(cb)
                else:
                    cb.draw(screen)

                    # Draw the clash effect ONCE when triggered
                    if 'clash_start_frame' in locals():
                        CLASH_FRAME_DELAY = 50
                        if now - clash_last_update >= CLASH_FRAME_DELAY:
                            clash_last_update = now
                            clash_anim_frame += 1

                        if clash_anim_frame < len(clashing_frames):
                            clash_img = clashing_frames[clash_anim_frame]
                            clash_rect = clash_img.get_rect(center=cb.rect.center)
                            clash_rect.y -= 5
                            screen.blit(clash_img, clash_rect.topleft)
                        else:
                            del clash_start_frame
                            del clash_anim_frame
                            del clash_last_update
        if current_dialogue:
            draw_dialogue(screen, current_dialogue["speaker"], current_dialogue["line"])
            duration = current_dialogue.get("duration", 999999)
            if pygame.time.get_ticks() - dialogue_start_time >= duration:
                current_dialogue = None

        elif dialogue_queue:
            current_dialogue = dialogue_queue.pop(0)
            dialogue_start_time = pygame.time.get_ticks()

        if defeat_dialogue_shown and not current_dialogue and not dialogue_queue and not defeat_dialogue_finished:
            defeat_dialogue_finished = True
            final_cutscene_active = True
            final_cutscene_shown = False
        
        elif pending_phase:
            if pending_phase == "start_phase1":
                pass
            else:
                ice_king_state = pending_phase  # Only assign real animation states
                animation_frame = 0
                last_update = pygame.time.get_ticks()
                ice_spike_loops = 0

            pending_phase = None
            phase_dialogue_active = False
            finn_forced_position_x = None

            ice_king_hit = False
            hit_overlay_start_time = 0
            if 'hit_start_frame' in locals(): del hit_start_frame
            if 'hit_anim_frame' in locals(): del hit_anim_frame
            if 'hit_last_update' in locals(): del hit_last_update
        # Draw health bars
        ice_king.draw_health_bar(screen)
        health_bar.draw(screen)

        # Draw snowflakes
        for fl in snowflakes:
            fl.update(); fl.draw()

        # Update and draw falling shards
        for shard in falling_shards[:]:
            if shard.update():
                falling_shards.remove(shard)
            else:
                shard.draw(screen)

        # Update and draw falling snowflakes
        for chunk in falling_snow_chunks[:]:
            if chunk.update():
                falling_snow_chunks.remove(chunk)
            else:
                chunk.draw(screen)
        
        for icicle in icicles[:]:
            if icicle.update():
                icicles.remove(icicle)
            else:
                icicle.draw(screen)
        
        for shard in ice_shards[:]:
            if shard.update():
                ice_shards.remove(shard)
            else:
                shard.draw(screen)
        
        if tutorial_active:
        # Stage 0: full-screen image only
            if tutorial_stage == 0:
                screen.blit(tutorial_images[0], (0, 0))

            elif 1 <= tutorial_stage < len(tutorial_images):
                # Background blur
                blur_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                blur_overlay.fill((0, 0, 0, 180))
                screen.blit(blur_overlay, (0, 0))

                # Scale image to a smaller size
                original_img = tutorial_images[tutorial_stage]
                scaled_width = int(SCREEN_WIDTH * 0.6)
                scaled_height = int(SCREEN_HEIGHT * 0.4)
                img = pygame.transform.scale(original_img, (scaled_width, scaled_height))

                # Center it slightly above mid screen
                img_rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
                screen.blit(img, img_rect)

                # Title and text
                title_surf = tutorial_font.render(tutorial_titles[tutorial_stage - 1], True, (255, 255, 255))
                screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))

                # Draw wrapped instructional text below the image
                lines = wrap_text(tutorial_texts[tutorial_stage - 1], text_font, SCREEN_WIDTH - 200)
                text_start_y = img_rect.bottom + 20  # space between image and text

                for i, line in enumerate(lines):
                    line_surf = text_font.render(line, True, (220, 220, 220))
                    screen.blit(
                        line_surf,
                        (SCREEN_WIDTH // 2 - line_surf.get_width() // 2, text_start_y + i * 30)
                    )

                # Click to continue tip
                tip_surf = text_font.render("Click to continue...", True, (180, 180, 180))
                screen.blit(tip_surf, (SCREEN_WIDTH // 2 - tip_surf.get_width() // 2, SCREEN_HEIGHT - 50))
        
            # Ensure tutorial plays first, then dialogue, then fight starts
        if tutorial_active:
            pass  # Still showing tutorial

        if (
            not cutscene_active and
            not tutorial_active and
            not phase1_dialogue_queued and
            not dialogue_queue and
            not current_dialogue
        ):
            queue_dialogue(battle_dialogue["phase1"])
            phase_dialogue_active = True
            phase1_dialogue_queued = True

        elif (
            not tutorial_active and
            phase1_dialogue_queued and
            not dialogue_queue and
            not current_dialogue and
            not fight_started
        ):
            pending_phase = "start_phase1"

        pygame.display.flip()
        clock.tick(FPS)

    return
