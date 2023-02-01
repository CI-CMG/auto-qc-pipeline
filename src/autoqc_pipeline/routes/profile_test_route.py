from eipiphany_core.framework.base.route_builder import RouteBuilder

from ..filters.pathological_profile_filter import PathologicalProfilesFilter
from ..processors.iquod_flag_processor import IquodFlagProcessor
from ..processors.profile_test_processor import ProfileTestProcessor
from ..processors.test_catalog import TestCatalog


class ProfileTestRoute(RouteBuilder):

  def __init__(self, auto_qc_home, *args, **kw):
    super().__init__(*args, **kw)
    self.__auto_qc_home = auto_qc_home
    self.__test_catalog = TestCatalog()


  def build(self, eip_context):

    # self._error_handler(DeadLetterChannel(QueueEndpoint(self.__error_queue, block_when_full=True)).on_prepare_failure(self.__dlq_prep_processor))

    # todo add choice to eipiphany to use filter in route definition instead of in test processor
    self._from(eip_context, 'seda:test-queue')\
      .process(ProfileTestProcessor(self.__auto_qc_home, PathologicalProfilesFilter(), self.__test_catalog))\
      .process(IquodFlagProcessor(self.__test_catalog))\
      .to(eip_context, 'seda:profile-test-failure-queue')\
      .to(eip_context, 'seda:file-test-result-queue') # aggregator queue
