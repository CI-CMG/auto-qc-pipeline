import json
import os

from eipiphany_core.framework.base.processor import Processor


class ProfileFailureSaveProcessor(Processor):

  def __init__(self, output_dir):
    self.__output_dir = output_dir

  def process(self, exchange):
    test_message = exchange.body
    results_dir = os.path.join(self.__output_dir, test_message.file_path_prefix + "-QC")
    summary_file = os.path.join(results_dir, str(test_message.profile.uid()) + "-failures.json")
    depth_failures = []
    for depth_failure in test_message.profile_test_result.depth_failures:
      depth_failures.append(list(depth_failure))
    json_obj = {
      'exception': test_message.profile_test_result.exception,
      'iquodFlags': test_message.profile_test_result.iquod_flags,
      'profileFailures': list(test_message.profile_test_result.profile_failures),
      'depthFailures': depth_failures
    }
    serialized = json.dumps(json_obj)
    with open(summary_file, "w") as outfile:
      outfile.write(serialized)

