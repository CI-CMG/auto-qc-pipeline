import json
import os

from eipiphany_core.framework.base.processor import Processor


class ProfileFailureSaveProcessor(Processor):

  def __init__(self, output_dir):
    self.__output_dir = output_dir

  def process(self, exchange):
    test_message = exchange.body
    summary_file = os.path.join(self.__output_dir, test_message.get_failure_file_name())
    serialized = json.dumps(file_summary.__dict__)
    with open(summary_file, "w") as outfile:
      outfile.write(serialized)

