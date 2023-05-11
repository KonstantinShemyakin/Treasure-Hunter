from Game import *

class Menu:
    def __init__(self, title, bg_image):
        self.Title = games.Text(value = str(title),
                                size = 60,
                                x = games.screen.width/2,
                                y = 300,
                                color = color.red)
        self.bg_image = games.Sprite(image = games.load_image(bg_image, False),
                                     top = 0,
                                     left = 0,
                                     is_collideable = False)
        self.game = None
        self.buttons = []
        self.buttons.append(Button(self.start_game, games.screen.width/2, 440, NEWGAME))
        self.buttons.append(Button(self.open_leaderboard, games.screen.width/2, 590, LEADERTABLE))
        self.buttons.append(Button(self.quit_game, games.screen.width/2, 730, EXIT))

    def destruct(self):
        self.Title.destroy()
        self.bg_image.destroy()
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()

    def setup(self):
        self.game = None
        games.screen.add(self.bg_image)
        games.screen.add(self.Title)
        for i in range(len(self.buttons)):
            games.screen.add(self.buttons[i])
        Mouse().setup()

    def set_name(self):
        games.screen.clear()
        SetName(self.game, self).setup()

    def start_game(self):
        self.game = Game(self)
        self.set_name()

    def quit_game(self):
        games.screen.quit()

    def open_leaderboard(self):
        LeaderBoard(self).setup()

class SetName(games.Sprite):
    keys = {games.K_q:"q", games.K_w:"w", games.K_e:"e", games.K_r:"r", games.K_t:"t", games.K_y:"y",
            games.K_u:"u", games.K_i:"i", games.K_o:"o", games.K_p:"p", games.K_a:"a", games.K_s:"s",
            games.K_d:"d", games.K_f:"f", games.K_g:"g", games.K_h:"h", games.K_j:"j", games.K_k:"k",
            games.K_l:"l", games.K_z:"z", games.K_x:"x", games.K_c:"c", games.K_v:"v", games.K_b:"b",
            games.K_n:"n", games.K_m:"m", games.K_1:"1", games.K_2:"2", games.K_3:"3", games.K_4:"4",
            games.K_5:"5", games.K_6:"6", games.K_7:"7", games.K_8:"8", games.K_9:"9", games.K_0:"0",
            games.K_SPACE:" "}

    def __init__(self, game, menu):
        super().__init__(image = games.load_image("Sprites\\Menu\\advancement_bg.png"),
                         top = 0,
                         left = 0,
                         is_collideable = False)
        self.NameText = games.Text(value = "",
                                   size = 50,
                                   x = games.screen.width/2,
                                   y = 450,
                                   color = color.white)
        self.pressed = [False, 0]
        self.game = game
        self.menu = menu

    def setup(self):
        games.screen.add(self)
        games.screen.add(self.NameText)
        games.screen.add(games.Text(value = "Введите ваше имя:",
                                    size = 50,
                                    x = games.screen.width/2,
                                    y = 350,
                                    color = color.white))
        games.screen.add(Button(self.start_game, 500, 600, ARROWR))
        games.screen.add(Button(self.go_to_menu, 140, 600, ARROWL))
        Mouse().setup()

    def start_game(self):
        self.game.play(self.NameText.value)

    def go_to_menu(self):
        games.screen.clear()
        self.menu.setup()
        
    def update(self):
        for key in SetName.keys:
            if games.keyboard.is_pressed(key):
                if self.pressed[1] == key:
                    if not self.pressed[0]:
                        self.NameText.value += SetName.keys[key]
                        self.pressed[0] = True
                elif not self.pressed[0]:
                    self.NameText.value += SetName.keys[key]
                    self.pressed[1] = key
                    self.pressed[0] = True
            elif self.pressed[1] == key:
                self.pressed[0] = False
        if games.keyboard.is_pressed(games.K_BACKSPACE):
            if self.NameText.value != "" and not self.pressed[0]:
                self.NameText.value = remove_char(self.NameText.value, -1)
                self.pressed[1] = games.K_BACKSPACE
                self.pressed[0] = True  
        elif self.pressed[1] == games.K_BACKSPACE:
            self.pressed[0] = False

class LeaderBoard:
    def __init__(self, menu):
        self.saves = json.load(open("saves.json"))
        self.bg_image = games.Sprite(image = games.load_image("Sprites\\Menu\\menu_bg.jpg"),
                                     top = 0,
                                     left = 0,
                                     is_collideable = False)
        self.heroes = []
        self.menu = menu
        for i in range(10):
            self.heroes.append(games.Text(value = f"{i + 1}.--------------",
                                          color = color.black,
                                          left = 30,
                                          top = i * 70 + 50,
                                          size = 40))
        heros = list(self.saves.keys())
        element = None
        for i in range(len(heros)):
            for j in range(len(heros) - 1):
                if self.saves[heros[j]] < self.saves[heros[j + 1]]:
                    element = heros[j]
                    heros[j] = heros[j + 1]
                    heros[j + 1] = element
        if len(heros) < 10:
            for i in range(len(heros)):
                self.heroes[i].value = f"{i + 1}.{heros[i]}:{self.saves[heros[i]]} уровень"
                self.heroes[i].left = 30
        else:
            for i in range(10):
                self.heroes[i].value = f"{i + 1}.{heros[i]}:{self.saves[heros[i]]} уровень"
                self.heroes[i].left = 30

    def setup(self):
        games.screen.add(self.bg_image)
        for i in range(len(self.heroes)):
            games.screen.add(self.heroes[i])
        games.screen.add(Button(self.go_to_menu, 100, 900, ARROWL))
        Mouse().setup()

    def go_to_menu(self):
        games.screen.clear()
        self.menu.setup()
                
