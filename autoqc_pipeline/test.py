from multiprocessing import JoinableQueue

from autoqc_pipeline.processors.sample_processor import SampleProcessor
from autoqc_pipeline.processors.sample_processor2 import SampleProcessor2
from autoqc_pipeline.routes.test_route import TestRoute

if __name__ == '__main__':

  test_route = TestRoute(3, SampleProcessor(), JoinableQueue(), SampleProcessor2())
  test_route.build()
  joiners = test_route.start()

  for joiner in joiners:
    joiner.join()
