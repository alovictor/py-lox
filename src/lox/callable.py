import time
from abc import ABC, abstractmethod

class LoxCallable(ABC):
    @abstractmethod
    def call(interpreter, arguments):
        pass

    @abstractmethod
    def arity():
        pass

class LoxClock(LoxCallable):
    def call(self, interpreter, arguments):
        return time.time()
    
    def arity(self):
        return 0

    def to_string(self):
        return '<native fn>'
