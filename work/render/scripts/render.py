from subprocess import call
from work.settings import RENDER_DIR


class AbsoluteRender():
    """
    Render methods for server usage (command line)

    Use split script with subprocess
    """

    def __init__(self, blenderFile):
        self.blenderFile = './../../../static/models/' + blenderFile
        self.renderDir = RENDER_DIR + blenderFile[0:-6]

    def renderSingleImage(self, setID, rotate, nameSeries, cameraID):
        call(
            "blender", 
            "-b", 
            self.blenderFile, 
            "--python", 
            "./console/renderSingleImage.py", 
            setID, 
            rotate, 
            nameSeries, 
            cameraID
        )

    def renderSingleSet(self, setID, cameraID):
        call(
            "blender",
            "-b",
            self.blenderFile,
            "--python",
            "./console/renderSingleSet.py",
            setID,
            cameraID
        )

    def renderEverySets(self):
        call(
            "blender",
            "-b",
            self.blenderFile,
            "--python",
            "./console/renderEverySets.py"
        )