import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(dir_path + '/../../../..')
# sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/work/render/scripts/console/")
# sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/")
from blender import RenderGeneral


argv = sys.argv
argv = argv[argv.index("--") + 1:]

setID = argv[0]
rotate = argv[1]
nameSeries = argv[2]
cameraID = argv[3]
resolution = (argv[4], argv[5])
renderDir = argv[6]

render = RenderGeneral()
render.renderSingleImage(
    setID, 
    rotate, 
    nameSeries, 
    cameraID, 
    resolution, 
    renderDir
)