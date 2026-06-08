import pygame

class Drawer:
    def __init__(self, window):
        self.objectsList = []
        self.window = window

    def AddObject(self, ObjName, ObjType, PyObject, ObjSurface, PosX, PosY, prioNumber):
        newObj = ObjectToDraw(ObjName, ObjType, PyObject, ObjSurface, PosX, PosY, prioNumber)
        self.objectsList.append(newObj)
        self.objectsList.sort(key=lambda x: x.prio)

    def ChangeObject(self, objName, changeIndex, change):
        for objects in self.objectsList:
            if objects.name == objName:
                if changeIndex == 0:
                    objects.name = change
                elif changeIndex == 1:
                    objects.PyObject = change
                elif changeIndex == 2:
                    objects.surface = change
                elif changeIndex == 3:
                    objects.PosX = change
                elif changeIndex == 4:
                    objects.PosY = change
                elif changeIndex == 5:
                    myOldValue = objects.prio

                    for objects2 in self.objectsList:
                        if objects2.prio == change:
                            objects2.prio = myOldValue
                            objects.prio = change
                            break

    def Draw(self):
        pygame.display.update()
        if len(self.objectsList) > 0:
           for drawings in self.objectsList:
               if drawings.type == "Static":
                   self.window.blit(drawings.surface, (drawings.PosX, drawings.PosY))
               elif drawings.type == "Dynamic":
                   self.window.blit(drawings.surface, (drawings.PyObject.x, drawings.PyObject.y))

class ObjectToDraw:
    def __init__(self, name, type, PyObject: pygame.Rect, ObjSurface: pygame.Surface, PosX: float, PosY: float, prio:int):
        self.name = name
        self.type = type

        self.PyObject : pygame.Rect

        self.surface = ObjSurface

        self.PosX : float
        self.PosY : float

        self.prio = prio

        if type == "Static":
            self.PosX = PosX
            self.PosY = PosY
        elif type == "Dynamic":
            if PyObject is None:
                self.PyObject = pygame.Rect(PosX, PosY, self.surface.get_width(), self.surface.get_height())
            else:
                self.PyObject = PyObject

