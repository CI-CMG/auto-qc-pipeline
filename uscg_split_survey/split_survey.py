import sys
import os
from datetime import datetime

import numpy as np
import pandas as pd
import haversine

from uscg_split_survey.csv_header_reader import CsvHeaderReader


class SplitSurvey():

    def get_data_frame(self, file_path):
        print("Reading coordinates from file: " + file_path)
        data_frame = pd.read_csv(file_path)
        return data_frame


    def build_array(self, df, mapped_columns):
        arr = []

        for _, series in df.iterrows():
            arr.append(
                [
                    series[mapped_columns.lat_col],
                    series[mapped_columns.lon_col],
                    series[mapped_columns.depth_col],
                    series[mapped_columns.time_col].strip(),
                    datetime.strptime(series[mapped_columns.time_col].strip(), "%Y-%m-%dT%H:%M:%SZ").timestamp()
                ]
            )

        arr.sort(key=lambda x: x[4])

        return np.array(arr)

    def split(self, arr, max_time_s, max_dist_km, ):
        d = {}
        current_key = 1
        current_row = arr[0]
        arr = arr[1:]
        while len(arr) != 0:
            dist = np.abs(haversine.haversine_vector(current_row[0:2].astype(np.float64), arr[0:, 0:2].astype(np.float64), comb=True, unit=haversine.Unit.KILOMETERS))
            dist = np.reshape(dist, len(dist))
            time_diff = arr[0:,4].astype(np.float64) - current_row[4].astype(np.float64)

            res = arr[np.where(dist <= max_dist_km) and np.where(time_diff <= max_time_s)]
            arr = arr[np.where(dist > max_dist_km) and np.where(time_diff > max_time_s)]

            if current_key == 1 and len(d) == 0:
                print("New survey: (" +
                        str(current_row[0]) + ", " +
                        str(current_row[1]) + "," +
                        current_row[3] +
                ")")
                d[current_key] = np.array([current_row])
                d[current_key] = np.append(d[current_key], res, axis=0)
                current_row = res[-1]
                continue

            if len(res) != 0:
                d[current_key] = np.append(d[current_key], res, axis=0)
                current_row = res[-1]
            else:
                print("End of current survey: (" +
                        str(d[current_key][-1][0]) + ", " +
                        str(d[current_key][-1][1]) + "," +
                        d[current_key][-1][3] +
                ")")
                print("\n")
                current_key += 1
                current_row = arr[0]
                print("New survey: (" +
                        str(current_row[0]) + ", " +
                        str(current_row[1]) + "," +
                        current_row[3] +
                ")")
                arr = arr[1:]
                d[current_key] = np.array([current_row])
            if len(arr) == 0:
                print("End of current survey: (" +
                        str(d[current_key][-1][0]) + ", " +
                        str(d[current_key][-1][1]) + "," +
                        d[current_key][-1][3] +
                ")")
        return d

    def write_surveys(self, d, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        print("Writing " + str(len(d.keys())) + " surveys")
        for survey_number in d.keys():
            data = np.array(d[survey_number])
            output_data_frame = pd.DataFrame()
            output_data_frame['LON'] = data[:, 1]
            output_data_frame['LAT'] = data[:, 0]
            output_data_frame['DEPTH'] = data[:, 2]
            output_data_frame['TIME'] = data[:, 3]
            output_data_frame.to_csv(output_directory + "/data" + str(survey_number) + ".xyz", index=False)

    def get_columns(self, csv_file):
        return CsvHeaderReader(csv_file).get_mapped_columns()


    def run(self, csv_file, max_time_s, max_dist_km, output_dir):
        mapped_columns = self.get_columns(csv_file)
        data_frame = self.get_data_frame(csv_file)
        arr = self.build_array(data_frame, mapped_columns)
        max_time_s = np.float64(max_time_s) # one day
        max_dist_km = np.float64(max_dist_km)
        d = self.split(arr, max_time_s, max_dist_km)
        self.write_surveys(d, output_dir)
    
if __name__ == "__main__":
    split_survey = SplitSurvey()
    split_survey.run(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[2])
