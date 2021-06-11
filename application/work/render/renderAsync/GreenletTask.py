from gevent import Greenlet
import greenlet

from gevent_tasks import Task, TaskManager
import uuid


class GreenletTask():
    """
    Own greenlet class for rendering in background
    """

    def __init__(self, func, logger=None, *args, **kwargs):
        self.taskKey = f'RenderAsync/{ uuid.uuid4() }'
        self.task = Task(self.taskKey, func, args=args, kwargs=kwargs, logger=logger)
        self.taskManager = TaskManager()
        self.taskManager.add(self.task, start=True)

    def getTaskId(self) -> str:
        return self.taskKey

    def getTask(self) -> Task:
        return self.task

    def getValue(self):
        return self.task.value()

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

    def _start(self, taskKey):
        for task in self._taskList:
            if task.taskKey is taskKey:
                task._start()

    def _stop(self, taskKey, force=False):
        for task in self._taskList:
            if task.taskKey is taskKey:
                task._stop(force=force)

    def _startAll(self):
        for task in self._taskList:
            task._start()

    def _stopAll(self, force=False):
        for task in self._taskList:
            task._stop(force=force)

    def __repr__(self):
        info = ''
        for greenlet in self._taskList:
            info += str(greenlet) + '\n'
        return info