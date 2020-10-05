import sys
from .bpyModule.blender import RenderGeneral

setID = sys.argv[1]
cameraID = sys.argv[2]

render = RenderGeneral()
render.renderSingleSet(setID, cameraID)