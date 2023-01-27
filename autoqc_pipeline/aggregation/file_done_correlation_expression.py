from autoqc_pipeline.routepy.framework.expression import Expression
class FileDoneCorrelationExpression(Expression):
  def evaluate(self, exchange):
    return exchange.get_body().file_path_prefix


