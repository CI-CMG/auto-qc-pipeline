from datetime import datetime
from multiprocessing import Process
from time import sleep

from autoqc_pipeline.routepy.framework.exchange import Exchange
from autoqc_pipeline.routepy.framework.process_joiner import ProcessJoiner
from autoqc_pipeline.routepy.framework.source import Source



class TimeIntervalSource(Source):

  def __init__(self, interval_seconds):
    self.__interval_seconds = interval_seconds
    self.__source_wrapper = None

  def set_source_wrapper(self, source_wrapper):
    self.__source_wrapper = source_wrapper

  def start(self):
    p = Process(target=self.__source_wrapper.wait_for_events)
    p.daemon = True
    p.start()
    return ProcessJoiner(p)

  def wait_for_event(self):
    sleep(self.__interval_seconds)
    return Exchange(datetime.now())

  def event_success(self, exchange):
    pass

  def event_failure(self, err, exchange):
    print(f"Unexpected {err=}, {type(err)=}")
    pass



