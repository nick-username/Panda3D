###########################################
# intro4.py
# Nick Ratti & Kevin Panasiuk
#
# Moving our camera through code so we can
# navigate our 3D environment however we want
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
        
        self.camera.setPos(100, -270, 55)
        self.camera.setHpr(25, -10, 0)

game = Game()
game.run()