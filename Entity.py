import numpy as np

import settings

class Entity():

    def __init__(self, x, y, sprite, layer=0):
        """Superclass for any entities used in the game
        
        :param x: the x coordinate of the left corner of the entity
        :type x: int
        :param y: the y coordinate of the left corner of the entity
        :type y: int
        :param sprite: the sprite of the character
        :type sprite: (m * n) numpy array consisting of numbers in displays charset
        :param layer: the layer, on which the sprite will be drawn, defaults to zero
        :type layer: int, optional
        """
        if isinstance(sprite, str):
            sprite = np.array(list(sprite), dtype=int).reshape(1,1)

        self.x = x
        self.y = y
        self.sprite = sprite
        self.layer = layer
        self.deleted = False

    
    def move(self, dx=0, dy=0):
        """Changes the location of the object
        
        :param dx: change in x, defaults to 0
        :type dx: int. optional
        :param dy: change in y, defaults to 0
        :type dy: int, optional
        """
        self.x += dx*settings.dt
        self.y += dy*settings.dt

    def update(self):
        raise NotImplementedError