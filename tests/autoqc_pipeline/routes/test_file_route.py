import os
from multiprocessing import Process

from eipiphany_core.framework.base.eip_context import EipContext
from eipiphany_core.framework.test_support.eip_test_context import \
  EipTestContext
from eipiphany_core.framework.test_support.test_eip_context_termination import \
  TestEipContextTermination

from src.autoqc_pipeline.application.route_configurer import RouteConfigurer


def touch(trigger_file):
  with open(trigger_file, 'a') as f: pass

class TestFileRoute(object):

  def test_consume_file(self):

    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    wod_directory = os.path.join(project_root, 'test-resources', 'wod18')
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    output_directory = os.path.join(project_root, 'test-dir')
    auto_qc_home = os.path.join(project_root, "..", "AutoQC")
    concurrent_unzip_files = 1
    test_concurrency = 1

    trigger_file = os.path.join(wod_directory, 'MRB', 'OBS', 'MRBO2022.gz.autoqc')

    if os.path.exists(trigger_file):
      os.remove(trigger_file)
    try:
      with EipTestContext(EipContext()) as eip_context:
        route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                       gunzip_directory, output_directory,
                                       concurrent_unzip_files, test_concurrency)
        route_config.configure()

        eip_context.mock_endpoint_and_skip('seda:test-queue', expected_message_count=2)

        eip_context.start_with_trigger(Process(target=touch, args=(trigger_file,)))

        exchanges = eip_context.get_endpoint('seda:test-queue').exchanges
        test_message1 = exchanges[0].body
        test_message2 = exchanges[1].body
        test_message3 = exchanges[2].body

        assert test_message1.profile.uid() == 21418924
        assert test_message2.profile.uid() == 21418925
        assert test_message3.profile.uid() == 21418926

        assert test_message1.file_path_prefix == "MRB/OBS/MRBO2022"
        assert test_message2.file_path_prefix == "MRB/OBS/MRBO2022"
        assert test_message3.file_path_prefix == "MRB/OBS/MRBO2022"

        assert test_message1.last_profile == False
        assert test_message2.last_profile == False
        assert test_message3.last_profile == True

        fc_context = route_config.file_controller.get_context("MRB/OBS/MRBO2022")

        assert 21418924 in fc_context.profiles
        assert 21418925 in fc_context.profiles
        assert 21418926 in fc_context.profiles

        assert fc_context.complete

    finally:
      if os.path.exists(trigger_file):
        os.remove(trigger_file)



  def test_test_processor(self):

    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    wod_directory = os.path.join(project_root, 'test-resources', 'wod18')
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    output_directory = os.path.join(project_root, 'test-dir')
    auto_qc_home = os.path.join(project_root, "..", "AutoQC")
    concurrent_unzip_files = 1
    test_concurrency = 1

    trigger_file = os.path.join(wod_directory, 'CTD', 'OBS', 'CTDO2020.gz.autoqc')

    if os.path.exists(trigger_file):
      os.remove(trigger_file)
    try:
      with EipTestContext(EipContext(), termination=TestEipContextTermination(timeout=60000)) as eip_context:
        route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                       gunzip_directory, output_directory,
                                       concurrent_unzip_files, test_concurrency)
        route_config.configure()

        # eip_context.mock_endpoint_and_skip('seda:test-queue', expected_message_count=20000)
        eip_context.mock_endpoint_and_skip('seda:file-test-result-queue', expected_message_count=1000)
        eip_context.mock_endpoint_and_skip('seda:profile-test-failure-queue', expected_message_count=1000)

        eip_context.start_with_trigger(Process(target=touch, args=(trigger_file,)))

        exchanges = eip_context.get_endpoint('seda:file-test-result-queue').exchanges

        assert len(exchanges) == 1000

    finally:
      if os.path.exists(trigger_file):
        os.remove(trigger_file)
