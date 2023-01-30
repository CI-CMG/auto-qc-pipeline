import os
import warnings

from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext

from .route_configurer import RouteConfigurer

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  output_directory = os.environ['AUTO_QC_OUTPUT']
  auto_qc_home = os.environ['AUTO_QC_HOME']
  concurrent_unzip_files = 3
  test_concurrency = 16

  with EipiphanyContext() as eip_context:
    route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                   gunzip_directory, output_directory,
                                   concurrent_unzip_files, test_concurrency)
    route_config.configure()
    eip_context.start()
