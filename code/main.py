from settings import *
from player import *
from sprites import *
from groups import AllSprites

class Game:

    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display\
            .set_mode((window_config['width'], window_config['height']))
        pygame.display.set_caption(window_config['title'])

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        #bullet time
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = bullet_config['cooldown']

        #enemy time
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, enemy_config['timer'])
        self.spawn_positions = []

        #audio
        pygame.mixer.init()
        self.impact_sound = pygame.mixer.Sound(audio['impact'])
        self.game_sound = pygame.mixer.Sound(audio['music'])
        self.shoot_sound = pygame.mixer.Sound(audio['shoot'])
        self.shoot_sound.set_volume(0.4)
        self.impact_sound.set_volume(0.6)
        self.game_sound.set_volume(0.3)
        self.game_sound.play(loops= -1)

        self.load_images(enemy_config['frame_images'])
        self.is_running = True
        self.setup()

    def load_images(self, *path):
        self.bullet_surf = pygame.image.load(bullet_config['image']).convert_alpha()
        self.frames = {}

        for folder, _, files in walk(join(*path)):
            if files:
                file_list = []
                for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder, file)
                    file_list.append(pygame.image.load(full_path).convert_alpha())
                self.frames[folder.split('/')[-1]] = file_list

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            pos = self.gun.rect.center + self.gun.player_direction * bullet_config['distance']
            self.shoot_sound.play()
            Bullet(self.bullet_surf, pos, self.gun.player_direction,
                   (self.all_sprites, self.bullet_sprites))

    def gun_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() - self.shoot_time >= self.cooldown:
                self.can_shoot = True

    def bullet_collisions(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide\
                    (bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def  player_collisions(self):
        if pygame.sprite.spritecollide(self.player,
                                       self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.is_running = False

    def setup(self):
        map = load_pygame(tile_config['map'])
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            GrounSprites((x * tile_config['size'], y * tile_config['size']),
                          image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprites((obj.x, obj.y), obj.image,
                             (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)),
                             self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y),
                                     self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):

        while self.is_running:
            dt = self.clock.tick()/ 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                if event.type == self.enemy_event:
                    Enemy(choice(list(self.frames.values())),
                          choice(self.spawn_positions),
                          (self.all_sprites, self.enemy_sprites),
                          self.player, self.collision_sprites)

            #update
            self.gun_timer()
            self.input()

            #change color
            self.display_surface.fill(window_config['color'])
            self.bullet_collisions()
            self.player_collisions()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()