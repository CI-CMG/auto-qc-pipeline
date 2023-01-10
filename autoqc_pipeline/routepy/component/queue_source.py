from multiprocessing import Process

from autoqc_pipeline.routepy.framework.exchange import Exchange
from autoqc_pipeline.routepy.framework.multi_process_joiner import \
  MultiProcessJoiner
from autoqc_pipeline.routepy.framework.process_joiner import ProcessJoiner
from autoqc_pipeline.routepy.framework.source import Source




class QueueSource(Source):

  def __init__(self, queue, concurrent_consumers=1):
    self.__queue = queue
    self.__concurrent_consumers = concurrent_consumers
    self.__source_wrapper = None

  def set_source_wrapper(self, source_wrapper):
    self.__source_wrapper = source_wrapper

  def start(self):
    consumer_process = []
    for i in range(self.__concurrent_consumers):
      p = Process(target=self.__source_wrapper.wait_for_events)
      p.daemon = True
      p.start()
      consumer_process.append(p)
    return MultiProcessJoiner(consumer_process)

  def wait_for_event(self):
    return Exchange(self.__queue.get())

  def event_success(self):
    self.__queue.task_done()
    pass

  def event_failure(self, err):
    self.__queue.task_done()
    print(f"Unexpected {err=}, {type(err)=}")
    pass

