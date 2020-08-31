import importlib
import sys
import os

from work.settings import *


class RenderGeneral():

    def __init__(self, blendFilePath):
        self.bpy = self.__setBlendFile(blendFilePath)
        self.bpy.context.scene.render.film_transparent = True
        self.bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        
        self.renderPath = os.path.dirname(os.path.abspath(__file__))
        self.slash = chr(92)

        self.scene = bpy.context.scene
        self.scene.frame_start = 1
        self.scene.frame_end = 86

        self.bones = bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
        bones.rotation_mode = 'XYZ'

        self.cameras = [ camera for camera in bpy.data.objects if camera.type == 'CAMERA' ]
        
        self.rotate = 0
        self.nameSeries = 0


    @classmethod
    def __setBlendFile(self, blendFile):
        if 'bpy' not in sys.modules:
            self.bpy = importlib.import_module('bpy')
            self.bpy.ops.wm.open_mainfile(blendFile)

            preferences = self.bpy.context.user_preferences.addons['cycles'].preferences
            preferences.compute_device_type = 'CUDA'
            
            self.bpy.context.scene.cycles.device = BLENDER_RENDER
            
            yield sys.modules['bpy']

    @classmethod
    def renderEverySets(self):
        for cameraID in len(self.cameras):
            bpy.context.scene.camera = self.cameras[ cameraID ]
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