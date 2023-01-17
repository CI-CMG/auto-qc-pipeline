import multiprocessing
from datetime import datetime

from autoqc_pipeline.routepy.framework.processor import Processor


class SimpleTimestampProcessor(Processor):

  def process(self, exchange):
    process = multiprocessing.current_process()
    file = exchange.get_body().wod_file_path
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%M.%f")
    print("{0} {1} {2}".format(now, process.pid, file))