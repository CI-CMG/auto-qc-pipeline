import csv
import os
from pathlib import Path

import pygeohash as pgh

class GeohashRecord(object):
  def __init__(self, row):
    self.__cruise = int(row[0])
    self.__uid = int(row[1])
    self.__offset = int(row[2])
    self.__longitude = float(row[3])
    self.__latitude = float(row[4])

  @property
  def cruise(self):
    return self.__cruise

  @property
  def uid(self):
    return self.__uid

  @property
  def offset(self):
    return self.__offset

  @property
  def longitude(self):
    return self.__longitude

  @property
  def latitude(self):
    return self.__latitude

class GeohashService(object):

  def __init__(self, gunzip_directory):
    self.__gunzip_directory = gunzip_directory

  def __resolve_hash_file(self, file_path_prefix, geohash, year, month):
    hash_dir = os.path.join(self.__gunzip_directory, file_path_prefix + '.geohash')
    return os.path.join(hash_dir, geohash, str(year), str(month) + ".csv")


  def read_geohash_file(self, file_path_prefix, p, geohash):
    hash_file = self.__resolve_hash_file(file_path_prefix, geohash, p.year(), p.month())
    result = []
    if os.path.exists(hash_file):
      with open(hash_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
          result.append(GeohashRecord(row))
    return result


  def append_to_geohash_file(self, file_path_prefix, p, geohash, offset):
    hash_file = self.__resolve_hash_file(file_path_prefix, geohash, p.year(), p.month())
    parent = os.path.split(hash_file)[0]
    if not os.path.exists(parent):
      Path(parent).mkdir( parents=True, exist_ok=True )

    mode = 'w'
    if os.path.exists(hash_file):
      mode = 'a'

    with open(hash_file, mode, newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([str(p.cruise()), str(p.uid()), str(offset), str(p.longitude()), str(p.latitude())])

  def get_geohash(self, lon, lat):
    return pgh.encode(latitude=lat, longitude=lon, precision=5)

  def __get_opposite(self, direction):
    if direction == 'right':
      return 'left'
    if direction == 'left':
      return 'right'
    if direction == 'top':
      return 'bottom'
    if direction == 'bottom':
      return 'top'
    raise Exception("invalid direction: " + direction)

  def __naive_around_world(self, geohash, direction):
    dir = self.__get_opposite(direction)
    adj = geohash
    while True:
      try:
        adj = pgh.get_adjacent(geohash=adj, direction=dir)
      except ValueError:
        return adj


  def get_adjacent(self, geohash, direction):
    try:
      adj = pgh.get_adjacent(geohash=geohash, direction=direction)
    except ValueError:
      if direction in {'left', 'right'}:
        adj = self.__naive_around_world(geohash, direction)
      else:
        adj = None
    return adj

  def __get_latitude_ring(self, geohash):
    ring = [geohash]
    current_hash = self.get_adjacent(geohash, 'right')
    while current_hash != geohash:
      ring.append(current_hash)
      current_hash = self.get_adjacent(geohash, 'right')
    return ring

  def __get_latitude_hashes(self, center, size):
    geohashes = {center}
    geohash = center
    for i in range(int(size / 2)):
      geohash = self.get_adjacent(geohash, 'left')
      geohashes.add(geohash)
    geohash = center
    for i in range(int(size / 2)):
      geohash = self.get_adjacent(geohash, 'right')
      geohashes.add(geohash)
    return geohashes

  def __get_longitude_hashes(self, center, size):
    geohashes = {center}
    geohash = center
    for i in range(int(size / 2)):
      geohash = self.get_adjacent(geohash, 'top')
      if geohash:
        geohashes.add(geohash)
      else:
        break
    geohash = center
    for i in range(int(size / 2)):
      geohash = self.get_adjacent(geohash, 'bottom')
      if geohash:
        geohashes.add(geohash)
      else:
        break
    return geohashes


  def get_hashes_to_check(self, geohash, ring_offset):
    hashes = set()
    last_top = None
    top = geohash
    last_bottom = None
    bottom = geohash
    left = geohash
    right = geohash
    for i in range(ring_offset):
      left = self.get_adjacent(left, 'left')
      right = self.get_adjacent(right, 'right')
      if top:
        top = self.get_adjacent(top, 'top')
        if top:
          last_top = top
      if bottom:
        bottom = self.get_adjacent(bottom, 'bottom')
        if bottom:
          last_bottom = bottom
    size = (ring_offset * 2) + 1

    for ghash in self.__get_longitude_hashes(left, size):
      hashes.add(ghash)

    for ghash in self.__get_longitude_hashes(right, size):
      hashes.add(ghash)

    if top:
      for ghash in self.__get_latitude_hashes(top, size):
        hashes.add(ghash)
    else:
      for ghash in self.__get_latitude_ring(last_top):
        hashes.add(ghash)


    if bottom:
      for ghash in self.__get_latitude_hashes(bottom, size):
        hashes.add(ghash)
    else:
      for ghash in self.__get_latitude_ring(last_bottom):
        hashes.add(ghash)

    return hashes
