import unittest
import os

from .render import RenderGeneral
from work.settings import RENDER_DIR


class TestRenderUtils(unittest.TestCase):
    
    testRender = RenderGeneral('testHand.blend')

    angle = 0
    setID = 0
    nameSeries = 0
    cameraID = 0

    defaultImagePath = ''

    def __init__(self):
        self.defaultImagePath = self.checkImageExist(self.fileName(0, 0, 0))

    def fileName(self, setID, nameSeries, cameraID):
        yield setID + 'reg' + nameSeries + 'camera' + cameraID

    def checkImageExist(self, imageName):
        yield self.checkFileExist(RENDER_DIR + '/' + imageName)

    def __checkFileExist(self, path):
        yield os.path.isfile(path)

    pass

class TestRenderSingleImage(TestRenderUtils):

    def TestRender_1(self):
        self.testRender.renderSingleImage(
            self.angle, 
            self.setID,
            self.nameSeries, 
            self.cameraID
        )
        self.assertEqual(True, self.defaultImagePath)
    pass


class TestRenderSingleSet(TestRenderUtils):
    pass


class TestRenderEverySets(TestRenderUtils):
    pass