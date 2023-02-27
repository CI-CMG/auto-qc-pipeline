import os
import shutil

from src.autoqc_pipeline.services.geohash_service import GeohashService

class MockProfile(object):
  def __init__(self, longitude, latitude, date, uid, cruise):

    self.__longitude = longitude
    self.__latitude = latitude
    self.__year = date[0]
    self.__month = date[1]
    self.__day = date[2]
    self.__uid = uid
    self.__cruise = cruise

  def longitude(self):
    return self.__longitude

  def latitude(self):
    return self.__latitude

  def year(self):
    return self.__year

  def month(self):
    return self.__month

  def day(self):
    return self.__day

  def uid(self):
    return self.__uid

  def cruise(self):
    return self.__cruise

class TestGeohashService(object):

  def setup_method(self, method):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    shutil.rmtree(gunzip_directory, ignore_errors=True)

  def teardown_method(self, method):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    shutil.rmtree(gunzip_directory, ignore_errors=True)

  def test_get_adjacent(self):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    geohash_service = GeohashService(gunzip_directory)
    assert geohash_service.get_adjacent(geohash='xzxfr', direction='right') == '8p842'
    assert geohash_service.get_adjacent(geohash='8p842', direction='left') == 'xzxfr'

  def test_get_geohash(self):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root,'gunzip-dir')
    geohash_service = GeohashService(gunzip_directory)
    assert geohash_service.get_geohash(10.40744,57.64911) == "u4pru"
    assert geohash_service.get_geohash(180,0) == "rzzzz"
    assert geohash_service.get_geohash(-180,0) == "2pbpb"

  def test_append_read_to_geohash_file(self):

    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root,'gunzip-dir')
    geohash_service = GeohashService(gunzip_directory)
    file_path_prefix = "MRB/OBS/MRBO1995"

    long = 126.5
    lat = 28.1667
    temp = [2,5.0001,2]
    depth = [1000,2000,3000]
    profile0 = MockProfile(longitude=long, latitude=lat, date=[1995, 7, 8, 0], uid=7282830, cruise=1000)
    profile1 = MockProfile(longitude=long, latitude=lat, date=[1995, 7, 8, 0], uid=7282831, cruise=2000)
    profile2 = MockProfile(longitude=long, latitude=lat, date=[1995, 7, 8, 0], uid=7282832, cruise=3000)
    geohash = geohash_service.get_geohash(profile1.longitude(),profile1.latitude())
    parent = os.path.join(gunzip_directory, file_path_prefix + '.geohash', geohash)

    # test append_to_geohash_file
    offset0 = 891
    offset1 = 1134
    offset2 = 3342
    geohash_service.append_to_geohash_file(file_path_prefix, profile0, geohash, offset0)
    assert os.path.exists(parent) == True
    geohash_service.append_to_geohash_file(file_path_prefix, profile1, geohash, offset1)
    geohash_file = geohash_service.read_geohash_file(file_path_prefix, profile0, geohash)
    assert geohash_file[0].uid == profile0.uid()
    assert geohash_file[0].offset == offset0
    assert geohash_file[0].cruise == profile0.cruise()

    assert geohash_file[1].uid == profile1.uid()
    assert geohash_file[1].offset == offset1
    assert geohash_file[1].cruise == profile1.cruise()

    geohash_service.append_to_geohash_file(file_path_prefix, profile2, geohash, offset2)
    geohash_file = geohash_service.read_geohash_file(file_path_prefix, profile0, geohash)
    assert geohash_file[2].uid == profile2.uid()
    assert geohash_file[2].offset == offset2
    assert geohash_file[2].cruise == profile2.cruise()


  def test_get_hashes_to_check(self):
    project_root = os.environ['AUTO_QC_PIPELINE_ROOT']
    gunzip_directory = os.path.join(project_root, 'gunzip-dir')
    geohash_service = GeohashService(gunzip_directory)
    geohash='xzxfr'
    ring_offset = 2
    hashes = geohash_service.get_hashes_to_check(geohash, ring_offset)
    left_lon_hashes=['xzxft', 'xzxcv', 'xzxfm', 'xzxfv', 'xzxfj']
    right_lon_hashes=['8p849', '8p84c', '8p81c', '8p841', '8p843']
    top_lat_hashes=['xzxfy', '8p84c', 'xzxfz', '8p84b', 'xzxfv']
    bottom_lat_hashes=['xzxcy', 'xzxcz', 'xzxcv', '8p81c', '8p81b']
    geohashes = set(left_lon_hashes + right_lon_hashes + top_lat_hashes + bottom_lat_hashes)
    assert hashes == geohashes

