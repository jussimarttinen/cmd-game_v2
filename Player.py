from Entity import Entity
from Entities import Bolt
import settings


class Player(Entity):

    def __init__(self, x, y, sprite, direction=(1,0), layer=1):
        super().__init__(x, y, sprite, layer=layer)
        self.direction = direction
        self.speed = settings.player_speed
        self.running_speed = settings.player_running_speed

    # TODO: Implement class

    def update(self):
        pass

    def move(self, dx=0, dy=0, running=False):
        speed = self.running_speed if running else self.speed
        self.direction = (dx, dy)
        self.x += speed*dx*settings.dt
        self.y += speed*dy*settings.dt
    
    def shoot(self):
        bolt = Bolt(self.x, self.y, self.direction, layer=self.layer-1)
        
        return bolt

    

