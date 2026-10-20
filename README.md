# license-header-check

Check source files for a license header such as an SPDX identifier or copyright notice.

## Features

- Recursively scans a directory for common source files.
- Reports files whose first lines do not contain a configured marker.
- Supports custom markers, extensions, ignored directories, and JSON output.
- Uses only the Python standard library.
- Returns a non-zero exit status when files are missing headers.

## Install

```sh
pip install .
```

Or run without installation:

```sh
python license_header_check.py .
```

## Usage

```sh
license-header-check .
license-header-check src --marker "Copyright" --marker "SPDX-License-Identifier"
license-header-check . --extensions py,js,ts --format json
```

## Options

- `path`: directory to scan; defaults to the current directory.
- `--marker`: text to look for in the first lines; may be repeated.
- `--spdx`: shorthand for `--marker SPDX-License-Identifier`.
- `--extensions`: comma-separated file extensions to scan.
- `--ignore`: comma-separated directory names to skip.
- `--max-lines`: number of leading lines to inspect.
- `--format`: `text` or `json`.

## Exit codes

- `0`: every scanned file has a matching header.
- `1`: one or more files are missing a matching header.

## License

MIT
