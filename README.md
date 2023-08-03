# Multi-Threaded Directory Brute Force Tool

## Requirements

- Python 3.x
- `requests` library: You can install it using `pip install requests`.

## How to Use

1. `git clone https://github.com/farukerdem34/dirbrute.git`.

2. `pip install requirements.txt`

3. Run the script with the following command:

**Options:**
- `-p, --proxies`: Specify proxy settings (e.g., http://proxy-server:port). Optional. (Not Tested)

- `-t, --threads`: Set the number of threads (default: 1). Optional.

- `-w, --whitelist`: Provide a whitelist of HTTP status codes (e.g., 200 204 301). Optional.

- `-b, --blacklist`: Specify a blacklist of HTTP status codes to ignore. Optional.

- `-o, --output`: Set the output file name (default: dir.txt). Optional.

- `--timeout`: Set the timeout for each request in seconds (default: 5). Optional.

