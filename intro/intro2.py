###########################################
# intro2.py
# Nick Ratti & Kevin Panasiuk
#
# Adding onto the previous example, we are now
# able to resize the window and disable mouse
# input (defaults to on in Panda3D)
###########################################
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        
        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

game = Game()
game.run()