import os
import warnings
from multiprocessing import JoinableQueue, Manager

from autoqc_pipeline.aggregation.file_done_aggregation_stategy import \
  FileDoneAggregationStrategy
from autoqc_pipeline.aggregation.file_done_correlation_expression import \
  FileDoneCorrelationExpression
from autoqc_pipeline.filters.profile_filter import ProfileFilter
from autoqc_pipeline.processors.gunzip_processor import GunzipProcessor
from autoqc_pipeline.processors.message_prep_processor import \
  MessagePrepProcessor
from autoqc_pipeline.processors.simple_timestamp_processor import \
  SimpleTimestampProcessor
from autoqc_pipeline.processors.test_processor import TestProcessor
from autoqc_pipeline.processors.wodpy_processor import WodpyProcessor
from autoqc_pipeline.routepy.component.aggregator.completion_size_predicate import \
  CompletionSizePredicate
from autoqc_pipeline.routepy.component.aggregator.single_correlation_expression import \
  SingleCorrelationExpression
from autoqc_pipeline.routepy.framework.aggregation_strategy import \
  AggregationStrategy
from autoqc_pipeline.routepy.framework.expression import Expression
from autoqc_pipeline.routes.test_route import TestRoute
from autoqc_pipeline.service.file_controller import FileController

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  gunzip_queue = JoinableQueue(maxsize=1000)
  test_queue = JoinableQueue(maxsize=1000)
  gunzip_processor = GunzipProcessor(wod_directory, gunzip_directory)
  wodpy_processor = WodpyProcessor(test_queue)
  test_processor = TestProcessor()
  test_result_processor = SimpleTimestampProcessor()
  message_prep_processor = MessagePrepProcessor()
  profile_filter = ProfileFilter()
  aggregator_queue =JoinableQueue(maxsize=1000)
  correlation_expression = FileDoneCorrelationExpression()

  completion_expression_list = [CompletionSizePredicate(4)]


  with Manager() as manager:
    file_controller = FileController(manager)
    agregation_strategy = FileDoneAggregationStrategy(file_controller)
    test_route = TestRoute(wod_directory, gunzip_directory, gunzip_queue,
                           test_queue, message_prep_processor, gunzip_processor,
                           wodpy_processor, test_processor, test_result_processor,
                           profile_filter, aggregator_queue, correlation_expression,
                           agregation_strategy, completion_expression_list, manager)
    test_route.build()
    joiners = test_route.start()

    # todo join in reverse order?
    for joiner in joiners:
      joiner.join()
