from subprocess import call
from work.settings import RENDER_DIR

from abc import ABC, abstractmethod
import uuid

from work.settings import (
    BASE_DIR
)

# Strategy design pattern 

class AbstractRenderStrategy(ABC):
    """
    Render methods for server usage (command line)

    this class just use split scripts from ./console directory
    """

    def __init__(self, blenderFile):
        self.blenderFile = BASE_DIR + '/static/models/' + blenderFile
        self.renderDir = RENDER_DIR + blenderFile[0:-6]
        
        self.slash = chr(92)

    @abstractmethod
    def render(self, *args, **kwargs):
        pass

    class Meta:
        abstract = True


class RenderSingleImage(AbstractRenderStrategy):

    def render(self, setID, rotate, nameSeries, cameraID, resolution=(0,0), renderDir='SingleImages'):
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


class RenderSingleSet(AbstractRenderStrategy):

    def __init__(self, blenderFile):
        AbstractRenderStrategy.__init__(self, blenderFile)
        self.RenderSingleImage = RenderSingleImage(blenderFile)

    def render(self, setID, cameraID, resolution=(0,0), angle=0.2, generalDir=''):
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

        progress = 0 
        while rotate <= 6.2:
            self.RenderSingleImage.render(
                setID, 
                rotate, 
                nameSeries, 
                cameraID, 
                resolution=resolution, 
                renderDir=renderDir
            )
            rotate += angle
            nameSeries += 1
            progress = round(rotate / (6.2 / 100), 2)
            yield progress


class RenderAllSets(AbstractRenderStrategy):

    def __init__(self, blenderFile):
        AbstractRenderStrategy.__init__(self, blenderFile)
        self.RenderSingleSet = RenderSingleSet(blenderFile)

    def render(self, resolution=(0,0), angle=0.2):
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

        generalProgress = 0
        for cameraID in range(2):
            for setID in range(87):
                generalProgress += ((cameraID + 1) * (setID + 1)) / ((2 * 87) / 100)
                for renderSetProgress in self.RenderSingleSet.render(
                    setID, 
                    cameraID, 
                    angle=angle, 
                    resolution=resolution, 
                    generalDir=generalDir
                ):
                    yield {
                        f'set{setID}_camera{cameraID}_percent:': renderSetProgress, 
                        'general_percent': round(generalProgress, 2)
                    }


class RenderSingleImageByVector(AbstractRenderStrategy):

    def render(
        self,
        rotate: float, 
        nameSeries: int, 
        cameraID: int, 
        vectors: dict,
        resolution: tuple=(0,0), 
        renderDir: str='SingleImages', 
    ):
        """
        render single image by parameters:

        `rotate` - value between `0 - 6.2` where `0.2 == 12 deg` && `6.2 == 360 deg`

        `nameSeries` - id of generated image (from current set)

        `cameraID` - id of current camera used to render

        `resolution` - tuple like: `( <width>, <height> )`

            default: (0,0) (blender file render settings)

        `renderDir` - directory order: 
                        
            single images: SingleImages, 
            single sets: Set<setID>_camera<cameraID>_size<width>x<height>
            every sets: AllSets_size<width>x<height>/Set<setID>_camera<cameraID>
        
        `vectors` - dict with tuples with positions of fingers in hand: (example)
            
            {
                'IK_nadgarstek_R': {
                    'head': {
                        'x': 0.1445000171661377, 
                        'y': 0.06353862583637238, 
                        'z': -0.0073097944259643555
                    }, 
                    'tail': {
                        'x': -0.08322930335998535, 
                        'y': 0.06281907856464386, 
                        'z': -0.009127259254455566
                    }
                }, 
                'IK_joint3_R': {},
                'IK_maly_1_R': {},
                'IK_maly_2_R': {},
                'IK_maly_3_R': {},
                'IK_joint4_R': {}, 
                'IK_serdeczny_1_R': {}, 
                'IK_serdeczny_2_R': {}, 
                'IK_serdeczny_3_R': {}, 
                'IK_joint5_R': {}, 
                'IK_srodkowy_1_R': {}, 
                'IK_srodkowy_2_R': {}, 
                'IK_srodkowy_3_R': {}, 
                'IK_joint6_R': {}, 
                'IK_wskazujacy_1_R': {}, 
                'IK_wskazujacy_2_R': {}, 
                'IK_wskazujacy_3_R': {}, 
                'IK_kciuk_0_R': {},
                'IK_kciuk_1_R': {}, 
                'IK_kciuk_2_R': {}
            }

        """
        call(
            [
                "blender", 
                "-b", 
                self.blenderFile, 
                "--python", 
                "work/render/scripts/console/renderSingleImageByVector.py", 
                "--",
                str(rotate),
                str(cameraID),
                str(resolution[0]),
                str(resolution[1]),
                renderDir,
                str(vectors)
            ]
        )


class RenderSingleSetByVector(AbstractRenderStrategy):

    def __init__(self, blenderFile):
        AbstractRenderStrategy.__init__(self, blenderFile)
        self.RenderSingleImage = RenderSingleImageByVector(blenderFile)

    def render(self, cameraID, vectors: dict, resolution=(0,0), angle=0.2, generalDir=''):
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
        uuid_hash = uuid.uuid4()

        if generalDir is '' and resolution[0] is 0 and resolution[1] is 0:
            renderDir = f'Set_vector_{ uuid_hash }_camera{ cameraID }_sizeDefault'
        elif generalDir is '':
            renderDir = f'Set_vector_{ uuid_hash }_camera{ cameraID }_size{ resolution[0] }x{ resolution[1] }'
        else:
            renderDir = generalDir + self.slash + f'Set{ setID }_camera{ cameraID }'

        progress = 0 
        while rotate <= 6.2:
            self.RenderSingleImage.render(
                rotate, 
                nameSeries, 
                cameraID, 
                vectors,
                resolution=resolution, 
                renderDir=renderDir
            )
            rotate += angle
            nameSeries += 1
            progress = round(rotate / (6.2 / 100), 2)
            yield progress