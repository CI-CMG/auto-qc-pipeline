import os

from buddy_finder import BuddyFinder, Buddy
from wodpy import wod


class BuddyPair(object):
  def __init__(self, buddy, profile_offset):
    self.__buddy = buddy
    self.__profile_offset = profile_offset

  @property
  def buddy(self):
    return self.__buddy

  @property
  def profile_offset(self):
    return self.__profile_offset

class GeohashBuddyFinder(BuddyFinder):
  MAX_RINGS = 100

  def __init__(self, geohash_service, gunzip_directory, test_message):
    self.__geohash_service = geohash_service
    self.__test_message = test_message
    self.__gunzip_directory = gunzip_directory

  def __check_hash_file(self, geohash, max_distance):
    p = self.__test_message.profile
    profile_offset = None
    min_buddy = None

    records = self.__geohash_service.read_geohash_file(self.__test_message.file_path_prefix, p, geohash)
    for record in records:
      cruise = record.cruise
      uid = record.uid
      offset = record.offset
      longitude = record.longitude
      latitude = record.latitude
      buddy = Buddy(uid, p.year(), p.month(), cruise, latitude, longitude)
      pDist = self._assessBuddyDistance(p, buddy)
      if (pDist is not None) and (not min_buddy or pDist < min_buddy.distance):
          min_buddy = buddy
          min_buddy.distance = pDist
          profile_offset = offset

      if min_buddy and min_buddy.distance > max_distance:
        min_buddy = None

    if not min_buddy:
      return None
    return BuddyPair(min_buddy, profile_offset)

  def __load_buddy(self, buddy_pair):
    wod_file = os.path.join(self.__gunzip_directory, self.__test_message.file_path_prefix)
    buddy = buddy_pair.buddy
    with open(wod_file, 'r') as fid:
        fid.seek(buddy_pair.profile_offset)
        buddy.profile = wod.WodProfile(fid)
    return buddy

  def find_buddy(self, p, max_distance, parameters):
    buddy_pair_in_geohash = self.__check_hash_file(self.__test_message.geohash, max_distance)
    # always check at least 1 ring in case profile is near edge and closest is in neighbor
    buddy_pair_in_ring = None
    for i in range(1, (GeohashBuddyFinder.MAX_RINGS + 1)):
      ring = self.__geohash_service.get_hashes_to_check(
        self.__test_message.geohash, i)
      for geohash in ring:
        bp = self.__check_hash_file(geohash, max_distance)
        if bp and (not buddy_pair_in_ring or bp.buddy.distance < buddy_pair_in_ring.buddy.distance):
          buddy_pair_in_ring = bp
      if buddy_pair_in_ring:
        break

    if not buddy_pair_in_geohash and not buddy_pair_in_ring:
      return None

    buddy_pair = None
    if not buddy_pair_in_geohash:
      buddy_pair = buddy_pair_in_ring
    elif not buddy_pair_in_ring:
      buddy_pair = buddy_pair_in_geohash
    elif buddy_pair_in_ring.buddy.distance < buddy_pair_in_geohash.buddy.distance:
      buddy_pair = buddy_pair_in_ring
    else:
      buddy_pair = buddy_pair_in_geohash

    return self.__load_buddy(buddy_pair)

