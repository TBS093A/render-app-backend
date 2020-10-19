from django.test import TestCase
import os

from subprocess import call

from .render import *


class TestRenderUtils(TestCase):
    
    testFile = 'testHand.blend'

    renderSingleImage = RenderSingleImage(testFile)
    renderSingleSet = RenderSingleSet(testFile)
    renderAllSets = RenderAllSets(testFile)

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

# class TestRenderSingleImage(TestRenderUtils):

#     def testRender_1(self):
#         self.renderSingleImage.render(self.setID, self.angle, self.nameSeries, self.cameraID, resolution=(50,33))

#     pass


# class TestRenderSingleSet(TestRenderUtils):

#     def testRender_1(self):
#         self.renderSingleSet.render(self.setID, self.cameraID, resolution=(50,33))

#     pass


# class TestRenderEverySets(TestRenderUtils):

#     def testRender_1(self):
#         self.renderAllSets.render(resolution=(50,33))

#     pass