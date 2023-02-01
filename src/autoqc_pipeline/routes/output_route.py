from eipiphany_core.framework.base.aggregator import Aggregator
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_seda.component.queue_endpoint import QueueEndpoint
from eipiphany_seda.component.queue_source import QueueSource

from ..aggregators.file_path_prefix_correlation_expression import \
  FilePathPrefixCorrelationExpression
from ..aggregators.file_summary_aggregation_stategy import \
  FileSummaryAggregationStrategy
from ..aggregators.file_summary_completion_predicate import \
  FileDoneCompletionPredicate
from ..filters.test_failed_filter import TestFailedFilter


class OutputRoute(RouteBuilder):

  def __init__(self, eip_context, file_test_result_queue,
      profile_test_failure_queue, error_queue, test_concurrency,
      file_controller, save_summary_queue, summary_save_processor,
      profile_failure_save_processor, aggregator, *args, **kw):
    super().__init__(*args, **kw)
    self.__eip_context = eip_context
    self.__file_test_result_queue = file_test_result_queue
    self.__error_queue = error_queue
    self.__test_concurrency = test_concurrency
    self.__file_controller = file_controller
    self.__save_summary_queue = save_summary_queue
    self.__summary_save_processor = summary_save_processor
    self.__profile_failure_save_processor = profile_failure_save_processor
    self.__profile_test_failure_queue = profile_test_failure_queue
    self.__aggregator = aggregator

  def build(self):
    self._from(
      QueueSource(self.__file_test_result_queue, concurrent_consumers=self.__test_concurrency)) \
        .aggregate(self.__aggregator) \
        .to(QueueEndpoint(self.__save_summary_queue, block_when_full=True))

    self._from(QueueSource(self.__save_summary_queue)) \
      .to(self.__summary_save_processor)

    self._from(QueueSource(self.__profile_test_failure_queue)).filter(
      TestFailedFilter()).to(self.__profile_failure_save_processor)

    self._from(QueueSource(self.__error_queue)) \
      .to(
      QueueEndpoint(self.__profile_test_failure_queue, block_when_full=True)) \
      .to(QueueEndpoint(self.__file_test_result_queue, block_when_full=True))
