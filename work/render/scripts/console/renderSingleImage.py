import sys
sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/work/render/scripts/console/")
sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/")
from blender import RenderGeneral


argv = sys.argv
argv = argv[argv.index("--") + 1:]

setID = argv[0]
rotate = argv[1]
nameSeries = argv[2]
cameraID = argv[3]

render = RenderGeneral()
render.renderSingleImage(setID, rotate, nameSeries, cameraID)