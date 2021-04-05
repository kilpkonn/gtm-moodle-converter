
## Data
- **hash**: Hashed user identifier. Can be used to group data by user.
- **path**: Edited file path or program name. For files this is either a complete path or 
  path beginning. For files this usually corresponds to task folder.
  _(Amount of files grouped can be seen in `files` field)_
- **is_app**: Identifier whether the time is recorded running program or editing file.
- **points**: Moodle (undefended) points.
- **style_points**: Style points. Typically either 0 or 1.
- **time**: Time recorded for `path` in seconds.
- **lines_added**: Amount of lines written in `path` according to git diff. Copy pastes without 
time data are considered 0.
- **lines_removed**: Amount of lines deleted in `path` according to git diff. Deletes without
any time spent are considered 0.
- **files**: Amount of files grouped for `path`
- **message**: Commit message
- **timestamp**: UNIX timestamp in seconds