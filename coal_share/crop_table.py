"""
Crop table to reduce previous years. Source for table: https://ourworldindata.org/grapher/share-electricity-coal.

"""

import csv

WORLD_2021_SHARE = 35.9863166809082
first_row = ['Afghanistan', 'AFG', '2001', '0']
last_row = ['Zimbabwe', '30.963096618652344']

prev_row = first_row


with open('share-electricity-coal-01-09-2022.csv', 'r') as f_r:
    with open('share-electricity-coal-01-09-2022_cropped.csv', 'w', newline='') as f_w:

        csv_orig = csv.reader(f_r)
        csv_cropped = csv.writer(f_w, delimiter=',')

        for row in csv_orig:
            if row[0] != prev_row[0]:
                if float(prev_row[3]) == 0.0:
                    cropped_row = [prev_row[0], WORLD_2021_SHARE]
                else:
                    cropped_row = [prev_row[0], float(prev_row[3])]
                csv_cropped.writerow(cropped_row)

            prev_row = row

        csv_cropped.writerow(last_row)
