import numpy as np
import time
import msvcrt
import logging

import Display
import Entity
from Player import Player
import settings as st

# Author: Jussi Marttinen
# Last updated: 2020/10/03


class Game():


    

    def __init__(self):

        self.display = Display.Display()

        self.player = Player(10,10, np.array([3], dtype=int).reshape(1,1), layer=69)
        #self.object1 = Entity.Entity(0, 10, np.array([1], dtype=int).reshape(1,1), 100)
        #self.object2 = Entity.Entity(100, 20, np.array([2], dtype=int).reshape(1,1), 0)
        self.display.add_objects([self.player])

        logging.basicConfig(filename="logging.log", filemode="w", level=logging.DEBUG)
        self.fps = 60

    def main_loop(self):
        frame = 0
        running = True
        ms_time = lambda: time.time()*1000

        current_time = ms_time()
        logging.info("Started")
        try:
            while running:
                self.display.compose_frame()
                print(self.display)

                self.get_player_input()

                time.sleep(1/self.fps)
                prev_time = current_time
                current_time = ms_time()
                self.dt = current_time - prev_time
                st.dt = self.dt/1000

                logging.info("Frame: {}; FPS: {:.2f}".format(frame,1/st.dt))
                frame += 1

        except Exception as e:
            logging.critical(msg=e, exc_info=1)
            raise e  


    def get_player_input(self, **kwargs):
        plr_speed = st.player_speed
        plr = self.player
        dp = self.display
        running = kwargs.get("running", False)
        keys = {
        224: self.get_player_input,  # special key (in this case means an arrow key)
        
        st.RIGHT: lambda: plr.move(dx=-plr_speed, running=running),  # right arrow
        st.LEFT: lambda: plr.move(dx=plr_speed, running=running),  # left arrow
        st.UP: lambda: plr.move(dy=-plr_speed, running=running),
        st.DOWN: lambda: plr.move(dy=plr_speed, running=running),
        st.SPACE: lambda: dp.add_objects(plr.shoot()),
        st.RUN: lambda: self.get_player_input(running=True)
        #27: self.pause
        }

        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            logging.info("Keypress: {}".format(key))

            return keys.get(key, lambda:None)()


def main():
    game = Game()
    game.main_loop()

if __name__ == "__main__":
    main()