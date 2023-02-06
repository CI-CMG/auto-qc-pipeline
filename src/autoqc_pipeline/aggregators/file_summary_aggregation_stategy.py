from eipiphany_core.framework.base.aggregation_strategy import \
  AggregationStrategy

from ..model.file_summary_message import FileSummaryMessage


class FileSummaryAggregationStrategy(AggregationStrategy):

  def __init__(self, file_controller):
    self.__file_controller = file_controller

  def aggregate(self, old_exchange, new_exchange):
    test_message = new_exchange.body
    if (old_exchange):
      file_summary = old_exchange.body
      self.__update_counts(file_summary, test_message)
      return old_exchange
    else:
      file_summary = FileSummaryMessage(test_message.file_path_prefix)
      self.__update_counts(file_summary, test_message)
      new_exchange.body = file_summary
      return new_exchange

  def __update_counts(self, file_summary, test_message):
    file_summary.increment_total_profiles()
    if(self.__file_controller.on_done_profile(test_message.file_path_prefix, test_message.profile.uid())):
      print("aggregate complete: {}".format(file_summary.file_path_prefix))
      file_summary.complete = True

    for test_name in test_message.profile_test_result.profile_failures:
      count = file_summary.failure_counts.get(test_name)
      if count is None:
        count = 0
      file_summary.failure_counts[test_name] = count + 1

    if test_message.profile_test_result.exception is not None:
      file_summary.increment_exception_count()
