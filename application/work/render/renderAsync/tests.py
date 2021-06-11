from django.test import TestCase

from logging import Logger
from gevent import sleep

from work.render.renderAsync.GreenletTask import *
from work.render.scripts.render import *


class UtilsTestGreenletTask():

    testFile = 'testHand.blend'

    renderSingleImage = RenderSingleImage(testFile)

    angle = 0
    setID = 0
    nameSeries = 0
    cameraID = 0

    def task_1():
        print('testTask')
    
    def task_2(a):
        testList = [x for x in range(a)]
        print(testList)

    def task_3(self):
         self.renderSingleImage.render(self.setID, self.angle, self.nameSeries, self.cameraID, resolution=(50,33))


# class TestGreenletTask(TestCase, UtilsTestGreenletTask):

#     def testTask_1(self):
#         logger = Logger('testTask_1')
#         GT = GreenletTask(self.task_1, logger=logger)
#         GT._start()

#     def testTask_2(self):
#         logger = Logger('testTask_2')
#         GT = GreenletTask(self.task_2, args=(10, ), logger=logger)
#         GT._start()

#     def testTask_3(self):
#         logger = Logger('testTask_3')
#         GT = GreenletTask(self.task_2, args=(20, ), logger=logger)
#         GT._start()

#     def testTask_4(self):
#         logger = Logger('testTask_4')
#         GT = GreenletTask(self.task_3, logger=logger)
#         GT._start()
