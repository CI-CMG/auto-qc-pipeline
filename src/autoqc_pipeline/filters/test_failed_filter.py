from eipiphany_core.framework.base.filter import Filter


class TestFailedFilter(Filter):

  def filter(self, exchange):
    test_message = exchange.body
    return test_message.profile_test_result.failed
