from autoqc_pipeline.routepy.framework.processor import Processor


class QueueEndpoint(Processor):

  def __init__(self, queue):
    self.__queue = queue

  def process(self, exchange):
    self.__queue.put(exchange.get_body())