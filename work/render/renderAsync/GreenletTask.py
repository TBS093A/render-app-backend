from gevent import Greenlet
import greenlet

from gevent_tasks import Task
import uuid

class GreenletTask(Task):
    """
    Own greenlet class for rendering in background
    """

    def __init__(self, func, **kwargs):
        self.taskKey = f'RenderAsync/{ uuid.uuid4() }'
        self.task = Task(self.taskKey, func, kwargs=kwargs)

    def getTaskId(self) -> str:
        return self.taskKey

    def getTask(self) -> Task:
        return self.task

    def _start(self):
        self.task.start()

    def _stop(self):
        self.task.stop()

    def __repr__(self) -> str:
        return str(self.task)


# Singleton design pattern

class GreenletTaskManager():
    """
    Global class for storage all running threads / greenlets
    """

    _taskList = []

    def __getitem__(self, position):
        return self._taskList[position]

    def append(self, item: GreenletTask):
        self._taskList.append(item)

    def remove(self, item: GreenletTask):
        self._taskList.remove(item)

    def __repr__(self):
        info = ''
        for greenlet in self._taskList:
            info += str(greenlet) + '\n'
        return info