from Entity import Entity
import settings

class Bolt(Entity):

    def __init__(self, x, y, direction, sprite="4", layer=0):
        super().__init__(x, y, sprite, layer=layer)
        self.speed = settings.bolt_speed
        self.direction = direction

    
    def move(self):
        self.x += self.direction[0]*self.speed*settings.dt
        self.y += self.direction[1]*self.speed*settings.dt

    def update(self):
        """Called every frame"""
        if (0 <= self.x < settings.w_width) & (0 <= self.y < settings.w_height):
            self.move()
        else:
            self.deleted = True