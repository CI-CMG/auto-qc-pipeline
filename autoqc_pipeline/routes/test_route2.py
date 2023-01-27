from eipiphany_core.component.error_handler.dead_letter_channel import \
  DeadLetterChannel
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_file.component.file_configuration import FileSourceConfiguration
from eipiphany_file.component.file_source import FileSource
from eipiphany_seda.component.queue_endpoint import QueueEndpoint
from eipiphany_seda.component.queue_source import QueueSource


class TestRoute2(RouteBuilder):

  def __init__(self, wod_directory, gunzip_directory, gunzip_queue, test_queue,
      message_prep_processor, gunzip_processor, wodpy_processor, test_processor,
      test_result_processor, profile_filter, error_queue, dlq_prep_processor, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory
    self.__gunzip_queue = gunzip_queue
    self.__test_queue = test_queue
    self.__message_prep_processor = message_prep_processor
    self.__gunzip_processor = gunzip_processor
    self.__wodpy_processor = wodpy_processor
    self.__test_processor = test_processor
    self.__test_result_processor = test_result_processor
    self.__profile_filter = profile_filter
    self.__error_queue = error_queue
    self.__dlq_prep_processor = dlq_prep_processor

  def build(self):
    # self._error_handler(DeadLetterChannel(QueueEndpoint(self.__gunzip_queue, block_when_full=True)).on_prepare_failure(self.__dlq_prep_processor))

    self._from(
      FileSource(FileSourceConfiguration()
                 .set_directory(self.__wod_directory)
                 .set_recursive(True)
                 .set_include_ext(['gz'])
                 .set_done_file_ext('autoqc')))\
      .to(self.__message_prep_processor)\
      .to(QueueEndpoint(self.__gunzip_queue, block_when_full=True))

    self._from(
      QueueSource(self.__gunzip_queue, concurrent_consumers=3))\
      .to(self.__gunzip_processor)\
      .to(self.__wodpy_processor)

    self._from(
      QueueSource(self.__test_queue, concurrent_consumers=16))\
      .filter(self.__profile_filter)\
      .to(self.__test_processor)\
      .to(self.__test_result_processor)
