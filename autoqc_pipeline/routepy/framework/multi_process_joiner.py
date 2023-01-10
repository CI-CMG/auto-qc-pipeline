from autoqc_pipeline.routepy.framework.joiner import Joiner


class MultiProcessJoiner(Joiner):

  def __init__(self, consumer_process_list):
    self.__consumer_process_list = consumer_process_list

  def join(self):
    for consumer_process in self.__consumer_process_list:
      consumer_process.join()