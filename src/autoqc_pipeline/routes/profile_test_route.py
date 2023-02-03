from eipiphany_core.framework.base.route_builder import RouteBuilder

from ..filters.pathological_profile_filter import PathologicalProfilesFilter
from ..processors.iquod_flag_processor import IquodFlagProcessor
from ..processors.profile_test_processor import ProfileTestProcessor
from ..processors.test_catalog import TestCatalog


class ProfileTestRoute(RouteBuilder):

  def __init__(self, auto_qc_home, profile_test_processor, test_catalog, file_controller, *args, **kw):
    super().__init__(*args, **kw)
    self.__auto_qc_home = auto_qc_home
    self.__test_catalog = test_catalog
    self.__profile_test_processor = profile_test_processor
    self.__file_controller = file_controller


  def build(self, eip_context):

    self._error_handler(DeadLetterChannel(eip_context, 'seda:error-queue').on_prepare_failure(TestErrorDlqPrepProcessor()))

    # todo add choice to eipiphany to use filter in route definition instead of in test processor
    self._from(eip_context, 'seda:test-queue')\
      .process(ProfileTestProcessor(self.__auto_qc_home, self.__file_controller, PathologicalProfilesFilter(), self.__test_catalog))\
      .process(IquodFlagProcessor(self.__test_catalog))\
      .to(eip_context, 'seda:profile-test-failure-queue')\
      .to(eip_context, 'seda:file-test-result-queue') # aggregator queue
