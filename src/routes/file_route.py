from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_file.component.file_configuration import FileSourceConfiguration
from eipiphany_file.component.file_source import FileSource
from eipiphany_seda.component.queue_endpoint import QueueEndpoint
from eipiphany_seda.component.queue_source import QueueSource



class FileRoute(RouteBuilder):

  def __init__(self, wod_directory, gunzip_queue, message_prep_processor, gunzip_processor, wodpy_processor, concurrent_unzip_files, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__message_prep_processor = message_prep_processor
    self.__gunzip_queue = gunzip_queue
    self.__gunzip_processor = gunzip_processor
    self.__wodpy_processor = wodpy_processor
    self.__concurrent_unzip_files = concurrent_unzip_files

  def build(self):
    self._from(
      FileSource(FileSourceConfiguration()
                 .set_directory(self.__wod_directory)
                 .set_recursive(True)
                 .set_include_ext(['gz'])
                 .set_done_file_ext('autoqc'))) \
      .to(self.__message_prep_processor) \
      .to(QueueEndpoint(self.__gunzip_queue, block_when_full=True))

    self._from(
      QueueSource(self.__gunzip_queue, concurrent_consumers=self.__concurrent_unzip_files)) \
      .to(self.__gunzip_processor) \
      .to(self.__wodpy_processor)