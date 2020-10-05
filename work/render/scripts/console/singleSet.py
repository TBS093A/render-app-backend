import sys
from work.render.scripts.render import RenderGeneral

setID = sys.argv[1]
cameraID = sys.argv[2]

render = RenderGeneral()
render.renderSingleSet(setID, cameraID)