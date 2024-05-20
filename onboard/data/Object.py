from enum import Enum

class ObjectType(Enum):
  CONTROL = 0
  SENSOR = 1
  ACTUATOR = 2

class Object:
  def __init__(self, name: str, type: ObjectType):
    self.name = name
    self.type = type

  def logAction(self):
    pass

  def logStat(self):
    pass

  def logError(self):
    pass