import Hero
from Game import *
from Location import *
from livewires import games
import random

fire_images = []

class Fire(games.Animation):
    def __init__(self, row, column, game, x, bottom):
        if len(fire_images) == 0:
            for sprite_num in range(1, 17):
                fire_images.append("Sprites\\Fire\\fire" + str(sprite_num) + ".png")
        super().__init__(images = fire_images,
                         x = x,
                         bottom = bottom,
                         repeat_interval = games.screen.fps/10)
        self.game = game
        self.row = row
        self.column = column

    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Hero.Hero):
                    sprite.hp -= 1
                    sprite.take_dmg()
                    self.destroy()
                    self.game.location.tiles[self.row][self.column] = None
        grow = random.randint(0, 200)
        if self.column != self.game.location.x - 1:
            if (self.game.location.tiles[self.row][self.column + 1] == None or isinstance(self.game.location.tiles[self.row][self.column + 1], Bonus)) and grow == 1:
                if self.game.location.tiles[self.row][self.column + 1] != None:
                    self.game.location.tiles[self.row][self.column + 1].destroy()
                self.game.location.tiles[self.row][self.column + 1] = Fire(self.row,
                                                                     self.column + 1,
                                                                     self.game,
                                                                     self.x + BLOCK_RANGE,
                                                                     self.bottom)
                games.screen.add(self.game.location.tiles[self.row][self.column + 1])
        if self.column != 0:
            if (self.game.location.tiles[self.row][self.column - 1] == None or isinstance(self.game.location.tiles[self.row][self.column - 1], Bonus)) and grow == 100:
                if self.game.location.tiles[self.row][self.column - 1] != None:
                    self.game.location.tiles[self.row][self.column - 1].destroy()
                self.game.location.tiles[self.row][self.column - 1] = Fire(self.row,
                                                                     self.column - 1,
                                                                     self.game,
                                                                     self.x - BLOCK_RANGE,
                                                                     self.bottom)
                games.screen.add(self.game.location.tiles[self.row][self.column - 1])

class Bonus(games.Sprite):
    bonus_score = {0:100, 1:200, 2:500}
    
    def __init__(self, row, column, x, bottom, type_of):
        super().__init__(image = games.load_image("Sprites\\Bonus\\bonus" + str(type_of) + ".png"),
                         x = x,
                         bottom = bottom)
        self.score = Bonus.bonus_score[type_of]
        self.row = row
        self.column = column

    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Hero.Hero):
                    sprite.game.score_value += self.score
                    self.destroy()
