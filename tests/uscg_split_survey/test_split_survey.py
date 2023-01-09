import os
import shutil
import csv


from uscg_split_survey.split_survey import SplitSurvey

class TestSplitSurvey:
  def test_run(self):
    dir = 'target/output'
    if os.path.exists(dir):
      shutil.rmtree(dir)
    SplitSurvey().run('data/test.xyz', 86400, 1000, dir)
    dir_list = os.listdir(dir)
    dir_list.sort()
    expected_dir_list = ['data1.xyz', 'data2.xyz', 'data3.xyz', 'data4.xyz', 'data5.xyz', 'data6.xyz']
    assert dir_list == expected_dir_list
    header = None
    first_row = None
    with open(dir + '/data1.xyz', newline='') as csvfile:
      reader = csv.reader(csvfile)
      header = next(reader, None)
      first_row = next(reader, None)
    assert header == ['LON', 'LAT', 'DEPTH', 'TIME']
    assert abs(float(first_row[0]) - -149.3551) <= 0.001
    assert abs(float(first_row[1]) - 60.08506666666667) <= 0.001
    assert abs(float(first_row[2]) - 4.693977078761279) <= 0.001
    assert first_row[3] == '2020-04-10T21:36:34Z'