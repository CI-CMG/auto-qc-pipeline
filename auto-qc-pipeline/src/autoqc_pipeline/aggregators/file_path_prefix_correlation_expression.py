from eipiphany_core.framework.base.expression import Expression


class FilePathPrefixCorrelationExpression(Expression):
  def evaluate(self, exchange):
    auto_qc_test_message = exchange.body
    return auto_qc_test_message.file_path_prefix
