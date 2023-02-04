
class ProfileTestResult(object):
  def __init__(self, profile):
    self.__profile_failures = set() # of strings
    self.__depth_failures = [] # of profile_failures
    for i in range(profile.n_levels()):
      self.__depth_failures.append(set())
    self.skipped = False
    self.exception = None
    self.iquod_flags = None

  @property
  def profile_failures(self):
    return self.__profile_failures

  @property
  def depth_failures(self):
    return self.__depth_failures

  @property
  def failed(self):
    return len(self.__profile_failures) or self.exception


class TestMessage(object):
  def __init__(self, file_path_prefix, profile, last_profile, geohash):
    self.__profile = profile
    self.__profile_test_result = ProfileTestResult(profile)
    self.__file_path_prefix = file_path_prefix
    self.__last_profile = last_profile
    self.__geohash = geohash

  @property
  def geohash(self):
    return self.__geohash

  @property
  def profile(self):
    return self.__profile

  @property
  def profile_test_result(self):
    return self.__profile_test_result

  @property
  def file_path_prefix(self):
    return self.__file_path_prefix

  @property
  def last_profile(self):
    return self.__last_profile

  def get_failure_file_name(self):
    return self.__file_path_prefix + "-failures-" + self.__profile.uid() + ".json"


