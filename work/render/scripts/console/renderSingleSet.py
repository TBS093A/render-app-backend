import sys
from .bpyModule.blender import RenderGeneral

argv = sys.argv
argv = argv[argv.index("--") + 1:]

setID = argv[0]
cameraID = argv[1]

render = RenderGeneral()
render.renderSingleSet(setID, cameraID)