import os
from multiprocessing import Process

from eipiphany_core.framework.base.eip_context import EipContext
from eipiphany_core.framework.test_support.eip_test_context import \
  EipTestContext

from src.autoqc_pipeline.application.route_configurer import RouteConfigurer


def touch(trigger_file):
  with open(trigger_file, 'a') as f: pass

class TestFileRoute(object):


#   public void testConsumeFile() throws Exception {
#     Path doneFile = Paths.get("src/test/resources/wod18/MRB/OBS/MRBO2022.gz.autoqc");
#   try {
#   testCastQueue.expectedMessageCount(3);
#   Files.createFile(doneFile);
#   testCastQueue.assertIsSatisfied();
#   List<AutoQcTestContextImpl> messages = testCastQueue.getReceivedExchanges().stream()
#   .map(e -> e.getIn().getBody(AutoQcTestContextImpl.class))
#   .sorted(Comparator.comparing(tc -> tc.getCast().getCastNumber()))
#   .collect(Collectors.toList());
#
#   assertFalse(Files.exists(doneFile));
#   assertTrue(Files.exists(Paths.get("src/test/resources/wod18/MRB/OBS/MRBO2022.gz")));
#
#   assertEquals(21418924, messages.get(0).getCast().getCastNumber());
#   assertEquals(21418925, messages.get(1).getCast().getCastNumber());
#   assertEquals(21418926, messages.get(2).getCast().getCastNumber());
#
#   assertEquals("MRB/OBS/MRBO2022", messages.get(0).getFilePathPrefix());
#   assertEquals("MRB/OBS/MRBO2022", messages.get(1).getFilePathPrefix());
#   assertEquals("MRB/OBS/MRBO2022", messages.get(2).getFilePathPrefix());
#
#   assertFalse(messages.get(0).isLastCast());
#   assertFalse(messages.get(1).isLastCast());
#   assertTrue(messages.get(2).isLastCast());
#
#   CastProcessingContext context = fileController.getContext("MRB/OBS/MRBO2022");
#   assertEquals(new HashSet<>(Arrays.asList(21418924, 21418925, 21418926)), context.getCasts());
#   assertTrue(context.isComplete());
#
#   } finally {
#     Files.deleteIfExists(doneFile);
#   }
# }





  def test_consume_file(self):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']


    wod_directory = os.path.join(project_root, 'test-resources', 'wod18')
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    output_directory = os.path.join(project_root, 'test-dir')
    auto_qc_home = os.path.join(project_root, "..", "AutoQC")
    concurrent_unzip_files = 1
    test_concurrency = 1

    trigger_file = os.path.join(wod_directory, 'MRB', 'OBS', 'MRBO2022.gz.autoqc')

    with EipTestContext(EipContext()) as eip_context:
      route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
                                     gunzip_directory, output_directory,
                                     concurrent_unzip_files, test_concurrency)
      route_config.configure()

      eip_context.mock_endpoint_and_skip('seda:test-queue', expected_message_count=2)

      # TODO
      # assertFalse(Files.exists(doneFile));
      # assertTrue(Files.exists(Paths.get("src/test/resources/wod18/MRB/OBS/MRBO2022.gz")));

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

      # TODO
      # CastProcessingContext context = fileController.getContext("MRB/OBS/MRBO2022");
      # assertEquals(new HashSet<>(Arrays.asList(21418924, 21418925, 21418926)), context.getCasts());
      # assertTrue(context.isComplete());


