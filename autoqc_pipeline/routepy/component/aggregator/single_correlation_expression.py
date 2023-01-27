from autoqc_pipeline.routepy.framework.expression import Expression


class SingleCorrelationExpression(Expression):

  def evaluate(self, exchange):
    return 1