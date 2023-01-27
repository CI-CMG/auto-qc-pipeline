import os

from autoqc_pipeline.model.auto_qc_message import AutoQcMessage
from autoqc_pipeline.routepy.framework.processor import Processor


class MessagePrepProcessor(Processor):

  def process(self, exchange):
    path_list = exchange.get_body().split("/")
    file_path_prefix = os.path.join(path_list[-3], path_list[-2],path_list[-1][:-3])
    exchange.set_body(AutoQcMessage().set_gzip_file_path(exchange.get_body()).set_file_path_prefix(file_path_prefix))
