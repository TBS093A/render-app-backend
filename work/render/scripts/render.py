from subprocess import call
from work.settings import RENDER_DIR

from celery import Task

class AbsoluteRender(Task):
    """
    Render methods for server usage (command line)

    this class just use split scripts from ./console directory
    """

    def __init__(self, blenderFile):
        self.blenderFile = 'static/models/' + blenderFile
        self.renderDir = RENDER_DIR + blenderFile[0:-6]

        self.slash = chr(92)

    def renderSingleImage(self, setID, rotate, nameSeries, cameraID, resolution=(0,0), renderDir='SingleImages'):
        """
        render single image by parameters:

        `setID` - id of generated set

        `rotate` - value between `0 - 6.2` where `0.2 == 12 deg` && `6.2 == 360 deg`

        `nameSeries` - id of generated image (from current set)

        `cameraID` - id of current camera used to render

        `resolution` - tuple like: `( <width>, <height> )`

            default: (0,0) (blender file render settings)

        `renderDir` - directory order: 
                        
            single images: SingleImages, 
            single sets: Set<setID>_camera<cameraID>_size<width>x<height>
            every sets: AllSets_size<width>x<height>/Set<setID>_camera<cameraID>
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
            str(cameraID),
            str(resolution[0]),
            str(resolution[1]),
            renderDir
        ])

    def renderSingleSet(self, setID, cameraID, resolution=(0,0), angle=0.2, generalDir=''):
        """
        render single image by parameters:

        `setID` - id of generated set

        `cameraID` - id of current camera used to render

        `resolution` - tuple like: `( <width>, <height> )`

            default: (0,0) (blender file render settings)

        `angle` - value between `0 - 6.2` (`0 - 360`) 
            
            default: 0.2

        `generalDir` - for all sets rendering directory order

            default: ''
        """
        rotate = 0
        nameSeries = 0
        renderDir = ''

        if generalDir is '' and resolution[0] is 0 and resolution[1] is 0:
            renderDir = f'Set{ setID }_camera{ cameraID }_sizeDefault'
        elif generalDir is '':
            renderDir = f'Set{ setID }_camera{ cameraID }_size{ resolution[0] }x{ resolution[1] }'
        else:
            renderDir = generalDir + self.slash + f'Set{ setID }_camera{ cameraID }'

        while rotate <= 6.2:
            self.renderSingleImage(setID, rotate, nameSeries, cameraID, resolution=resolution, renderDir=renderDir)
            rotate += angle
            nameSeries += 1

    def renderEverySets(self, resolution=(0,0), angle=0.2):
        """
        render all sets from blend file

        `resolution` - tuple like: `( <width>, <height> )`

            default: (0,0) (blender file render settings)

        `angle` - value between `0 - 6.2` (`0 - 360`) 
            
            default: 0.2
        """
        if resolution[0] is 0 and resolution[1] is 0:
            generalDir = f'AllSets_sizeDefault'
        else:
            generalDir = f'AllSets_size{ resolution[0] }x{ resolution[1] }'
        for cameraID in range(1):
            for setID in range(87):
                self.renderSingleSet(setID, cameraID, angle=angle, resolution=resolution, generalDir=generalDir)