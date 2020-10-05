import sys
from .bpyModule.blender import RenderGeneral


setID = sys.argv[1]
rotate = sys.argv[2]
nameSeries = sys.argv[3]
cameraID = sys.argv[4]

render = RenderGeneral()
render.renderSingleImage(setID, rotate, nameSeries, cameraID)