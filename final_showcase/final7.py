###########################################
# final7.py
# Nick Ratti & Kevin Panasiuk
#
# Now we'll add a second bear.
# And we'll have them face off
###########################################
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Spotlight, AmbientLight, DirectionalLight
from panda3d.core import Vec4
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.DirectGui import DirectButton


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        # Add lighting
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Load the first bear
        self.bear1 = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.bear1.setScale(0.005, 0.005, 0.005)
        self.bear1.setPos(0, 6, 0)
        self.bear1.loop("walk")
        self.bear1.reparentTo(self.render)

        # Load the second bear
        self.bear2 = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.bear2.setScale(0.005, 0.005, 0.005)
        self.bear2.setPos(0, -6, 0)
        self.bear2.setHpr(180,0,0)
        self.bear2.loop("walk")
        self.bear2.reparentTo(self.render)
        
        

        # Add tasks and UI buttons
        self.taskMgr.add(self.updateBearPositions, "UpdateBearPositions")
        self.createButtons()

        # Flags to toggle camera behavior.
        self.cameraCircling = True
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera in a circle.
    def spinCameraTask(self, task):
        if self.cameraCircling:
            angleDegrees = task.time * 6.0
            angleRadians = angleDegrees * (pi / 180.0)
            self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
            self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    # Define a procedure to make the camera look at the average position of the bears.
    def lookAtPanda(self, task):
        if not self.cameraCircling:
            pos1 = self.bear1.getPos()
            pos2 = self.bear2.getPos()
            avgPos = (pos1 + pos2) / 2
            self.camera.setPos(avgPos.getX() + 10, avgPos.getY() - 10, avgPos.getZ() + 5)
            self.camera.lookAt(avgPos)
        return Task.cont

    # Adjust the sizes of the bears and update their positions accordingly.
    def updateBearPositions(self, task):
        scale1 = self.bear1.getScale().getX()
        scale2 = self.bear2.getScale().getX()
        pos1 = self.bear1.getPos()
        pos2 = self.bear2.getPos()
        

        if scale1 > scale2:
            self.bear1.setPos(pos1.getX(), pos1.getY() - 0.01, pos1.getZ())
            self.bear2.setPos(pos2.getX() ,pos2.getY() - 0.01, pos2.getZ())
        elif scale2 > scale1:
            self.bear1.setPos(pos1.getX() ,pos1.getY() + 0.01, pos1.getZ())
            self.bear2.setPos(pos2.getX(), pos2.getY() + 0.01, pos2.getZ())

        return Task.cont

    # Adjust the scale of a bear.
    def adjustBearSize(self, bear, scaleChange):
        currentScale = bear.getScale().getX()
        newScale = max(0.002, currentScale + scaleChange)
        bear.setScale(newScale, newScale, newScale)

    # Toggle camera behavior between circling and focusing on the bears.
    def toggleCamera(self):
        if self.cameraCircling:
            self.taskMgr.add(self.lookAtPanda, "lookAtPanda")
        else:
            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.cameraCircling = not self.cameraCircling

    # Create buttons for interactivity.
    def createButtons(self):
        DirectButton(text="Bear 1 Bigger", scale=0.05, pos=(-0.8, 0, -0.8),
                     command=self.adjustBearSize, extraArgs=[self.bear1, 0.002])
        DirectButton(text="Bear 1 Smaller", scale=0.05, pos=(-0.8, 0, -0.9),
                     command=self.adjustBearSize, extraArgs=[self.bear1, -0.002])
        DirectButton(text="Bear 2 Bigger", scale=0.05, pos=(0.8, 0, -0.8),
                     command=self.adjustBearSize, extraArgs=[self.bear2, 0.002])
        DirectButton(text="Bear 2 Smaller", scale=0.05, pos=(0.8, 0, -0.9),
                     command=self.adjustBearSize, extraArgs=[self.bear2, -0.002])
        DirectButton(text="Toggle Camera", scale=0.05, pos=(0, 0, -0.95),
                     command=self.toggleCamera)


app = MyApp()
app.run()