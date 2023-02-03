import os
import logging.config
import yaml
from multiprocessing import Process

from eipiphany_core.framework.base.eip_context import EipContext
from eipiphany_core.framework.test_support.eip_test_context import \
  EipTestContext
from eipiphany_core.framework.test_support.test_eip_context_termination import \
  TestEipContextTermination

from autoqc_pipeline.routepy.framework.processor import Processor
from src.autoqc_pipeline.application.route_configurer import RouteConfigurer


def touch(trigger_file):
  with open(trigger_file, 'a') as f: pass

class ProfileErrorTester(Processor):
  def process(self, exchange):
    raise Exception("Test Exception")

class TestTestRoute(object):

  def test_error(self):


    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']

    with open(os.path.join(project_root, 'test-resources', 'logging.yaml'), 'r') as stream:
      config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)


    wod_directory = os.path.join(project_root, 'test-resources', 'wod18')
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    output_directory = os.path.join(project_root, 'test-dir')
    auto_qc_home = os.path.join(project_root, "..", "AutoQC")
    concurrent_unzip_files = 1
    test_concurrency = 2

    trigger_file = os.path.join(wod_directory, 'CTD', 'OBS', 'CTDO2020.gz.autoqc')

    if os.path.exists(trigger_file):
      os.remove(trigger_file)
    try:
      with EipTestContext(EipContext(), termination=TestEipContextTermination(timeout=20000)) as eip_context:
        route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                       gunzip_directory, output_directory,
                                       concurrent_unzip_files, test_concurrency)
        route_config.profile_test_processor = ProfileErrorTester()
        route_config.configure()

        eip_context.mock_endpoint_and_skip('seda:error-queue', expected_message_count=3)

        eip_context.start_with_trigger(Process(target=touch, args=(trigger_file,)))

        exchanges = eip_context.get_endpoint('seda:error-queue').exchanges

        assert len(exchanges) == 3

        test_message1 = exchanges[0].body
        test_message2 = exchanges[1].body
        test_message3 = exchanges[2].body

        assert test_message1.profile_test_result.exception == "Test Exception"
        assert test_message2.profile_test_result.exception == "Test Exception"
        assert test_message3.profile_test_result.exception == "Test Exception"

        assert test_message1.profile_test_result.failed
        assert test_message2.profile_test_result.failed
        assert test_message3.profile_test_result.failed


    finally:
      if os.path.exists(trigger_file):
        os.remove(trigger_file)

  def test_no_failures(self):
    pass

  def test_failures(self):
    pass


