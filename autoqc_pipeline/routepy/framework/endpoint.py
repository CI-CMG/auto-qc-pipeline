import abc


class Endpoint(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def to(self, exchange):
    pass
