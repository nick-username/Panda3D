###########################################
# final6.py
# Nick Ratti & Kevin Panasiuk
#
# Looks nice, but how about we add some interaction?
# We'll add a button to the screen and let it move the camera.
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
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

        # Flag to toggle camera behavior.
        self.cameraCircling = True

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Add an interactive button.
        self.createButton()

    # Define a procedure to move the camera in a circle.
    def spinCameraTask(self, task):
        if self.cameraCircling:
            angleDegrees = task.time * 6.0
            angleRadians = angleDegrees * (pi / 180.0)
            self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
            self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    # Define a procedure to make the camera look at the panda.
    def lookAtPanda(self, task):
        if not self.cameraCircling:
            angleDegrees = task.time * 12.0
            angleRadians = angleDegrees * (pi / 180.0)
            pandaPos = self.pandaActor.getPos()
            self.camera.setPos(
                pandaPos.getX() + 10 * sin(angleRadians),  
                pandaPos.getY() - 10 * cos(angleRadians),  
                pandaPos.getZ() + 5                       
            )
            self.camera.lookAt(pandaPos+(0,0,1))
        return Task.cont

    # Toggle camera behavior between circling and focusing on the panda.
    def toggleCamera(self):
        if self.cameraCircling:
            # Stop circling and focus on the panda.
            self.taskMgr.add(self.lookAtPanda, "lookAtPanda")
        else:
            # Resume circling.
            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.cameraCircling = not self.cameraCircling

    # Create a button to toggle camera behavior.
    def createButton(self):
        button = DirectButton(text=("Toggle Camera"),
                              scale=0.05,
                              pos=(0, 0, -0.9),
                              command=self.toggleCamera)


app = MyApp()
app.run()
