from autoqc_pipeline.routepy.framework.processor import Processor


class QueueEndpoint(Processor):

  def __init__(self, queue, block_when_full=False):
    self.__queue = queue
    self.__block_when_full = block_when_full

  def process(self, exchange):
    self.__queue.put(exchange.get_body(), self.__block_when_full)