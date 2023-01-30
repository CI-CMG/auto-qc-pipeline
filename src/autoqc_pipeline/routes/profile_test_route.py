from eipiphany_core.component.error_handler.dead_letter_channel import \
  DeadLetterChannel
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_seda.component.queue_endpoint import QueueEndpoint
from eipiphany_seda.component.queue_source import QueueSource


class ProfileTestRoute(RouteBuilder):

  def __init__(self, test_concurrency, error_queue, dlq_prep_processor,
      profile_test_failure_queue, file_test_result_queue, test_queue,
      test_processor, iquod_flag_processor, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_concurrency = test_concurrency
    self.__error_queue = error_queue
    self.__dlq_prep_processor = dlq_prep_processor
    self.__profile_test_failure_queue = profile_test_failure_queue
    self.__file_test_result_queue = file_test_result_queue
    self.__test_queue = test_queue
    self.__test_processor = test_processor
    self.__iquod_flag_processor = iquod_flag_processor


  def build(self):

    self._error_handler(DeadLetterChannel(QueueEndpoint(self.__error_queue, block_when_full=True)).on_prepare_failure(self.__dlq_prep_processor))

    # todo add choice to eipiphany to use filter in route definition instead of in test processor
    self._from(
      QueueSource(self.__test_queue, concurrent_consumers=self.__test_concurrency))\
      .to(self.__test_processor)\
      .to(self.__iquod_flag_processor)\
      .to(QueueEndpoint(self.__profile_test_failure_queue, block_when_full=True))\
      .to(QueueEndpoint(self.__file_test_result_queue, block_when_full=True)) # aggregator queue
