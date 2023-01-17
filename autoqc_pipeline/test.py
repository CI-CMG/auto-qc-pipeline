import warnings
from multiprocessing import JoinableQueue

from autoqc_pipeline.filters.profile_filter import ProfileFilter
from autoqc_pipeline.processors.gunzip_processor import GunzipProcessor
from autoqc_pipeline.processors.message_prep_processor import \
  MessagePrepProcessor
from autoqc_pipeline.processors.simple_timestamp_processor import \
  SimpleTimestampProcessor
from autoqc_pipeline.processors.test_processor import TestProcessor
from autoqc_pipeline.processors.wodpy_processor import WodpyProcessor
from autoqc_pipeline.routes.test_route import TestRoute


warnings.simplefilter(action='ignore', category=FutureWarning)


if __name__ == '__main__':
  wod_directory = '/Users/cslater/Desktop/wod/wod18'
  gunzip_directory = '/Users/cslater/projects/auto-qc-pipeline/gunzip-dir'
  gunzip_queue = JoinableQueue(3)
  test_queue = JoinableQueue(1000)
  gunzip_processor = GunzipProcessor(wod_directory, gunzip_directory)
  wodpy_processor = WodpyProcessor(test_queue)
  test_processor = TestProcessor()
  test_result_processor = SimpleTimestampProcessor()
  message_prep_processor = MessagePrepProcessor()
  profile_filter = ProfileFilter()

  test_route = TestRoute(wod_directory, gunzip_directory, gunzip_queue,
                         test_queue, message_prep_processor, gunzip_processor,
                         wodpy_processor, test_processor, test_result_processor,
                         profile_filter)
  test_route.build()
  joiners = test_route.start()

  # todo join in reverse order?
  for joiner in joiners:
    joiner.join()
