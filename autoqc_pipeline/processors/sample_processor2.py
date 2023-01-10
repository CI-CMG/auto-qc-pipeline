from autoqc_pipeline.routepy.framework.processor import Processor


class SampleProcessor2(Processor):

  def process(self, exchange):
    print(exchange.get_body())