import logging
import os
import sys
import warnings

from eipiphany_core.framework.base.eip_context import EipContext
from src.autoqc_pipeline.application.route_configurer import RouteConfigurer

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  root.addHandler(handler)

  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  output_directory = os.environ['AUTO_QC_OUTPUT']
  auto_qc_home = os.environ['AUTO_QC_HOME']
  concurrent_unzip_files = 3
  test_concurrency = 16

  with EipContext() as eip_context:
    route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                   gunzip_directory, output_directory,
                                   concurrent_unzip_files, test_concurrency)
    route_config.configure()
    eip_context.start()

# if __name__ == '__main__':
  # wod_directory = os.environ['WOD_GZ_DATA']
  # gunzip_directory = os.environ['WOD_UNGZ_DATA']
  # gunzip_queue = JoinableQueue(maxsize=1000)
  # test_queue = JoinableQueue(maxsize=1000)
  # gunzip_processor = GunzipProcessor(wod_directory, gunzip_directory)
  #
  # test_processor = TestProcessor()
  # test_result_processor = SimpleTimestampProcessor()
  # message_prep_processor = MessagePrepProcessor()
  # profile_filter = ProfileFilter()
  # aggregator_queue =JoinableQueue(maxsize=1000)
  # correlation_expression = FileDoneCorrelationExpression()
  #
  # completion_expression_list = [FileDoneCompletionPredicate(),CompletionSizePredicate(100)]
  #
  #
  # with Manager() as manager:
  #   file_controller = FileController(manager)
  #   wodpy_processor = WodpyProcessor(test_queue, file_controller)
  #   aggregation_strategy = FileDoneAggregationStrategy(file_controller)
  #   test_route = TestRoute(wod_directory, gunzip_directory, gunzip_queue,
  #                          test_queue, message_prep_processor, gunzip_processor,
  #                          wodpy_processor, test_processor, test_result_processor,
  #                          profile_filter, aggregator_queue, correlation_expression,
  #                          aggregation_strategy, completion_expression_list, manager)
  #   test_route.build()
  #   joiners = test_route.start()
  #
  #   # todo join in reverse order?
  #   for joiner in joiners:
  #     joiner.join()
