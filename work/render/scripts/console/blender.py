import bpy
import sys
import os

from work.settings import (
    MODEL_DIR,
    BPY_DEFAULT_RENDER_FILE,
    BPY_RENDER_DIR,
    BPY_DEVICE,
)

class RenderGeneral():
    """
    Rendering functionality for scripts (blender usage)
    """

    renderPath = BPY_RENDER_DIR
    slash = chr(92)

    bones = bpy.data.collections["Collection3"].all_objects["IKSkeleton"]
    bones.rotation_mode = 'XYZ'

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 86

    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    cameras = [ camera for camera in bpy.data.objects if camera.type == 'CAMERA' ]

    @classmethod
    def renderSingleImage(self, setID, rotate, nameSeries, cameraID, resolution, renderDir):
        """
        render single image by parameters:

        `setID` - id of generated set

        `rotate` - value between `0 - 6.2` where `0.2 == 12 deg` && `6.2 == 360 deg`

        `nameSeries` - id of generated image (from current set)

        `cameraID` - id of current camera used to render
        """
        self.bones.rotation_euler = (float(rotate), 0, 0)
        self.bones.keyframe_insert('rotation_euler', frame=int(setID))

        if int(resolution[0]) is not 0 and int(resolution[1]) is not 0:
            self.scene.render.resolution_x = int(resolution[0])
            self.scene.render.resolution_y = int(resolution[1])
        else:
            resolution = ( 
                self.scene.render.resolution_x,
                self.scene.render.resolution_y
            )
        
        self.scene.render.filepath = self.__setFilePathAndName(renderDir, setID, nameSeries, cameraID, resolution)

        bpy.ops.render.render(write_still = True)

    @classmethod
    def __setFilePathAndName(self, dirPath, setID, nameSeries, cameraID, resolution):
        return os.path.dirname(self.renderPath) + self.slash + 'render' + self.slash + dirPath + self.slash + 'set' + str(setID) + '_reg' + str(nameSeries) + '_camera' + str(cameraID) + '_size' + str(resolution[0]) + 'x' + str(resolution[1])