import abc

class Expression(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def evaluate(self, exchange):
    pass
