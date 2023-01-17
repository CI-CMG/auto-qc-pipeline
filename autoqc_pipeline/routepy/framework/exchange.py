
class Exchange:

  def __init__(self, body):
    self.__body = body
    self.__headers = {}

  def get_header(self, key):
    return self.__headers.get(key)

  def set_header(self, key, value):
    self.__headers[key] = value
    return self

  def get_body(self):
    return self.__body

  def set_body(self, body):
    self.__body = body
    return self
