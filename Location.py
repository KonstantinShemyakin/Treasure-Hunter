from Game import *
from Tile import *
from Bonus import *
from livewires import games
import random

class Location:
    def __init__(self, game, size_x, size_y):
        self.camera_top = 360
        self.game = game
        self.x = size_x
        self.y = size_y
        self.bg_tiles = []
        self.tiles = []
        self.bg_image = games.Sprite(image = games.load_image("Sprites\\Tiles\\bg_top.jpg"),
                                     top = 0,
                                     left = 0,
                                     is_collideable = False)
        for i in range(size_y):
            self.tiles.append([])
            for j in range(size_x):
                if i == 0:
                    self.tiles[i].append(Tile(i, j, "top", self))
                else:
                    self.tiles[i].append(Tile(i, j, "bot", self))
        for i in range(size_y):
            self.bg_tiles.append([])
            for j in range(size_x):
                if i == 0:
                    self.bg_tiles[i].append(BgTile("top"))
                else:
                    self.bg_tiles[i].append(BgTile("bot"))
                self.bg_tiles[i][j].is_collideable = False

    def break_block(self, y, x):
        if self.tiles[y][x] != None:
            if isinstance(self.tiles[y][x], Tile):
                if self.tiles[y][x].type == "bot":
                    bonus_type = random.randint(1, 100)
                    self.tiles[y][x].destroy()
                    if bonus_type <= 12:
                        self.tiles[y][x] = Bonus(y, x, (x + 1/2)*BLOCK_RANGE, self.camera_top + (y + 1)*BLOCK_RANGE, 0)
                    elif bonus_type <= 20:
                        self.tiles[y][x] = Bonus(y, x, (x + 1/2)*BLOCK_RANGE, self.camera_top + (y + 1)*BLOCK_RANGE, 1)
                    elif bonus_type <= 25:
                        self.tiles[y][x] = Bonus(y, x, (x + 1/2)*BLOCK_RANGE, self.camera_top + (y + 1)*BLOCK_RANGE, 2)
                    elif bonus_type <= (36 + (self.game.level - 1) * 2) and bonus_type <= 50:
                        self.tiles[y][x] = Fire(y, x, self.game, (x + 1/2)*BLOCK_RANGE, self.camera_top + (y + 1)*BLOCK_RANGE)
                    else:
                        self.tiles[y][x] = None

                    if self.tiles[y][x] != None:
                        games.screen.add(self.tiles[y][x])
                else:
                    self.tiles[y][x].destroy()
                    self.tiles[y][x] = None

    def update(self):
        if not self.game.hero.stuck["bottom"][0]:
            for i in range(len(self.tiles)):
                for j in range(self.x):
                    if self.tiles[i][j] != None:
                        self.tiles[i][j].bottom = self.camera_top + (i + 1)*BLOCK_RANGE
                    self.bg_tiles[i][j].bottom = self.camera_top + (i + 1)*BLOCK_RANGE
                    if self.bg_image != None:
                        self.bg_image.bottom = self.camera_top
        if self.tiles[0][0].top <= BLOCK_RANGE:
            self.del_row()
            self.camera_top = self.tiles[0][0].top
        if self.tiles[-1][0].bottom < games.screen.height:
            self.add_row()
        if self.game.hero.right >= games.screen.width:
            self.game.hero.stuck["right"][0] = True
            self.game.hero.stuck["right"][1] = games.screen.fps/5
        if self.game.hero.left <= 0:
            self.game.hero.stuck["left"][0] = True
            self.game.hero.stuck["left"][1] = games.screen.fps/5

    def add_row(self):
        self.bg_tiles.append([])
        for i in range(self.x):
            self.bg_tiles[-1].append(BgTile("bot", (i + 1)*BLOCK_RANGE, self.camera_top + len(self.bg_tiles)*BLOCK_RANGE))
            self.bg_tiles[-1][i].is_collideable = False
            games.screen.add(self.bg_tiles[-1][i])

        self.tiles.append([])
        for i in range(self.x):
            self.tiles[-1].append(Tile(len(self.tiles) - 1,
                                       i,
                                       "bot",
                                       self,
                                       (i + 1)*BLOCK_RANGE,
                                       self.camera_top + len(self.tiles)*BLOCK_RANGE))
            games.screen.add(self.tiles[-1][i])

        self.game.hero.elevate()
               
    def del_row(self):
        if self.bg_image != None:
            self.bg_image.destroy()
            self.bg_image = None
        
        for i in range(self.x):
            if self.tiles[0][i] != None:
                self.tiles[0][i].destroy()
        self.tiles.pop(0)
        for i in range(len(self.tiles)):
            for j in range(self.x):
                if self.tiles[i][j] != None:
                    self.tiles[i][j].row -= 1

        for i in range(self.x):
            self.bg_tiles[0][i].destroy()
        self.bg_tiles.pop(0)

    def setup(self):
        for i in range(len(self.bg_tiles)):
            for j in range(self.x):
                self.bg_tiles[i][j].right = (j + 1)*BLOCK_RANGE
                self.bg_tiles[i][j].bottom = self.camera_top + (i + 1)*BLOCK_RANGE
                games.screen.add(self.bg_tiles[i][j])

        for i in range(len(self.tiles)):
            for j in range(self.x):
                if self.tiles[i][j] != None:
                    self.tiles[i][j].right = (j + 1)*BLOCK_RANGE
                    self.tiles[i][j].bottom = self.camera_top + (i + 1)*BLOCK_RANGE
                    games.screen.add(self.tiles[i][j])

        games.screen.add(self.bg_image)

    def destruct(self):
        for i in range(len(self.tiles)):
            for j in range(self.x):
                if self.tiles[i][j] != None:
                    self.tiles[i][j].destroy()

        for i in range(len(self.bg_tiles)):
            for j in range(self.x):
                self.bg_tiles[i][j].destroy()
