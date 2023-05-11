import Hero
from Location import *
from Button import *
from Mouse import *
from Menu import *
from livewires import games, color
import json

class AdvanceLabel(games.Sprite):
    IMAGE = "Sprites\\Menu\\advancement_bg.png"
    
    def __init__(self, game, level, score):
        super().__init__(image = games.load_image(AdvanceLabel.IMAGE),
                       left = 0,
                       top = 0)
        self.game = game
        self.level = games.Message(value = "Уровень " + str(level),
                                   size = 40,
                                   color = color.white,
                                   x = 320,
                                   y = 450,
                                   lifetime = 4 * games.screen.fps,
                                   after_death = self.destruct)
        self.score = games.Text(value = "Цель: " + str(score) + " очков",
                                size = 40,
                                color = color.white,
                                x = 320,
                                y = 550)
    def setup(self):
        games.screen.add(self.level)
        games.screen.add(self.score)

    def destruct(self):
        self.game.setup()
        self.score.destroy()
        self.destroy()

class Game(games.Sprite):
    def __init__(self, menu):
        super().__init__(image = games.load_image("Sprites\\Menu\\advancement_bg.png"),
                         top = 0,
                         left = 0)
        self.score_value = 0
        self.score_text = games.Text(value = "Очки:" + str(self.score_value),
                                     size = 40,
                                     color = color.green,
                                     left = 10,
                                     top = 10)
        self.camera_lock = False
        self.lock_place = 0
        self.level = 0
        self.goal = 0
        self.location = None
        self.hero = None
        self.center_x = games.screen.width/2
        self.center_y = games.screen.height/2
        self.name = None
        self.menu = menu
        self.die_counter = 0

    def play(self, name):
        self.name = name
        self.hero = Hero.Hero(self, 320, 300)
        games.screen.clear()
        self.advance()

    def setup(self):
        games.screen.add(self)    
        self.location.setup()
        self.hero.setup()
        games.screen.add(self.score_text)
        
    def advance(self):
        self.level += 1

        self.score_value = 0
        self.goal = 500 + 200 * (self.level - 1)

        self.lock_place = 0
        self.camera_lock = False

        label = AdvanceLabel(self, self.level, self.goal)
        games.screen.add(label)
        label.setup()

        if self.location != None:
            self.location.destruct()

        self.location = Location(self, 10, 10)

    def end(self):
        self.hero.locked = True
        games.screen.clear()
        games.screen.add(self)
        games.screen.add(self.hero)
        vel_x = (self.center_x - self.hero.x)/(games.screen.fps * 2)
        vel_y = (self.center_y - self.hero.y)/(games.screen.fps * 2)
        self.hero.dx = vel_x
        self.hero.dy = vel_y

        write_file = open("saves.json")
        saves = json.load(write_file)
        if self.name not in saves:
            saves[self.name] = self.level
        elif saves[self.name] < self.level:
            saves[self.name] = self.level
        write_file = open("saves.json", "w")
        json.dump(saves, write_file)

    def set_end_menu(self):
        self.destroy()
        music = random.randint(1, 3)
        music = games.load_sound("Music\\Death" + str(music) + ".wav")
        games.screen.add(games.Text(value = f"Вы достигли:{self.level} уровня",
                                            x = self.center_x,
                                            y = 400,
                                            color = color.white,
                                            size = 40))
        games.screen.add(games.Text(value = f"Вы не будете забыты:{self.name}",
                                    x = self.center_x,
                                    y = self.hero.bottom + 40,
                                    color = color.white,
                                    size = 40))
        games.screen.add(Button(self.restart, self.center_x, 700, TRYAGAIN))
        games.screen.add(Button(self.go_to_menu, self.center_x, 850, MAINMENU))
        Mouse().setup()
        music.play()

    def restart(self):
        name = self.name
        self.__init__(self.menu)
        self.play(name)

    def go_to_menu(self):
        games.screen.clear()
        self.menu.setup()

    def update(self):
        if not self.hero.locked:
            self.location.update()

            self.score_text.value = "Очки:" + str(self.score_value)
            self.score_text.left = 10
            self.score_text.top = 10

            if self.hero.hp <= 0:
                self.end()

            if self.hero.y >= games.screen.height/2 and not self.camera_lock:
                self.camera_lock = True
                self.lock_place = self.hero.y

            if self.camera_lock and not self.hero.stuck["bottom"][0]:
                delta = self.hero.y - self.lock_place
                self.location.camera_top -= delta
                self.hero.y = self.lock_place

            if self.score_value >= self.goal:
                self.play(self.name)
        else:
            if self.hero.x <= self.center_x + 4 and self.hero.x >= self.center_x - 4 and self.hero.y <= self.center_y + 4 and self.hero.y >= self.center_y - 4:
                self.hero.x = self.center_x
                self.hero.y = self.center_y
                self.hero.dx = 0
                self.hero.dy = 0
                games.screen.add(games.Text(value = "Вы погибли",
                                            x = self.center_x,
                                            y = 360,
                                            color = color.red,
                                            size = 60))
                if self.die_counter >= games.screen.fps * 2:
                    self.hero.destroy()
                    games.screen.add(games.Sprite(image = games.load_image(Hero.Hero.PR_STAND[-1]),
                                                  x = self.center_x,
                                                  y = self.center_y))
                    self.set_end_menu()
                else:
                    self.die_counter += 1
