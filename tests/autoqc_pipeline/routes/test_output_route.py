from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext
from eipiphany_core.framework.test_support.eipiphany_test_context import \
  EipiphanyTestContext

from src.autoqc_pipeline.application.route_configurer import RouteConfigurer


class TestOutputRoute(object):

  def test_aggregate_complete(self):
    wod_directory = 'test-resources/wod18'
    gunzip_directory = 'gunzip-dir'
    output_directory = 'test-dir'
    auto_qc_home = "../AutoQC"
    concurrent_unzip_files = 2
    test_concurrency = 2

    # done_file = 'test-resources/wod18/MRB/OBS/MRBO2022.gz.autoqc'
    #
    # route_config = RouteConfigurer(wod_directory, auto_qc_home,
    #                                gunzip_directory, output_directory,
    #                                concurrent_unzip_files, test_concurrency)
    #
    # with EipiphanyTestContext(EipiphanyContext()) as eip_context:
    #   route_config.configure(eip_context)
    #   eip_context.start()

  def test_error(self):
    pass
