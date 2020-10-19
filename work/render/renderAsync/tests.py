from django.test import TestCase

from work.render.renderAsync.GreenletTask import *


class UtilsTestGreenletTask():

    def task_1(a):
        testList = [x for x in range(a)]
        print(testList)

    def task_2():
        print('testTask')


class TestGreenletTask(TestCase, UtilsTestGreenletTask):

    def testTask_1(self):
        GT = GreenletTask(self.task_1, args=(10, ))
        GT._start()

    def testTask_2(self):
        GT = GreenletTask(self.task_1, args=(20, ))
        GT._start()

    def testTask_3(self):
        GT = GreenletTask(self.task_2)
        GT._start()
