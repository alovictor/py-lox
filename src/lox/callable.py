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
    
    def arity():
        return 0
