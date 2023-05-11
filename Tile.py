from Basics import *
import Hero
from livewires import games
import random

BLOCK_RANGE = 64

class Tile(Collidable):
    def __init__(self, row, column, type_of, location, right = 0, bottom = 0):
        self.type = type_of
        image_num = random.randint(1, 4)
        self.row = row
        self.column = column
        super().__init__(image = "Sprites\\Tiles\\" + self.type + "_earth" + str(image_num) + ".png",
                             bottom = bottom,
                             right = right)  
        self.location = location

    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Hero.Hero) and not isinstance(sprite, Tile):
                    side = self.check_side(sprite)
                    if side == "top":
                        sprite.bottom = self.top + 1
                        sprite.stuck["bottom"][0] = True
                        sprite.stuck["bottom"][1] = games.screen.fps/5
                    elif side == "bottom":
                        sprite.top = self.bottom - 1
                        sprite.stuck["top"][0] = True
                        sprite.stuck["top"][1] = games.screen.fps/5
                    elif side == "right":
                        sprite.left = self.right - 1
                        sprite.stuck["left"][0] = True
                        sprite.stuck["left"][1] = games.screen.fps/5
                    else:
                        sprite.right = self.left + 1
                        sprite.stuck["right"][0] = True
                        sprite.stuck["right"][1] = games.screen.fps/5

class BgTile(games.Sprite):
    def __init__(self, type_of, right = 0, bottom = 0):
        self.type = type_of
        image_num = random.randint(1, 4)
        super().__init__(image = games.load_image("Sprites\\Tiles\\" + self.type + "_bg_earth" + str(image_num) + ".png", False),
                             bottom = bottom,
                             right = right)
