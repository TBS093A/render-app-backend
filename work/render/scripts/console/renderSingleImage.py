import sys
from .bpyModule.blender import RenderGeneral

argv = sys.argv
argv = argv[argv.index("--") + 1:]

setID = argv[0]
rotate = argv[1]
nameSeries = argv[2]
cameraID = argv[3]

render = RenderGeneral()
render.renderSingleImage(setID, rotate, nameSeries, cameraID)