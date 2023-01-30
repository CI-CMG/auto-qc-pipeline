from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext
from eipiphany_core.framework.test_support.eipiphany_test_context import \
  EipiphanyTestContext

from src.autoqc_pipeline.application.route_configurer import RouteConfigurer


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
    wod_directory = 'test-resources/wod18'
    gunzip_directory = 'gunzip-dir'
    output_directory = 'test-dir'
    auto_qc_home = "../AutoQC"
    concurrent_unzip_files = 2
    test_concurrency = 2

    done_file = 'test-resources/wod18/MRB/OBS/MRBO2022.gz.autoqc'

    # with EipiphanyTestContext(EipiphanyContext()) as eip_context:
    #   route_config = RouteConfigurer(eip_context, wod_directory, auto_qc_home,
    #                                  gunzip_directory, output_directory,
    #                                  concurrent_unzip_files, test_concurrency)
    #   route_config.configure()
    #
    #   file_cntroller = route_config.file_controller
    #
    #   eip_context.start()
