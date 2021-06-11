import os
import sys
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(dir_path + '/../../../..')
# sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/work/render/scripts/console/")
# sys.path.append("/home/tbs093a/Projects/engineer's work/application/work/")
from blender import RenderGeneral


argv = sys.argv
argv = argv[argv.index("--") + 1:]

rotate = argv[0]
cameraID = argv[1]
resolution = (argv[2], argv[3])
renderDir = argv[4]
vectors = json.loads(argv[5])
uuid = argv[6]

render = RenderGeneral()
render.renderSingleImageByVector(
    rotate, 
    cameraID, 
    resolution, 
    renderDir,
    vectors,
    uuid
)