###########################################
# intro3.py
# Nick Ratti & Kevin Panasiuk
#
# Loading our first model. Shows how to take
# a 3d model and add it to our environment.
# The file extension is not needed when
# getting a file from a path
###########################################
from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        
        self.environment = loader.loadModel("models/environment")
        self.environment.reparentTo(render)

game = Game()
game.run()