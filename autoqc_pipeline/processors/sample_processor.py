from autoqc_pipeline.routepy.framework.processor import Processor


class SampleProcessor(Processor):

  def process(self, exchange):
    current_time = exchange.get_body().strftime("%H:%M:%S")
    exchange.set_body("Current Time = " + current_time)