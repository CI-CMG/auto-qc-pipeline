import abc

class AutoQcTestContext(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def get_cast(self):
    pass
