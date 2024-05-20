from dataclasses import dataclass
import RPi.GPIO as GPIO

from data.Object import Object, ObjectType

@dataclass
class Servo(Object):
  def __init__(self, name: str):
    Object.__init__(name, ObjectType.ACTUATOR)

