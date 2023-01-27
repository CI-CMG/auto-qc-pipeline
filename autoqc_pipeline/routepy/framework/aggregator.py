
class Aggregator(object):
  AGGREGATOR_COMPLETED_EXCHANGES = "AggregatorCompletedExchanges"

  def __init__(self, correlation_expression, aggregation_strategy,  completion_expression_list, manager):
    self.__aggregation_state = manager.dict()
    self.__aggregation_strategy = aggregation_strategy
    self.__correlation_expression = correlation_expression
    self.__completion_expression_list = completion_expression_list
    self.__lock = manager.RLock()

  def aggregate(self, new_exchange):
    correlation_id = self.__correlation_expression.evaluate(new_exchange)
    if correlation_id is not None:
      self.__lock.acquire()
      try:
        old_exchange = self.__aggregation_state.get(correlation_id)
        count = 0 if old_exchange is None else old_exchange.get_header(Aggregator.AGGREGATOR_COMPLETED_EXCHANGES)
        exchange = self.__aggregation_strategy.aggregate(old_exchange, new_exchange)
        exchange.set_header(Aggregator.AGGREGATOR_COMPLETED_EXCHANGES, count+1)
        self.__aggregation_state[correlation_id] = exchange
        for completion_expression in self.__completion_expression_list:
          if completion_expression.matches(exchange):
            del self.__aggregation_state[correlation_id]
            return exchange
      finally:
        self.__lock.release()
    return None

