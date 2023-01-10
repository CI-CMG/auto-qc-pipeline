from multiprocessing import Process

from autoqc_pipeline.routepy.framework.exchange import Exchange
from autoqc_pipeline.routepy.framework.process_joiner import ProcessJoiner
from autoqc_pipeline.routepy.framework.source import Source




class QueueSource(Source):

  def __init__(self, queue):
    self.__queue = queue
    self.__source_wrapper = None
    self.__consumer_process = None

  def set_source_wrapper(self, source_wrapper):
    self.__source_wrapper = source_wrapper

  def start(self):
    self.__consumer_process = Process(target=self.__source_wrapper.wait_for_events)
    self.__consumer_process.start()
    return ProcessJoiner(self.__consumer_process)

  def wait_for_event(self):
    return Exchange(self.__queue.get())

