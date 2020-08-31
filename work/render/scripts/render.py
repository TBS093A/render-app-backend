import bpy
import math
import os

from work.celery import import_bpy as bpy

# scene = bpy.context.scene
# bones = bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
# bones.rotation_mode = 'XYZ'

# scene.frame_start = 1
# scene.frame_end = 86

# rotate = 0
# nameSeries = 0

# renderPath = os.path.dirname(os.path.abspath(__file__))
# slash = chr(92)

# cameraOne = bpy.data.objects["CameraOne"]
# cameraTwo = bpy.data.objects["CameraTwo"]

# bpy.context.scene.render.film_transparent = True
# bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# for camera in range(2):
#     if camera == 0:
#         bpy.context.scene.camera = cameraOne
#     elif camera == 1:
#         bpy.context.scene.camera = cameraTwo
#     for x in range(87):
#         rotate = 0
#         nameSeries = 0
#         bpy.context.scene.frame_set(x)
#         while rotate <= 6.2:
#             bones.rotation_euler = (rotate, 0, 0)
#             bones.keyframe_insert('rotation_euler', frame=x)
#             bpy.context.scene.render.filepath = os.path.dirname(renderPath) + slash + 'render' + slash + str(x) + 'reg' + str(nameSeries) + 'camera' + str(camera)
#             bpy.ops.render.render(write_still = True)
#             rotate += 0.2
#             nameSeries += 1

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
        for cameraID in range(2):
            if cameraID == 0:
                bpy.context.scene.camera = self.cameraOne
            elif cameraID == 1:
                bpy.context.scene.camera = self.cameraTwo
            for setID in range(87):
                self.renderSingleSet(setID, cameraID)

    @classmethod
    def renderSingleSet(self, setID, cameraID):
        rotate = 0
        nameSeries = 0
        bpy.context.scene.frame_set(setID)
        while rotate <= 6.2:
            self.renderSingleImage(rotate, nameSeries, cameraID)
            rotate += 0.2
            nameSeries += 1

    @classmethod
    def renderSingleImage(self, rotate, nameSeries, cameraID):
        bones.rotation_euler = (rotate, 0, 0)
        bones.keyframe_insert('rotation_euler', frame=x)
        bpy.context.scene.render.filepath = self.__setFilePathAndName(nameSeries, cameraID)
        bpy.ops.render.render(write_still = True)

    @classmethod
    def __setFilePathAndName(self, nameSeries, camera):
        yield os.path.dirname(self.renderPath) 
            + self.slash 
            + 'render' 
            + self.slash 
            + str(x) 
            + 'reg' 
            + str(nameSeries) 
            + 'camera' 
            + str(camera)