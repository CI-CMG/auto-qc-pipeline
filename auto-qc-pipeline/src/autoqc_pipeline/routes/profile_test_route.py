from eipiphany_core.framework.base.dead_letter_channel import DeadLetterChannel
from eipiphany_core.framework.base.route_builder import RouteBuilder

from autoqc_pipeline.processors.iquod_flag_processor import IquodFlagProcessor
from autoqc_pipeline.processors.test_error_dlq_prep_processor import TestErrorDlqPrepProcessor


class ProfileTestRoute(RouteBuilder):

  def __init__(self, auto_qc_home, profile_test_processor, test_catalog, *args, **kw):
    super().__init__(*args, **kw)
    self.__auto_qc_home = auto_qc_home
    self.__test_catalog = test_catalog
    self.__profile_test_processor = profile_test_processor


  def build(self, eip_context):

    self._error_handler(DeadLetterChannel(eip_context, 'seda:error-queue').on_prepare_failure(TestErrorDlqPrepProcessor()))

    self._from(eip_context, 'seda:test-queue')\
      .process(self.__profile_test_processor)\
      .process(IquodFlagProcessor(self.__test_catalog))\
      .to(eip_context, 'seda:profile-test-failure-queue')\
      .to(eip_context, 'seda:file-test-result-queue') # aggregator queue
