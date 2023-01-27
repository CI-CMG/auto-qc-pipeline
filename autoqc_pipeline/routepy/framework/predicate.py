import abc

class Predicate(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def matches(self, exchange):
    pass
