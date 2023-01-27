import abc

class AggregationStrategy(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def aggregate(self, old_exchange, new_exchange):
    pass
