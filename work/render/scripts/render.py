import bpy
import math
import os

from work.celery import import_bpy as bpy

scene = bpy.context.scene
bones = bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
bones.rotation_mode = 'XYZ'

scene.frame_start = 1
scene.frame_end = 86

rotate = 0
nameSeries = 0

renderPath = os.path.dirname(os.path.abspath(__file__))
slash = chr(92)

cameraOne = bpy.data.objects["CameraOne"]
cameraTwo = bpy.data.objects["CameraTwo"]

bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# default position
#for x in range(87):
#    bones.rotation_euler = (3, 0, 0)
#    bones.keyframe_insert('rotation_euler', frame=x)

for camera in range(2):
    if camera == 0:
        bpy.context.scene.camera = cameraOne
    elif camera == 1:
        bpy.context.scene.camera = cameraTwo
    for x in range(87):
        rotate = 0
        nameSeries = 0
        bpy.context.scene.frame_set(x)
        while rotate <= 6.2:
            bones.rotation_euler = (rotate, 0, 0)
            bones.keyframe_insert('rotation_euler', frame=x)
            bpy.context.scene.render.filepath = os.path.dirname(renderPath) + slash + 'render' + slash + str(x) + 'reg' + str(nameSeries) + 'camera' + str(camera)
            bpy.ops.render.render(write_still = True)
            rotate += 0.2
            nameSeries += 1

class RenderScripts():

    scene = bpy.context.scene
    bones = bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
    bones.rotation_mode = 'XYZ'

    scene.frame_start = 1
    scene.frame_end = 86

    rotate = 0
    nameSeries = 0

    renderPath = os.path.dirname(os.path.abspath(__file__))
    slash = chr(92)

    cameraOne = bpy.data.objects["CameraOne"]
    cameraTwo = bpy.data.objects["CameraTwo"]

    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    @classmethod
    def setBlendFile(self):
        pass

    @classmethod
    def renderEverySets(self):
        for camera in range(2):
            if camera == 0:
                bpy.context.scene.camera = cameraOne
            elif camera == 1:
                bpy.context.scene.camera = cameraTwo
            for x in range(87):
                rotate = 0
                nameSeries = 0
                bpy.context.scene.frame_set(x)
                while rotate <= 6.2:
                    bones.rotation_euler = (rotate, 0, 0)
                    bones.keyframe_insert('rotation_euler', frame=x)
                    bpy.context.scene.render.filepath = self.__setFilePathAndName(camera)
                    bpy.ops.render.render(write_still = True)
                    rotate += 0.2
                    nameSeries += 1

    @classmethod
    def __setFilePathAndName(self, camera):
        return os.path.dirname(renderPath) 
                + self.slash 
                + 'render' 
                + self.slash 
                + str(x) 
                + 'reg' 
                + str(self.nameSeries) 
                + 'camera' 
                + str(camera)