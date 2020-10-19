from gevent_tasks import Task
import uuid


class GeenletTask(Task):
    """
    Own greenlet class for rendering in background
    """

    def __init__(self, func, **kwargs):
        self.taskKey = f'RenderAsync/{ uuid.uuid4() }'
        self.task = Task(self.taskKey, func)

    def getTaskId(self) -> str:
        return self.taskKey

    def __getitem__(self) -> Task:
        return self.task

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

    def append(self, item: RenderGeenlet):
        self._taskList.append(item)

    def remove(self, item: RenderGeenlet):
        self._taskList.remove(item)

    def __repr__(self):
        info = ''
        for greenlet in self._taskList:
            info += str(greenlet) + '\n'
        return info