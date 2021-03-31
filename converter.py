
import sys
import csv

if len(sys.argv) < 3:
    print("please specify moodle and gtm files as arguments")
    exit(1)

moodle = sys.argv[1]
moodle_headers = []
moodle_rows = []
moodle_email_col_index = -1

gtm = sys.argv[2]
gtm_headers = []
gtm_rows = []
gtm_user_col_index = -1
gtm_path_col_index = -1


with open(moodle) as f:
    reader = csv.reader(f)
    moodle_headers = next(reader, None)
    moodle_rows = [r for r in reader]
    moodle_email_col_index = moodle_headers.index('Kasutajanimi')

with open(gtm) as f:
    reader = csv.reader(f)
    gtm_headers = next(reader, None)
    gtm_rows = [r for r in reader]
    gtm_user_col_index = gtm_headers.index('user')
    gtm_path_col_index = gtm_headers.index('path')

i = 1
for row in gtm_rows:
    moodle_row = [x for x in moodle_rows if row[gtm_user_col_index] in x[moodle_email_col_index]]
    if len(moodle_row) < 1:
        continue
    moodle_row = moodle_row[0]
    path = row[gtm_path_col_index].strip('/')
    moodle_test_points_col_idxes = [i for i, col in enumerate(moodle_headers) if f"{path} - Tests" in col]
    moodle_test_points_col_idx = moodle_test_points_col_idxes[0] if len(moodle_test_points_col_idxes) > 0 else -1
    if moodle_test_points_col_idx < 0:
        continue
    i += 1
    print(i, row[gtm_user_col_index], path, moodle_row[moodle_test_points_col_idx])
