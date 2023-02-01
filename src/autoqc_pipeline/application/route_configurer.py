from multiprocessing import JoinableQueue

from eipiphany_core.framework.base.aggregator import Aggregator

from ..aggregators.file_summary_completion_predicate import \
  FileDoneCompletionPredicate

from ..aggregators.file_summary_aggregation_stategy import \
  FileSummaryAggregationStrategy

from ..aggregators.file_path_prefix_correlation_expression import \
  FilePathPrefixCorrelationExpression

from ..filters.pathological_profile_filter import PathologicalProfilesFilter
from ..processors.file_gunzip_processor import FileGunzipProcessor
from ..processors.file_message_processor import FileMessageProcessor
from ..processors.file_summary_save_processor import FileSummarySaveProcessor
from ..processors.iquod_flag_processor import IquodFlagProcessor
from ..processors.profile_failure_save_processor import \
  ProfileFailureSaveProcessor
from ..processors.profile_test_processor import ProfileTestProcessor
from ..processors.test_catalog import TestCatalog
from ..processors.test_error_dlq_prep_processor import TestErrorDlqPrepProcessor
from ..processors.wodpy_profile_processor import WodpyProfileProcessor
from ..routes.file_route import FileRoute
from ..routes.output_route import OutputRoute
from ..routes.profile_test_route import ProfileTestRoute
from ..services.file_controller import FileController


class RouteConfigurer(object):

  def __init__(self, eip_context, wod_directory, auto_qc_home, gunzip_directory,
      output_directory,
      concurrent_unzip_files, test_concurrency):
    self.__eip_context = eip_context
    self.__wod_directory = wod_directory
    self.__concurrent_unzip_files = concurrent_unzip_files
    self.__test_concurrency = test_concurrency
    self.__gunzip_queue = JoinableQueue(maxsize=1000)
    self.__file_message_processor = FileMessageProcessor()
    self.__test_queue = JoinableQueue(maxsize=1000)
    self.__error_queue = JoinableQueue(maxsize=1000)
    self.__profile_test_failure_queue = JoinableQueue(maxsize=1000)
    self.__file_test_result_queue = JoinableQueue(maxsize=1000)
    self.__save_summary_queue = JoinableQueue(maxsize=1000)
    self.__gunzip_processor = FileGunzipProcessor(wod_directory, gunzip_directory)
    self.__wodpy_processor = WodpyProfileProcessor(self.__test_queue)
    self.__test_catalog = TestCatalog()
    self.__test_processor = ProfileTestProcessor(auto_qc_home, PathologicalProfilesFilter(), self.__test_catalog)
    self.__dlq_prep_processor = TestErrorDlqPrepProcessor()
    self.__file_controller = FileController(eip_context.manager)
    self.__summary_save_processor = FileSummarySaveProcessor(output_directory)
    self.__profile_failure_save_processor = ProfileFailureSaveProcessor(
      output_directory)
    self.__iquod_flag_processor = IquodFlagProcessor(self.__test_catalog)
    self.__file_path_corr_exp = FilePathPrefixCorrelationExpression()
    self.__file_summary_agg_strat = FileSummaryAggregationStrategy(self.__file_controller)
    self.__file_summary_comp_pred = FileDoneCompletionPredicate()
    self.__aggregator = Aggregator(eip_context, self.__file_path_corr_exp, self.__file_summary_agg_strat, [self.__file_summary_comp_pred])

  def configure(self):
    self.__eip_context.add_route_builder(
      FileRoute(self.__wod_directory, self.__gunzip_queue,
                self.__file_message_processor, self.__gunzip_processor,
                self.__wodpy_processor, self.__concurrent_unzip_files))

    self.__eip_context.add_route_builder(
      ProfileTestRoute(self.__test_concurrency,
                       self.__error_queue,
                       self.__dlq_prep_processor,
                       self.__profile_test_failure_queue,
                       self.__file_test_result_queue,
                       self.__test_queue,
                       self.__test_processor,
                       self.__iquod_flag_processor))

    self.__eip_context.add_route_builder(
      OutputRoute(self.__eip_context, self.__file_test_result_queue,
                  self.__profile_test_failure_queue, self.__error_queue,
                  self.__test_concurrency,
                  self.__file_controller, self.__save_summary_queue,
                  self.__summary_save_processor,
                  self.__profile_failure_save_processor,
                  self.__aggregator))
