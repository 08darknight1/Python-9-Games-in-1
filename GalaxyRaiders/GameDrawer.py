import pygame

class Drawer:
    def __init__(self, window):
        self.objectsList = []
        self.window = window

    def AddObject(self, ObjSurface, PyObject, prioNumber):
        newObj = Object(ObjSurface, PyObject, prioNumber)
        self.objectsList.append(newObj)
        self.objectsList.sort(key=lambda x: x.prio)

    def Draw(self):
        pygame.display.update()

        if len(self.objectsList) > 0:
           for drawings in self.objectsList:
            self.window.blit(drawings.surface, (drawings.PyObject.x, drawings.PyObject.y))

class Object:
    def __init__(self, ObjSurface: pygame.Surface, PyObject: pygame.Rect, prio:int):
        self.surface = ObjSurface
        self.object : pygame.Rect
        self.prio = prio

        if PyObject is None:
            self.PyObject = pygame.Rect(0, 0, ObjSurface.get_width(), ObjSurface.get_height())
        else:
            self.PyObject = PyObject
