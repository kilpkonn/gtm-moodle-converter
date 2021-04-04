
import sys
import csv
import hashlib


class Commit:
    def __init__(self, hash, path, is_app, points, style_points, time, lines_added, lines_removed, files, message, timestamp):
        """Init."""
        self.hash = hash
        self.path = path
        self.is_app = is_app
        self.points = points
        self.style_points = style_points
        self.time = time
        self.lines_added = lines_added
        self.lines_removed = lines_removed
        self.files = files
        self.message = message
        self.timestamp = timestamp


if len(sys.argv) < 3:
    print("please specify moodle and gtm files as arguments")
    exit(1)


csv_headers = ['hash', 'path', 'is_app', 'points', 'style_points', 'time', 'lines_added', 'lines_removed', 'files',
               'message', 'timestamp']
moodle = sys.argv[1]
moodle_headers = []
moodle_rows = []
moodle_email_col_index = -1

gtm = sys.argv[2]
gtm_headers = []
gtm_rows = []
gtm_user_col_index = -1
gtm_path_col_index = -1
gtm_is_app_col_index = -1
gtm_time_col_index = -1
gtm_lines_added_col_index = -1
gtm_lines_removed_col_index = -1
gtm_files_col_index = -1
gtm_message_col_index = -1
gtm_timestamp_col_index = -1


with open(moodle) as f:
    reader = csv.reader(f)
    moodle_headers = [x.lower() for x in next(reader, None)]
    moodle_rows = [[a.lower() for a in r] for r in reader]
    moodle_email_col_index = moodle_headers.index('kasutajanimi')

with open(gtm, encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    gtm_headers = [x.lower().replace('"', '').strip() for x in next(reader, None)]
    gtm_rows = [[a.lower().replace('"', '').strip() for a in r] for r in reader]
    gtm_user_col_index = gtm_headers.index('user')
    gtm_path_col_index = gtm_headers.index('path')
    gtm_is_app_col_index = gtm_headers.index('isapp')
    gtm_time_col_index = gtm_headers.index('totaltime')
    gtm_lines_added_col_index = gtm_headers.index('linesadded')
    gtm_lines_removed_col_index = gtm_headers.index('linesremoved')
    gtm_files_col_index = gtm_headers.index('filescount')
    gtm_message_col_index = gtm_headers.index('message')
    gtm_timestamp_col_index = gtm_headers.index('timestamp')

i = 1
commits = []
for row in gtm_rows:
    moodle_row = [x for x in moodle_rows if row[gtm_user_col_index] in x[moodle_email_col_index]]
    if len(moodle_row) < 1:
        continue
    moodle_row = moodle_row[0]
    path = row[gtm_path_col_index].strip('/')
    moodle_test_points_col_idxes = [i for i, col in enumerate(moodle_headers) if f"{path} - tests" in col]
    moodle_style_points_col_idxes = [i for i, col in enumerate(moodle_headers) if f"{path} - style" in col]
    moodel_points = sum([float(moodle_row[i]) for i in moodle_test_points_col_idxes if moodle_row[i].isnumeric()])
    moodel_style_points = sum([float(moodle_row[i]) for i in moodle_style_points_col_idxes if moodle_row[i].isnumeric()])

    # i += 1
    # print(i,
    #       hashlib.sha1(row[gtm_user_col_index].encode("utf-8")).hexdigest(),
    #       path,
    #       moodel_points,
    #       row[gtm_time_col_index],
    #       row[gtm_lines_added_col_index],
    #       row[gtm_lines_removed_col_index],
    #       row[gtm_files_col_index],
    #       row[gtm_message_col_index],
    #       row[gtm_timestamp_col_index])
    commits.append(Commit(hashlib.sha1(row[gtm_user_col_index].encode("utf-8")).hexdigest(),
                          path,
                          row[gtm_is_app_col_index],
                          moodel_points,
                          moodel_style_points,
                          row[gtm_time_col_index],
                          row[gtm_lines_added_col_index],
                          row[gtm_lines_removed_col_index],
                          row[gtm_files_col_index],
                          row[gtm_message_col_index],
                          row[gtm_timestamp_col_index]))

with open('./output.csv', 'w+') as f:
    wr = csv.writer(f, delimiter=',')
    wr.writerow(csv_headers)
    for c in commits:
        wr.writerow([c.hash, c.path, c.is_app, c.points, c.style_points, c.time, c.lines_added, c.lines_removed,
                     c.files, c.message, c.timestamp])
