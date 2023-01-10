import abc

class Joiner(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def join(self):
    pass