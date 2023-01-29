import os
import warnings

from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext

from .route_configurer import RouteConfigurer

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  auto_qc_home = os.environ['AUTO_QC_HOME']
  with EipiphanyContext() as eip_context:
    RouteConfigurer(eip_context, wod_directory, gunzip_directory, concurrent_unzip_files, test_concurrency).configure()
    eip_context.start()