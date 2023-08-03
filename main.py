import threading
import requests
import argparse
import time
import sys

# Function to perform the directory brute force
def directory_brute_force(url, directory, output_file, proxies=None, white_list=None, black_list=None, timeout=5):
    full_url = url + directory
    try:
        response = requests.get(full_url, proxies=proxies, timeout=timeout)
    except requests.Timeout:
        print(f"Timeout - {full_url}")
        return
    except requests.ConnectionError:
        print(f"Connection Error - {full_url}")
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    status = response.status_code

    with open(output_file, 'a') as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"URL: {full_url}\n")
        file.write(f"HTTP Status Code: {status}\n")

    if white_list and status in white_list:
        with open(output_file, 'a') as file:
            file.write("Result: Whitelist Match\n")
        print(f"Whitelist Match - {full_url}")
    elif black_list and status in black_list:
        with open(output_file, 'a') as file:
            file.write("Result: Blacklist Ignored\n")
    elif status == 200:
        with open(output_file, 'a') as file:
            file.write("Result: Successful Hit\n")
        print(f"Successful Hit - {full_url}")

    with open(output_file, 'a') as file:
        file.write(f"Tested Directory: {directory}\n")
        file.write("-" * 40 + "\n")

# Function to create and start threads
def start_threads(url, directories, output_file, proxies=None, thread_count=1, white_list=None, black_list=None, timeout=5):
    total_directories = len(directories)
    progress_lock = threading.Lock()
    progress_bar_width = 50

    def print_progress(progress):
        with progress_lock:
            sys.stdout.write("\rProgress: [{:<{}}] {}%".format('=' * progress, progress_bar_width, progress))
            sys.stdout.flush()

    def threaded_directory_brute_force(directory):
        directory_brute_force(url, directory, output_file, proxies, white_list, black_list, timeout)
        with progress_lock:
            nonlocal completed
            completed += 1
            progress = int((completed / total_directories) * progress_bar_width)
            print_progress(progress)

    threads = []
    completed = 0

    for directory in directories:
        thread = threading.Thread(target=threaded_directory_brute_force, args=(directory,))
        threads.append(thread)
        thread.start()

        # Limit the number of concurrent threads
        if len(threads) >= thread_count:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for the remaining threads to complete
    for thread in threads:
        thread.join()

    # Ensure the progress bar reaches 100%
    print_progress(progress_bar_width)
    print()  # New line after progress bar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Threaded Directory Brute Force")
    parser.add_argument("url", type=str, help="Target URL to test")
    parser.add_argument("wordlist", type=str, help="Path to the word list file")
    parser.add_argument("-p", "--proxies", type=str, default=None, help="Proxy settings (e.g., http://proxy-server:port)")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads (default: 1)")
    parser.add_argument("-w", "--whitelist", type=int, nargs="*", help="Whitelist of HTTP status codes (e.g., 200 204 301)")
    parser.add_argument("-b", "--blacklist", type=int, nargs="*", help="Blacklist of HTTP status codes to ignore")
    parser.add_argument("-o", "--output", type=str, default="dir.txt", help="Output file name")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout for each request in seconds (default: 5)")

    args = parser.parse_args()

    target_url = args.url
    wordlist_path = args.wordlist
    proxy_settings = {'http': args.proxies, 'https': args.proxies} if args.proxies else None
    thread_count = args.threads
    white_list = args.whitelist
    black_list = args.blacklist
    output_file = args.output
    timeout = args.timeout

    # Load the word list from the file
    with open(wordlist_path, "r") as file:
        directories = [line.strip() for line in file]

    with open(output_file, 'w') as file:
        file.write(f"Target URL: {target_url}\n")
        file.write(f"Word List: {wordlist_path}\n")
        file.write(f"Proxy Settings: {proxy_settings}\n")
        file.write(f"Threads: {thread_count}\n")
        file.write(f"Whitelist: {white_list}\n")
        file.write(f"Blacklist: {black_list}\n")
        file.write(f"Timeout: {timeout} seconds\n")
        file.write("=" * 40 + "\n")

    start_threads(target_url, directories, output_file, proxies=proxy_settings, thread_count=thread_count)
