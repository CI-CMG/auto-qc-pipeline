from autoqc_pipeline.routepy.component.queue_endpoint import QueueEndpoint
from autoqc_pipeline.routepy.component.queue_source import QueueSource
from autoqc_pipeline.routepy.component.time_interval_source import TimeIntervalSource
from autoqc_pipeline.routepy.framework.route_builder import RouteBuilder


class TestRoute(RouteBuilder):


  def __init__(self, interval_seconds, sample_processor, sample_queue, sample_processor2, *args, **kw):
    super().__init__(*args, **kw)
    self.__interval_seconds = interval_seconds
    self.__sample_processor = sample_processor
    self.__sample_queue = sample_queue
    self.__sample_processor2 = sample_processor2;

  def build(self):
    self.comes_from(TimeIntervalSource(self.__interval_seconds)).to(self.__sample_processor).to(QueueEndpoint(self.__sample_queue))
    self.comes_from(QueueSource(self.__sample_queue, concurrent_consumers=3)).to(self.__sample_processor2)
