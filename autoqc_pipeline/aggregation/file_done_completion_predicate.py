from autoqc_pipeline.routepy.framework.predicate import Predicate


class FileDoneCompletionPredicate(Predicate):
  def matches(self, exchange):
    return exchange.get_body().is_complete