from autoqc_pipeline.routepy.framework.joiner import Joiner


class ProcessJoiner(Joiner):

  def __init__(self, consumer_process):
    self.__consumer_process = consumer_process

  def join(self):
    self.__consumer_process.join()