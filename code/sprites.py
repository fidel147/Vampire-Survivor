from settings import *

class GrounSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprites(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):

    def __init__(self, player, groups):

        self.player = player
        self.distance = gun_config['distance']
        self.player_direction = pygame.Vector2(1, 0)
        super().__init__(groups)

        self.gun_surf = pygame.image.load(gun_config['image']).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction*self.distance)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction*self.distance

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(window_config['width'] / 2, window_config['height'] / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) -90

        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)

        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
class Bullet(pygame.sprite.Sprite):

    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)

        self.speed = bullet_config['speed']
        self.direction = direction
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = bullet_config['lifetime']

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):

    def __init__(self, frames, pos, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        #image
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = enemy_config['animation_speed']

        #rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = enemy_config['speed']

        #death time
        self.death_time = 0
        self.death_duration = enemy_config['death_duration']

    def animation(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def move(self, dt):
        #get direction
        player_pos= pygame.Vector2(self.player.rect.center)
        enemy_pos= pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        #update the rect position
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.hitbox_rect):
                        if direction == 'horizontal':
                            if self.direction.x >0: self.hitbox_rect.right = sprite.rect.left
                            if self.direction.x <0: self.hitbox_rect.left = sprite.rect.right
                        else:
                            if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                            if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animation(dt)
        else:
            self.death_timer()
