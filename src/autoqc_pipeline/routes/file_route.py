from eipiphany_core.framework.base.route_builder import RouteBuilder

from ..processors.file_gunzip_processor import FileGunzipProcessor
from ..processors.file_message_processor import FileMessageProcessor
from ..processors.wodpy_profile_processor import WodpyProfileProcessor


class FileRoute(RouteBuilder):

  def __init__(self, wod_directory, gunzip_directory, file_controller, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory
    self.__file_controller = file_controller

  def build(self, eip_context):
    self._from(eip_context, 'file:' + self.__wod_directory) \
      .process(FileMessageProcessor()) \
      .to(eip_context, 'seda:gunzip-queue')

    self._from(eip_context, 'seda:gunzip-queue')\
      .process(FileGunzipProcessor(self.__wod_directory, self.__gunzip_directory))\
      .process(WodpyProfileProcessor(eip_context, self.__file_controller))
