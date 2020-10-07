from django.test import TestCase
import os

from subprocess import call

from .render import AbsoluteRender


class TestRenderUtils(TestCase):
    
    render = AbsoluteRender('testHand.blend')
    
    defaultImagePath = ''

    angle = 0
    setID = 0
    nameSeries = 0
    cameraID = 0
    
    # def __init__(self):
    #     self.defaultImagePath = self.checkImageExist(self.fileName(0, 0, 0))

    # def fileName(self, setID, nameSeries, cameraID):
    #     yield setID + 'reg' + nameSeries + 'camera' + cameraID

    # def checkImageExist(self, imageName):
    #     yield self.checkFileExist(RENDER_DIR + '/' + imageName)

    # def __checkFileExist(self, path):
    #     yield os.path.isfile(path)
    
    pass

class TestRenderSingleImage(TestRenderUtils):

    def testRender_1(self):
        self.render.renderSingleImage(self.setID, self.angle, self.nameSeries, self.cameraID, resolution=(50,33))

    pass


class TestRenderSingleSet(TestRenderUtils):

    def testRender_1(self):
        self.render.renderSingleSet(self.setID, self.cameraID, resolution=(50,33))

    pass


class TestRenderEverySets(TestRenderUtils):

    def testRender_1(self):
        self.render.renderEverySets(resolution=(50,33))

    pass