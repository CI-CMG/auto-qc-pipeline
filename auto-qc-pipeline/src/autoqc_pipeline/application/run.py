import os
import warnings

import yaml
from eipiphany_core.framework.base.eip_context import EipContext

from autoqc_pipeline.application.route_configurer import RouteConfigurer

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
  wod_directory = os.environ['WOD_GZ_DATA']
  gunzip_directory = os.environ['WOD_UNGZ_DATA']
  output_directory = os.environ['AUTO_QC_OUTPUT']
  auto_qc_home = os.environ['AUTO_QC_HOME']
  logging_config_file = os.environ['AUTO_QC_LOGGING_YAML']
  run_only_iquod = bool(os.environ.get('RUN_ONLY_IQUOD'))
  if os.environ.get('AUTO_QC_PIPELINE_UNZIP_CONCUR'):
    concurrent_unzip_files = int(os.environ.get('AUTO_QC_PIPELINE_UNZIP_CONCUR'))
  else:
    concurrent_unzip_files = 1
  if os.environ.get('AUTO_QC_PIPELINE_TEST_CONCUR'):
    test_concurrency = int(os.environ.get('AUTO_QC_PIPELINE_TEST_CONCUR'))
  else:
    test_concurrency = 1

  logging_config = None
  with open(logging_config_file, 'r') as stream:
    logging_config = yaml.load(stream, Loader=yaml.FullLoader)

  with EipContext(logging_config=logging_config) as eip_context:
    route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                   gunzip_directory, output_directory,
                                   concurrent_unzip_files, test_concurrency, run_only_iquod)
    route_config.configure()
    eip_context.start()
