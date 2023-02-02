from test_data_store import TestDataStore


class DictionaryDataStore(TestDataStore):

  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)
    self.__data = {}

  def is_prepared(self, key):
    return True

  def prepare(self, key, field_list):
    pass

  def put(self, uid, key, field_dict):
    self.__data[key] = field_dict

  def get(self, uid, key):
    return self.__data.get(key)