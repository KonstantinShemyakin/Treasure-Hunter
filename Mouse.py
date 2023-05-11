from livewires import games

class Mouse(games.Sprite):
    def __init__(self):
        super().__init__(image = games.load_image("Sprites\\Mouse\\MouseCheck.jpg"),
                         x = games.mouse.x,
                         y = games.mouse.y)
        self.act_image = games.Sprite(image = games.load_image("Sprites\\Mouse\\MouseCursor.bmp"),
                                      top = games.mouse.y - 3,
                                      left = games.mouse.x - 3,
                                      is_collideable = False)
        games.mouse.is_visible = False

    def setup(self):
        games.screen.add(self)
        games.screen.add(self.act_image)

    def destruct(self):
        self.destroy()
        self.act_image.destroy()

    def update(self):
        self.x = games.mouse.x
        self.y = games.mouse.y
        self.act_image.left = games.mouse.x - 3
        self.act_image.top = games.mouse.y - 3

        if self.x < 0:
            self.x = 0
            self.act_image.left = -3
        elif self.x > games.screen.width:
            self.x = games.screen.width
            self.act_image.left = 3
        if self.y < 0:
            self.y = 0
            self.act_image.top = -3
        elif self.y > games.screen.height:
            self.y = games.screen.height
            self.act_image.top = 3
