from eipiphany_core.framework.base.route_builder import RouteBuilder

from autoqc_pipeline.processors.file_gunzip_processor import FileGunzipProcessor
from autoqc_pipeline.processors.file_message_processor import FileMessageProcessor
from autoqc_pipeline.processors.geohash_processor import GeohashProcessor
from autoqc_pipeline.processors.resource_cleanup_processor import ResourceCleanupProcessor
from autoqc_pipeline.processors.wodpy_profile_processor import WodpyProfileProcessor


class FileRoute(RouteBuilder):

  def __init__(self, wod_directory, gunzip_directory, file_controller, geohash_service, filter, output_directory, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory
    self.__file_controller = file_controller
    self.__geohash_service = geohash_service
    self.__filter = filter
    self.__output_directory = output_directory

  def build(self, eip_context):
    self._from(eip_context, 'file:' + self.__wod_directory) \
      .process(FileMessageProcessor()) \
      .to(eip_context, 'seda:gunzip-queue')

    self._from(eip_context, 'seda:gunzip-queue')\
      .process(ResourceCleanupProcessor(self.__gunzip_directory))\
      .process(FileGunzipProcessor(self.__wod_directory, self.__gunzip_directory, self.__output_directory))\
      .process(GeohashProcessor(self.__geohash_service, self.__filter))\
      .process(WodpyProfileProcessor(eip_context, self.__file_controller, self.__geohash_service))
