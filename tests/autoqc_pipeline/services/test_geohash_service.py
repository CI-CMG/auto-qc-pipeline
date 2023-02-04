import os
import shutil

from src.autoqc_pipeline.services.geohash_service import GeohashService


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

