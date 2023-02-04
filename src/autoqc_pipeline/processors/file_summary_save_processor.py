import json
import os

from eipiphany_core.framework.base.processor import Processor


class FileSummarySaveProcessor(Processor):

  def __init__(self, output_dir):
    self.__output_dir = output_dir

  def process(self, exchange):
    file_summary = exchange.body
    results_dir = os.path.join(self.__output_dir, file_summary.file_path_prefix + "-QC")
    summary_file = os.path.join(results_dir, "summary.json")
    serialized = json.dumps(file_summary.__dict__)
    with open(summary_file, "w") as outfile:
      outfile.write(serialized)
    print("finished {}".format(file_summary.file_path_prefix))

