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
        """
        render single image by parameters:

        `setID` - id of generated set

        `rotate` - value between `0 - 6.2` where `0.2 == 12 deg` && `6.2 == 360 deg`

        `nameSeries` - id of generated image (from current set)

        `cameraID` - id of current camera used to render
        """
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
        """
        render single image by parameters:

        `setID` - id of generated set

        `cameraID` - id of current camera used to render
        """
        rotate = 0
        nameSeries = 0
        while rotate <= 6.2:
            self.renderSingleImage(setID, rotate, nameSeries, cameraID)
            rotate += 0.2
            nameSeries += 1

    def renderEverySets(self):
        """
        render all sets from blend file
        """
        for cameraID in range(1):
            for setID in range(87):
                self.renderSingleSet(setID, cameraID)