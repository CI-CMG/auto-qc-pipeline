from eipiphany_core.framework.base.processor import Processor
from wodpy import wod


class GeohashProcessor(Processor):

  def __init__(self, geohash_service, filter):
    self.__geohash_service = geohash_service
    self.__filter = filter

  def process(self, exchange):
    file_message = exchange.body
    file_path_prefix = file_message.file_path_prefix
    with open(file_message.wod_file_path, 'r') as fid:
      while True:
        offset = fid.tell()
        profile = wod.WodProfile(fid)
        if self.__filter.assess_profile(profile):
          geohash = self.__geohash_service.get_geohash(profile.longitude(), profile.latitude())
          self.__geohash_service.append_to_geohash_file(file_path_prefix, profile, geohash, offset)
        if profile.is_last_profile_in_file(fid):
          break

