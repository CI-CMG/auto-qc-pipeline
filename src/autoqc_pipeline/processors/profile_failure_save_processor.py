import json
import os

from eipiphany_core.framework.base.processor import Processor


class ProfileFailureSaveProcessor(Processor):

  def __init__(self, output_dir):
    self.__output_dir = output_dir

  def process(self, exchange):
    test_message = exchange.body
    results_dir = os.path.join(self.__output_dir, test_message.file_path_prefix + "-QC")
    summary_file = os.path.join(results_dir, test_message.profile.uid() + "-failures.json")
    serialized = json.dumps(test_message.profile_test_result__dict__)
    with open(summary_file, "w") as outfile:
      outfile.write(serialized)

