"""
Crop table to reduce previous years. Source for table: https://ourworldindata.org/grapher/share-electricity-coal.

"""

import csv

WORLD_2021_SHARE = 35.9863166809082
prev_year = 0


with open('share-electricity-coal-01-09-2022.csv', 'r') as f_r:
    with open('share-electricity-coal-01-09-2022_cropped.csv', 'w', newline='') as f_w:

        csv_orig = csv.reader(f_r)
        csv_cropped = csv.writer(f_w, delimiter=',')

        for row in csv_orig:
            if int(row[2]) < prev_year:
                if float(row[3]) == 0.0:
                    cropped_row = [row[0], WORLD_2021_SHARE]
                else:
                    cropped_row = [row[0], float(row[3])]
                csv_cropped.writerow(cropped_row)

            prev_year = int(row[2])



