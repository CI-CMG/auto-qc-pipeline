import multiprocessing
from time import sleep

from autoqc_pipeline.routepy.framework.processor import Processor


class SampleProcessor2(Processor):

  def process(self, exchange):
    process = multiprocessing.current_process()
    for i in range(100):
      sleep(1)
      print("{0} {1}".format(process.pid,exchange.get_body()))