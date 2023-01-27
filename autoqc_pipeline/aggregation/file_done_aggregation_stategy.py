from autoqc_pipeline.model.auto_qc_file_result import AutoQcFileResult
from autoqc_pipeline.model.auto_qc_test_context_imp import AutoQcTestContextImpl
from autoqc_pipeline.routepy.framework.aggregation_strategy import \
  AggregationStrategy

class FileDoneAggregationStrategy(AggregationStrategy):

  def __init__(self, file_controller):
    self.__file_controller = file_controller

  def aggregate(self, old_exchange, new_exchange):
    message = new_exchange.get_body()
    if (old_exchange):
      file_result = old_exchange.get_body()
      self.update_counts(file_result, message)
      return old_exchange
    else:
      file_result = AutoQcFileResult(message.file_path_prefix)
      self.update_counts(file_result, message)
      new_exchange.set_body(file_result)
      return new_exchange

  def update_counts(self, file_result, test_context):
    file_result.increment_total_casts()
    if(self.__file_controller.on_done_cast(test_context.get_file_path_prefix(), test_context.get_cast().get_cast_number())):
      file_result.set_complete()

    failure_counts = file_result.get_failure_counts()
    for test_name in test_context.get_cast_test_result().get_cast_failures():
      count = failure_counts.get(test_name)
      if count is None:
        count = 0
      failure_counts[test_name] = count + 1
    file_result.set_failure_counts(failure_counts)
    if test_context.get_cast_test_result().get_exception() is not None:
      file_result.set_exceptions(file_result.get_exceptions() + 1)
