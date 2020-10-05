import sys
sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/work/render/scripts/console/")
sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/")
print(sys.path)
from blender import RenderGeneral

argv = sys.argv
argv = argv[argv.index("--") + 1:]

setID = argv[0]
cameraID = argv[1]

render = RenderGeneral()
render.renderSingleSet(setID, cameraID)