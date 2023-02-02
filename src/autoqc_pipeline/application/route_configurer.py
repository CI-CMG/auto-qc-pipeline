from eipiphany_file.component.file_configuration import FileConfiguration
from eipiphany_file.component.file_endpoint import FileEndpoint
from eipiphany_seda.component.seda_configuration import SedaConfiguration
from eipiphany_seda.component.seda_endpoint import SedaEndpoint

from ..routes.file_route import FileRoute
from ..routes.output_route import OutputRoute
from ..routes.profile_test_route import ProfileTestRoute
from ..services.file_controller import FileController


class RouteConfigurer(object):

  def __init__(self, eip_context, wod_directory, auto_qc_home, gunzip_directory, output_directory, concurrent_unzip_files, test_concurrency):
    self.__eip_context = eip_context
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory
    self.__output_directory = output_directory
    self.__auto_qc_home = auto_qc_home
    self.__concurrent_unzip_files = concurrent_unzip_files
    self.__test_concurrency = test_concurrency
    self.__file_controller = FileController(eip_context.manager)

  @property
  def file_controller(self):
    return self.__file_controller

  def configure(self):
    self.__eip_context.register_endpoint(FileEndpoint(self.__wod_directory, FileConfiguration().set_directory(self.__wod_directory).set_recursive(True).set_include_ext(['gz']).set_done_file_ext('autoqc')))
    self.__eip_context.register_endpoint(SedaEndpoint('gunzip-queue', SedaConfiguration().set_concurrent_consumers(self.__concurrent_unzip_files)))
    self.__eip_context.register_endpoint(SedaEndpoint('test-queue', SedaConfiguration().set_concurrent_consumers(self.__test_concurrency)))
    self.__eip_context.register_endpoint(SedaEndpoint('error-queue'))
    self.__eip_context.register_endpoint(SedaEndpoint('profile-test-failure-queue', SedaConfiguration().set_concurrent_consumers(self.__test_concurrency)))
    self.__eip_context.register_endpoint(SedaEndpoint('file-test-result-queue'))
    self.__eip_context.register_endpoint(SedaEndpoint('save-summary-queue'))

    self.__eip_context.add_route_builder(FileRoute(self.__wod_directory, self.__gunzip_directory))
    self.__eip_context.add_route_builder(ProfileTestRoute(self.__auto_qc_home))
    self.__eip_context.add_route_builder(OutputRoute(self.__output_directory, self.__file_controller))
