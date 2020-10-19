from django.test import TestCase

from work.render.renderAsync.GreenletTask import *


class TestGreenletTask(TestCase):

    def task(self, a):
        return [x for x in range(a)]

    def testTask_1(self):
        GT = GreenletTask(self.task, args=(10, ))
        print(GT)
        GT._start()

    def testTask_2(self):
        GT = GreenletTask(self.task, args=(20, ))
        print(GT)
        GT._start()