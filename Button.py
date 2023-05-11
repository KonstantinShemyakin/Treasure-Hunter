from livewires import games
import Mouse

EXIT = ["Sprites\\Buttons\\Exit_Main.png",
         "Sprites\\Buttons\\Exit_Alter.png",
         "Sprites\\Buttons\\Exit_Pushed.png"]
MAINMENU = ["Sprites\\Buttons\\MainMenu_Main.png",
             "Sprites\\Buttons\\MainMenu_Alter.png",
             "Sprites\\Buttons\\MainMenu_Pushed.png"]
LEADERTABLE = ["Sprites\\Buttons\\Leader_Main.png",
                "Sprites\\Buttons\\Leader_Alter.png",
                "Sprites\\Buttons\\Leader_Pushed.png"]
NEWGAME = ["Sprites\\Buttons\\NewGame_Main.png",
            "Sprites\\Buttons\\NewGame_Alter.png",
            "Sprites\\Buttons\\NewGame_Pushed.png"]
ARROWL = ["Sprites\\Buttons\\ArrowL_Main.png",
           "Sprites\\Buttons\\ArrowL_Alter.png",
           "Sprites\\Buttons\\ArrowL_Pushed.png"]
ARROWR = ["Sprites\\Buttons\\ArrowR_Main.png",
           "Sprites\\Buttons\\ArrowR_Alter.png",
           "Sprites\\Buttons\\ArrowR_Pushed.png"]
TRYAGAIN = ["Sprites\\Buttons\\TryAgain_Main.png",
             "Sprites\\Buttons\\TryAgain_Alter.png",
             "Sprites\\Buttons\\TryAgain_Pushed.png"]

class Button(games.Sprite):
    def __init__(self, function, x, y, images):
        self.images = []
        for image in images:
            self.images.append(games.load_image(image, False))
        self.function = function
        super().__init__(image = self.images[0],
                         x = x,
                         y = y)
        self.current_image = "Main"

    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Mouse.Mouse):
                    if games.mouse.is_pressed(0):
                        if self.current_image != "Pushed":
                            self.current_image = "Pushed"
                            self.set_image(self.images[2])
                    else:
                        if self.current_image != "Alter":
                            if self.current_image == "Pushed":
                                self.function()
                            self.current_image = "Alter"
                            self.set_image(self.images[1])
        elif self.current_image != "Main":
            self.current_image = "Main"
            self.set_image(self.images[0])
