from eipiphany_core.framework.base.filter import Filter
from profile_filter import ProfileFilter


class PathologicalProfilesFilter(Filter):

  def __init__(self):
    self.__filter = ProfileFilter()

  def filter(self, exchange):
    auto_qc_test_message = exchange.body
    return self.__filter.assess_profile(auto_qc_test_message.profile)