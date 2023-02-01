from eipiphany_core.framework.base.aggregator import Aggregator
from eipiphany_core.framework.base.route_builder import RouteBuilder

from ..aggregators.file_path_prefix_correlation_expression import FilePathPrefixCorrelationExpression
from ..aggregators.file_summary_aggregation_stategy import FileSummaryAggregationStrategy
from ..aggregators.file_summary_completion_predicate import FileDoneCompletionPredicate
from ..filters.test_failed_filter import TestFailedFilter
from ..processors.file_summary_save_processor import FileSummarySaveProcessor
from ..processors.profile_failure_save_processor import ProfileFailureSaveProcessor


class OutputRoute(RouteBuilder):

  def __init__(self, output_directory, file_controller, *args, **kw):
    super().__init__(*args, **kw)
    self.__output_directory = output_directory
    self.__file_controller = file_controller

  def build(self, eip_context):
    self._from(eip_context, 'seda:profile-test-failure-queue') \
      .aggregate(Aggregator(eip_context,
                            FilePathPrefixCorrelationExpression(),
                            FileSummaryAggregationStrategy(self.__file_controller),
                            [FileDoneCompletionPredicate()])) \
      .to(eip_context, 'seda:save-summary-queue')

    self._from(eip_context, 'seda:save-summary-queue') \
      .process(FileSummarySaveProcessor(self.__output_directory))

    self._from(eip_context, 'seda:profile-test-failure-queue') \
      .filter(TestFailedFilter()) \
      .process(ProfileFailureSaveProcessor(self.__output_directory))

    self._from(eip_context, 'seda:error-queue') \
      .to(eip_context, 'seda:profile-test-failure-queue') \
      .to(eip_context, 'seda:file-test-result-queue')
