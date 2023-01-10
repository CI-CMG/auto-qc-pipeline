from multiprocessing import Queue

from autoqc_pipeline.processors.sample_processor import SampleProcessor
from autoqc_pipeline.processors.sample_processor2 import SampleProcessor2
from autoqc_pipeline.routes.test_route import TestRoute

if __name__ == '__main__':

  queue = Queue()

  test_route = TestRoute(3, SampleProcessor(), Queue(), SampleProcessor2())
  test_route.build()
  joiners = test_route.start()

  for joiner in joiners:
    joiner.join()
