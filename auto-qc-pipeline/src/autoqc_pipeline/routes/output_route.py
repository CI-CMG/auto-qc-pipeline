from eipiphany_core.framework.base.aggregator import Aggregator
from eipiphany_core.framework.base.route_builder import RouteBuilder

from autoqc_pipeline.aggregators.file_path_prefix_correlation_expression import FilePathPrefixCorrelationExpression
from autoqc_pipeline.aggregators.file_summary_aggregation_stategy import FileSummaryAggregationStrategy
from autoqc_pipeline.aggregators.file_summary_completion_predicate import FileDoneCompletionPredicate
from autoqc_pipeline.filters.test_failed_filter import TestFailedFilter
from autoqc_pipeline.processors.file_summary_save_processor import FileSummarySaveProcessor
from autoqc_pipeline.processors.profile_failure_save_processor import ProfileFailureSaveProcessor
from autoqc_pipeline.processors.resource_cleanup_processor import ResourceCleanupProcessor


class OutputRoute(RouteBuilder):

  def __init__(self, output_directory, file_controller, gunzip_directory, *args, **kw):
    super().__init__(*args, **kw)
    self.__output_directory = output_directory
    self.__file_controller = file_controller
    self.__gunzip_directory = gunzip_directory

  def build(self, eip_context):
    self._from(eip_context, 'seda:file-test-result-queue') \
      .aggregate(Aggregator(eip_context,
                            FilePathPrefixCorrelationExpression(),
                            FileSummaryAggregationStrategy(self.__file_controller),
                            [FileDoneCompletionPredicate()])) \
      .to(eip_context, 'seda:save-summary-queue')

    self._from(eip_context, 'seda:save-summary-queue') \
      .process(ResourceCleanupProcessor(self.__gunzip_directory))\
      .process(FileSummarySaveProcessor(self.__output_directory))

    self._from(eip_context, 'seda:profile-test-failure-queue') \
      .filter(TestFailedFilter()) \
      .process(ProfileFailureSaveProcessor(self.__output_directory))

    self._from(eip_context, 'seda:error-queue') \
      .to(eip_context, 'seda:profile-test-failure-queue') \
      .to(eip_context, 'seda:file-test-result-queue')
