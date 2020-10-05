from subprocess import call
from work.settings import RENDER_DIR


class AbsoluteRender():
    """
    Render methods for server usage (command line)

    this class just use split scripts from ./console directory
    """

    def __init__(self, blenderFile):
        self.blenderFile = 'static/models/' + blenderFile
        self.renderDir = RENDER_DIR + blenderFile[0:-6]

    def renderSingleImage(self, setID, rotate, nameSeries, cameraID):
        call([
            "blender", 
            "-b", 
            self.blenderFile, 
            "--python", 
            "work/render/scripts/console/renderSingleImage.py", 
            "--",
            str(setID), 
            str(rotate), 
            str(nameSeries), 
            str(cameraID)
        ])

    def renderSingleSet(self, setID, cameraID):
        call([
            "blender",
            "-b",
            self.blenderFile,
            "--python",
            "work/render/scripts/console/renderSingleSet.py",
            "--",
            str(setID),
            str(cameraID)
        ])

    def renderEverySets(self):
        call([
            "blender",
            "-b",
            self.blenderFile,
            "--python",
            "work/render/scripts/console/renderEverySets.py"
        ])