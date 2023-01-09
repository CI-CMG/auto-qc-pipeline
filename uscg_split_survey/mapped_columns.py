
class MappedColumns:

  def __init__(self, lon_col, lat_col, depth_col, time_col):
    self.lon_col = lon_col
    self.lat_col = lat_col
    self.depth_col = depth_col
    self.time_col = time_col

  def __members(self):
    return (self.lon_col, self.lat_col, self.depth_col, self.time_col)

  def __eq__(self, other):
    if type(other) is type(self):
      return self.__members() == other.__members()
    else:
      return False

  def __hash__(self):
    return hash(self.__members())

  def is_valid(self):
    return self.lon_col != None and self.lat_col != None and self.depth_col != None and self.time_col != None



