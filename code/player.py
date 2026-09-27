from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):

        super().__init__(groups)
        self.load_images(*player_config['image_path'])
        self.state, self.frames_index = 'down', 0
        self.image = self.frames[self.state][self.frames_index]
        self.rect = self.image.get_frect(center = pos)
        self.collision_sprites = collision_sprites
        self.hitbox_rect = self.rect.inflate(-90, -100)

        #movement
        self.direction = pygame.Vector2()
        self.speed = player_config['speed']
        self.animation_speed = player_config['animation_speed']

    def load_images(self, *path):
        self.frames = {}

        for folder, _, files in walk(join(*path)):
            if files:
                file_list = []
                for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder, file)
                    file_list.append(pygame.image.load(full_path).convert_alpha())
                self.frames[folder.split('/')[-1]] = file_list

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x >0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x <0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        self.direction.x = int(keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d])\
              - int(keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a])

        self.direction.y = int(keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_z]) \
            - int(keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w])
        self.direction = self.direction.normalize() if \
            self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'

        elif self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        #update frames index
        self.frames_index = self.frames_index + \
            self.animation_speed * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frames_index) % \
                                             len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)