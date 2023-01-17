import abc

class Filter(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def filter(self, exchange):
    pass
