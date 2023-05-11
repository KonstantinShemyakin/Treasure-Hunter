from math import asin, sqrt, pi
from livewires import games
import Tile

def length(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def remove_char(string, index):
    final = list(string)
    final.pop(index)
    return "".join(final)

class Collidable(games.Sprite):
    def __init__(self, right, bottom, image):
        super().__init__(image = games.load_image(image, False),
                         right = right,
                         bottom = bottom)

    def check_side(self, to_check):
        #angle_actual = (self.y - (self.top - (to_check.bottom - to_check.top)/2))/length(self.x, self.y, self.right + (to_check.right - to_check.left)/2,  self.y - (self.top - (to_check.bottom - to_check.top)/2))
        angle_actual = (Tile.BLOCK_RANGE/2 + (to_check.bottom - to_check.top)/2 - 0.5)/length(Tile.BLOCK_RANGE/2 - 0.5, Tile.BLOCK_RANGE/2 - 0.5, Tile.BLOCK_RANGE - 1 + (to_check.right - to_check.left)/2, (-1)*(to_check.bottom - to_check.top)/2)
        angle_to_check = (self.y - (to_check.bottom + to_check.top)/2)/length(self.x, self.y, (to_check.right + to_check.left)/2, (to_check.bottom + to_check.top)/2)
        if angle_to_check >= (-1)*angle_actual and angle_to_check <= angle_actual:
            if self.x >= to_check.x:
                return "left"
            else:
                return "right"
        else:
            if self.y >= to_check.y:
                return "top"
            else:
                return "bottom"
