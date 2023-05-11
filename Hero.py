from Game import *
from Location import *
from livewires import games

ACS_FALL = 0.5
MAX_VEL = 4

class Hero(games.Animation):
    MAX_HP = 3
    VELOCITY_X = 2
    PR_GO = ["Sprites\\Hero\\char_walk1.bmp",
            "Sprites\\Hero\\char_walk2.bmp",
            "Sprites\\Hero\\char_walk3.bmp"]
    PL_GO = ["Sprites\\Hero\\char_Lwalk1.bmp",
            "Sprites\\Hero\\char_Lwalk2.bmp",
            "Sprites\\Hero\\char_Lwalk3.bmp"]
    PR_STAND = ["Sprites\\Hero\\char_walk2.bmp",
                "Sprites\\Hero\\char_walk3.bmp"]
    PL_STAND = ["Sprites\\Hero\\char_Lwalk2.bmp",
                "Sprites\\Hero\\char_Lwalk3.bmp"]

    def __init__(self, game, right, bottom):
        super().__init__(images = Hero.PR_STAND,
                         right = right,
                         bottom = bottom,
                         repeat_interval = games.screen.fps/5)
        self.hp = Hero.MAX_HP
        self.dig_counter = 0
        self.middle_x = (self.right + self.left)/2
        self.middle_y = (self.bottom + self.top)/2
        self.acs = ACS_FALL
        self.vel_y = 0
        self.direction = "R"
        self.game = game
        self.locked = False
        self.current_sprite = "R_STAND"
        self.stuck = {"top":[False, 0], "right":[False, 0], "bottom":[False, 0], "left":[False, 0]}
        self.health = []
        for hp in range(self.hp):
            self.health.append(games.Sprite(image = games.load_image("Sprites\\Hero\\heart_full.png", False),
                                            top = 0,
                                            right = games.screen.width + ((hp + 1) - self.hp)*(BLOCK_RANGE + 5),
                                            is_collideable = False))

    def take_dmg(self):
        #Maybe add animation
        broken_hp = Hero.MAX_HP - (self.hp + 1)
        self.health[broken_hp].__init__(image = games.load_image("Sprites\\Hero\\heart_empty.png", False),
                                        top = 0,
                                        right = self.health[broken_hp].right,
                                        is_collideable = False)

    def setup(self):
        games.screen.add(self)
        for hp in range(len(self.health)):
            games.screen.add(self.health[hp])

    def update(self):
        if not self.overlapping_sprites:
            for key in self.stuck:
                self.stuck[key][0] = False
                self.stuck[key][1] = 0
        else:
            for key in self.stuck:
                if self.stuck[key][1] <= 0:
                    self.stuck[key][0] = False
                    self.stuck[key][1] = 0
                else:
                    self.stuck[key][1] -= 1
        
        if not self.locked:
            if games.keyboard.is_pressed(games.K_s) and self.stuck["bottom"][0] and self.dig_counter <= 0:
                if self.overlapping_sprites:
                    for sprite in self.overlapping_sprites:
                        if isinstance(sprite, Tile):
                            self.game.location.break_block(sprite.row, sprite.column)
                            self.dig_counter = games.screen.fps
                            break 
            elif self.dig_counter > 0:
                self.dig_counter -= 1

            if self.direction == "R" and self.dx != 0 and self.current_sprite != "R_GO":
                super().__init__(images = Hero.PR_GO,
                             right = self.right,
                             bottom = self.bottom,
                             repeat_interval = games.screen.fps/5)
                self.current_sprite = "R_GO"
            elif self.direction == "R" and self.dx == 0 and self.current_sprite != "R_STAND":
                super().__init__(images = Hero.PR_STAND,
                             right = self.right,
                             bottom = self.bottom,
                             repeat_interval = games.screen.fps/5)
                self.current_sprite = "R_STAND"
                
            if self.direction == "L" and self.dx != 0 and self.current_sprite != "L_GO":
                super().__init__(images = Hero.PL_GO,
                             right = self.right,
                             bottom = self.bottom,
                             repeat_interval = games.screen.fps/5)
                self.current_sprite = "L_GO"
            elif self.direction == "L" and self.dx == 0 and self.current_sprite != "L_STAND":
                super().__init__(images = Hero.PL_STAND,
                             right = self.right,
                             bottom = self.bottom,
                             repeat_interval = games.screen.fps/5)
                self.current_sprite = "L_STAND"

            if not self.stuck["bottom"][0]: 
                if self.vel_y < MAX_VEL:
                    self.vel_y += self.acs
                self.dy = self.vel_y
            else:
                self.vel_y = 0
                self.dy = 0

            if games.keyboard.is_pressed(games.K_d):
                if not self.stuck["right"][0]:
                    self.dx = Hero.VELOCITY_X
                else:
                    self.dx = 0
                self.direction = "R"
            elif self.dx > 0:
                self.dx = 0

            if games.keyboard.is_pressed(games.K_a):
                if not self.stuck["left"][0]:
                    self.dx = (-1)*Hero.VELOCITY_X
                else:
                    self.dx = 0
                self.direction = "L"
            elif self.dx < 0:
                self.dx = 0
