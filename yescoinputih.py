import requests
import concurrent.futures
import time
import threading
import sys

def current_unix_timestamp():
    return int(time.time() * 1000)

def read_launch_params_and_tokens(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        launch_params = lines[0].strip()
        tokens = [line.strip() for line in lines[1:]]
        return launch_params, tokens

def make_post_request(launch_params, token):
    view_completed_at = current_unix_timestamp()

    post_url = "https://clownfish-app-f7unk.ondigitalocean.app/v2/tasks/claimAdsgramAdReward"
    post_data = {
        "viewCompletedAt": view_completed_at,
        "reference": 81
    }
    post_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json; charset=utf-8",
        "Origin": "https://miniapp.yesco.in",
        "Referer": "https://miniapp.yesco.in/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Authorization": f"Bearer {token}",
        "Launch-Params": launch_params
    }

    try:
        post_response = requests.post(post_url, headers=post_headers, json=post_data)
        if post_response.status_code == 200:
            log_message(f"POST request successful for token {token}.")
        else:
            log_message(f"POST request failed for token {token}. Status code: {post_response.status_code}")
        log_message(f"Response content for token {token}: {post_response.text}")
    except Exception as e:
        log_message(f"Exception during POST request for token {token}: {e}")

    log_message(f"Unix timestamp at the end for token {token}: {view_completed_at}")

def start_requests():
    global stop_requests
    launch_params, tokens = read_launch_params_and_tokens(data_file_path)

    while not stop_requests:
        for token in tokens:
            if stop_requests:
                break
            
            log_message(f"Starting requests for token {token}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(make_post_request, launch_params, token) for _ in range(num_requests)]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        log_message(f"Exception occurred: {e}")

            log_message(f"Completed requests for token {token}")
            log_message("Waiting before starting the next token...")
            for _ in range(60):
                if stop_requests:
                    break
                time.sleep(1)

def on_start_stop():
    global stop_requests, request_thread

    if not request_thread or not request_thread.is_alive():
        stop_requests = False
        request_thread = threading.Thread(target=start_requests)
        request_thread.start()
    else:
        stop_requests = True
        request_thread.join()

def log_message(message):
    print(message)
    sys.stdout.flush()

data_file_path = 'data.txt'
num_requests = 100000000
stop_requests = False
request_thread = None

if __name__ == "__main__":
    on_start_stop()
    try:
        while request_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_requests = True
        request_thread.join()
