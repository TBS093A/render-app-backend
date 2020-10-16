from gevent import Greenlet
import gevent


class RenderGeenlet(Greenlet):

    def __init__(self, func, **kwargs):
        Greenlet.__init__(self)
        self.thread = Greenlet.spawn(func, **kwargs)


class GreenletSingleton():

    _greenletList = []

    def __getitem__(self, position):
        return self._greenletList[position]

    def append(self, item: RenderGeenlet):
        self._greenletList.append(item)

    def remove(self, item: RenderGeenlet):
        self._greenletList.remove(item)

    def __repr__(self):
        info = ''
        for greenlet in self._greenletList:
            info += '{:>15} | {:>15} | {:>15} | {:>15}'.format(
                greenlet,
                str(greenlet.started()), 
                str(greenlet.ready()),
                str(greenlet.successful())    
            )
        return info