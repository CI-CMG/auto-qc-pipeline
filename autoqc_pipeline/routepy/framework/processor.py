import abc

class Processor(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def process(self, exchange):
    pass
