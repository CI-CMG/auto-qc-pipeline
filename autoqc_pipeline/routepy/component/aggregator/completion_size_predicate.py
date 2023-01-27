from autoqc_pipeline.routepy.framework.aggregator import Aggregator
from autoqc_pipeline.routepy.framework.predicate import Predicate


class CompletionSizePredicate(Predicate):

  def __init__(self, completetion_size):
    self.__completetion_size = completetion_size

  def matches(self, exchange):
    return exchange.get_header(Aggregator.AGGREGATOR_COMPLETED_EXCHANGES) >= self.__completetion_size
