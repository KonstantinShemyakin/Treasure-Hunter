from livewires import games, color
from math import asin, sqrt, pi
import datetime
import random
from Menu import *

games.init(screen_width = 640, screen_height = 1000, fps = 50)

games.pygame.display.set_caption("Treasure hunter")
icon = games.pygame.image.load("Sprites\\Bonus\\bonus1.png")
games.pygame.display.set_icon(icon)

def main():
    random.seed()

    MainMenu = Menu("Treasure Hunter", "Sprites\\Menu\\menu_bg.jpg")

    MainMenu.setup()

    games.screen.background = games.load_image("Sprites\\Menu\\advancement_bg.png")
    games.screen.mainloop()

if __name__ == "__main__":
    main()
