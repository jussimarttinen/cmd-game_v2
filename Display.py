import numpy as np
from collections.abc import Iterable
from shutil import get_terminal_size
from queue import Queue

import Entity
import settings

class Display():

    
    def __init__(self, width=None, height=None, charset=" *#@-", layers=100):
        """Creates an instance of a display object used for displaying the graphics

        :param width: width of display in symbols, if None or 0, will be set to 
            value returned from shutil.get_terminal_size(), defaults to None
        :type width: int, optional
        :param height: height of display in symbols, if None or 0, will be set to 
            value returned from shutil.get_terminal_size(), defaults to None
        :type width: int, optional
        :param charset: contains the characters used for displaying
            the screen. If dict, the keys should be positive integers. 
            param layers (optional, defaults to 100): number of layers the display object has. Simultaneously the max supported amount
            of entities on screen
            The first character (or the value with key 0 if dict) should be a reserved for "dead" pixels
        :type charset: iterable, optional
        """
        w_width, w_height = get_terminal_size()
        
        # 
        self.w_width = width if width else w_width
        self.w_height = height if height else w_height
        settings.w_width = self.w_width
        settings.w_height = self.w_height

        self.layers = layers
        self.shape = (self.w_width, self.w_height, self.layers)

        if isinstance(charset, dict):
            self.charset = charset
        elif isinstance(charset, Iterable):
            self.charset = dict(zip(range(len(charset)), charset))    
        else:
            raise ValueError("Invalid type for parameter 'charset'.")
        
        inv_charset = dict(zip(self.charset.values(), self.charset.keys()))
        # creates a placeholder (empty) frame
        #self.frame = np.zeros(self.shape, dtype=int)
        
        self.buffer = Queue(0)
        
        self.objects = []


    def add_objects(self, added):
        """Adds objects to the objects of the display

        :param added: objects to be added to the display
        :type added: iterable of items of type Entity or its subclasses
        :raises ValueError: if any objects of invalid type
        """
        if isinstance(added, Entity.Entity):
            self.objects.append(added)

        elif all(map(lambda x: isinstance(x, Entity.Entity), added)):
            self.objects.extend(added)
        else:
            raise ValueError("All elements of 'objects' must be instances of class Entity")
    
    def remove_objects(self, removed):
        """Removes objects from the display

        :param removed: objects to be added to the display
        :type removed: iterable of items of type Entity or its subclasses
        :raises ValueError: if any objects of invalid type
        """
        if isinstance(removed, Entity.Entity):
            self.objects.remove(removed)

        elif all(map(lambda x: isinstance(x, Entity.Entity), removed)):
            self.objects = [x for x in self.objects if x not in removed]
        else:
            raise ValueError("All elements of 'objects' must be instances of class Entity")
        
    def compose_frame(self, *args):
        """Composes frame from objects the frame contains and adds it to the buffer
        :*args: arguments for the buffer, optional
        """

        frame = np.zeros(self.shape, dtype=int)

        for ent in self.objects:
            # taken from https://stackoverflow.com/a/53124171
            # sets the area of the given layer of display to the sprite
            if ent.deleted:
                self.objects.remove(ent)
            else:
                ent.update()
                frame[int(ent.x) : int(ent.x)+ent.sprite.shape[0],
                int(ent.y) : int(ent.y)+ent.sprite.shape[1], min(ent.layer, self.layers-1)] = ent.sprite
        
        self.buffer.put(frame, *args)

    def display_picture(self, *args):
        """Turns display into a printable picture
        
        :*args: arguments for the buffer, optional
        :returns: frame object
        :rtype: (w_height * w_width) numpy array
        """

        # gets the next item in the buffer
        frame = self.buffer.get(*args)
        
        displayed = np.zeros(self.shape[0:2], dtype=int)
        
        # loops
        for i in range(self.shape[2]):
            L = frame[:,:,i]
            displayed[L != 0] = L[L != 0]

        return np.vectorize(self.charset.get)(displayed).T

    def __str__(self):
        # the frame contains lots of ascii null characters for some reason
        # which causes problems on command line
        return self.display_picture().tobytes().decode("utf-8").replace("\x00", "")


def main():
    np.set_printoptions(threshold=np.inf)
    display = Display(*get_terminal_size())
    ent = Entity.Entity(10, 8, np.array([1]*10).reshape(5,2))
    display.add_objects([ent])
    
    display.compose_frame()
    f = str(display)
    print(f)
    input()

if __name__ == "__main__":
    main()