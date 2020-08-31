import importlib
import sys
import os

from work.settings import (
    MODEL_DIR,
    BPY_DEFAULT_RENDER_FILE,
    BPY_RENDER_DIR,
    BPY_DEVICE,
)


class RenderGeneral():

    def __init__(self, blendFileName):
        self.bpy = self.__setBlendFile(blendFileName)

        self.scene = self.bpy.context.scene
        
        self.bones = self.bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
        self.bones.rotation_mode = 'XYZ'

        self.scene.frame_start = 1
        self.scene.frame_end = 86

        self.rotate = 0
        self.nameSeries = 0
        
        # self.renderPath = os.path.dirname(os.path.abspath(__file__))
        self.renderPath = BPY_RENDER_DIR
        self.slash = chr(92)

        self.bpy.context.scene.render.film_transparent = True
        self.bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        
        self.cameras = [ camera for camera in self.bpy.data.objects if camera.type == 'CAMERA' ]
        

    @classmethod
    def __setBlendFile(self, blendFile):
        if 'bpy' not in sys.modules:
            bpy = importlib.import_module('bpy')
            bpy.ops.wm.open_mainfile(MODEL_DIR + '/' + blendFile)

            preferences = bpy.context.user_preferences.addons['cycles'].preferences
            preferences.compute_device_type = 'CUDA'
            
            bpy.context.scene.cycles.device = BPY_DEVICE
            
            # return sys.modules['bpy']
            return bpy

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
            self.renderSingleImage(rotate, setID, nameSeries, cameraID)
            rotate += 0.2
            nameSeries += 1

    @classmethod
    def renderSingleImage(self, setID, rotate, nameSeries, cameraID):
        self.bones.rotation_euler = (rotate, 0, 0)
        self.bones.keyframe_insert('rotation_euler', frame=setID)
        bpy.context.scene.render.filepath = self.__setFilePathAndName(setID, nameSeries, cameraID)
        bpy.ops.render.render(write_still = True)

    @classmethod
    def __setFilePathAndName(self, setID, nameSeries, cameraID):
        yield os.path.dirname(self.renderPath) + self.slash + 'render' + self.slash + str(setID) + 'reg' + str(nameSeries) + 'camera' + str(cameraID)