import os
import warnings
from multiprocessing import JoinableQueue

from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext

from autoqc_pipeline.filters.profile_filter2 import ProfileFilter2
from autoqc_pipeline.processors.dlq_prep_processor import DlqPrepProcessor
from autoqc_pipeline.processors.gunzip_processor2 import GunzipProcessor2
from autoqc_pipeline.processors.message_prep_processor2 import \
  MessagePrepProcessor2
from autoqc_pipeline.processors.simple_timestamp_processor2 import \
  SimpleTimestampProcessor2
from autoqc_pipeline.processors.test_processor2 import TestProcessor2
from autoqc_pipeline.processors.wodpy_processor2 import WodpyProcessor2
from autoqc_pipeline.routes.test_route2 import TestRoute2


warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  gunzip_queue = JoinableQueue(maxsize=1000)
  test_queue = JoinableQueue(maxsize=1000)
  error_queue = JoinableQueue(maxsize=1000)
  gunzip_processor = GunzipProcessor2(wod_directory, gunzip_directory)
  wodpy_processor = WodpyProcessor2(test_queue)
  test_processor = TestProcessor2()
  test_result_processor = SimpleTimestampProcessor2()
  message_prep_processor = MessagePrepProcessor2()
  profile_filter = ProfileFilter2()
  dlq_prep_processor = DlqPrepProcessor()

  with EipiphanyContext() as eip_context:
    eip_context.add_route_builder(TestRoute2(wod_directory, gunzip_directory, gunzip_queue,
                                             test_queue, message_prep_processor, gunzip_processor,
                                             wodpy_processor, test_processor, test_result_processor,
                                             profile_filter, error_queue, dlq_prep_processor))
    eip_context.start()

