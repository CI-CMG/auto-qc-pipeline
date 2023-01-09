import csv

from uscg_split_survey.mapped_columns import MappedColumns


class CsvHeaderReader:

  def __init__(self, file):
    self.file = file

  def get_mapped_columns(self):
    with open(self.file, newline='') as csvfile:
      reader = csv.reader(csvfile)
      header = next(reader, None)
      if header:
        lon_col = None
        lat_col = None
        depth_col = None
        time_col = None
        i = 0
        for value in header:
          if value.strip().upper() == 'LON':
            lon_col = i
          elif value.strip().upper() == 'LAT':
            lat_col = i
          elif value.strip().upper() == 'DEPTH':
            depth_col = i
          elif value.strip().upper() == 'TIME':
            time_col = i
          i += 1
        mapped_columns = MappedColumns(lon_col, lat_col, depth_col, time_col)
        if not mapped_columns.is_valid():
          raise Exception("header is invalid")
        return mapped_columns
      else:
        raise Exception("file is empty")
