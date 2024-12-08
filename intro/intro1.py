###########################################
# intro1.py
# Nick Ratti & Kevin Panasiuk
#
# This file is the intro to Panda3d, and contains
# the absolute basics of how to create a
# blank window in Panda3d
###########################################
from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

game = Game()
game.run()
