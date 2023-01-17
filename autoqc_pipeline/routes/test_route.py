from autoqc_pipeline.routepy.component.file.file_configuration import \
  FileSourceConfiguration
from autoqc_pipeline.routepy.component.file.file_source import FileSource
from autoqc_pipeline.routepy.component.seda.queue_endpoint import QueueEndpoint
from autoqc_pipeline.routepy.component.seda.queue_source import QueueSource
from autoqc_pipeline.routepy.framework.route_builder import RouteBuilder


class TestRoute(RouteBuilder):


  def __init__(self, wod_directory, gunzip_directory, gunzip_queue, test_queue, message_prep_processor, gunzip_processor, wodpy_processor, test_processor, test_result_processor, profile_filter, *args, **kw):
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

  def build(self):
    self.comes_from(FileSource(FileSourceConfiguration().set_directory(self.__wod_directory).set_recursive(True).set_include_ext(['gz']).set_done_file_ext('autoqc'))).to(self.__message_prep_processor).to(QueueEndpoint(self.__gunzip_queue, block_when_full=True))
    self.comes_from(QueueSource(self.__gunzip_queue)).to(self.__gunzip_processor).to(self.__wodpy_processor)
    self.comes_from(QueueSource(self.__test_queue, concurrent_consumers=16)).filter(self.__profile_filter).to(self.__test_processor).to(self.__test_result_processor)


