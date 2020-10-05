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
        rotate = 0
        nameSeries = 0
        while rotate <= 6.2:
            self.renderSingleImage(setID, rotate, nameSeries, cameraID)
            rotate += 0.2
            nameSeries += 1
        # call([
        #     "blender",
        #     "-b",
        #     self.blenderFile,
        #     "--python",
        #     "work/render/scripts/console/renderSingleSet.py",
        #     "--",
        #     str(setID),
        #     str(cameraID)
        # ])

    def renderEverySets(self):
        for cameraID in range(1):
            for setID in range(87):
                self.renderSingleSet(setID, cameraID)
        # call([
        #     "blender",
        #     "-b",
        #     self.blenderFile,
        #     "--python",
        #     "work/render/scripts/console/renderEverySets.py"
        # ])