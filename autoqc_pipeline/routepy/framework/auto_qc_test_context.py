import abc

class AutoQcTestContext(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def getCast(self):
    pass
