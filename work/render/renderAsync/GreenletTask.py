from gevent import Greenlet
import greenlet

from gevent_tasks import Task, TaskManager
import uuid


class GreenletTask():
    """
    Own greenlet class for rendering in background
    """

    def __init__(self, func, *args, **kwargs):
        self.taskKey = f'RenderAsync/{ uuid.uuid4() }'
        self.task = Task(self.taskKey, func, args=args, kwargs=kwargs)
        self.taskManager = TaskManager(pool_size=25)
        self.taskManager.add(self.task)

    def getTaskId(self) -> str:
        return self.taskKey

    def getTask(self) -> Task:
        return self.task

    def _start(self):
        self.taskManager.start(self.taskKey)

    def _stop(self, force=False):
        self.taskManager.stop(self.taskKey, force=force)

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