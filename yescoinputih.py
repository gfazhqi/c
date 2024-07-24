import tkinter as tk
import requests
import concurrent.futures
import time
import threading
import sys

def current_unix_timestamp():
    return int(time.time() * 1000)

def read_launch_params(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def make_post_request(launch_params):
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
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Launch-Params": launch_params
    }

    post_response = requests.post(post_url, headers=post_headers, json=post_data)

    if post_response.status_code == 200:
        log_message("POST request successful.")
    else:
        log_message(f"POST request failed. Status code: {post_response.status_code}")

    log_message(f"Response content: {post_response.text}")

    log_message(f"Unix timestamp at the end: {view_completed_at}")

def start_requests():
    global stop_requests
    launch_params = read_launch_params(data_file_path)

    while not stop_requests:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(make_post_request, launch_params) for _ in range(num_requests)]

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    log_message(f"Exception occurred: {e}")

        log_message("All requests completed. Waiting before starting again...")
        for _ in range(60):
            if stop_requests:
                break
            time.sleep(1)  

def on_start_stop_button_click():
    global stop_requests, request_thread

    if start_stop_button['text'] == "Start":
        stop_requests = False
        start_stop_button['text'] = "Stop"
        request_thread = threading.Thread(target=start_requests)
        request_thread.start()
    else:
        stop_requests = True
        start_stop_button['text'] = "Start"

def log_message(message):
    log_text_widget.insert(tk.END, message + "\n")
    log_text_widget.see(tk.END)

class RedirectText(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

data_file_path = 'data.txt'
num_requests = 100000
stop_requests = False
request_thread = None

root = tk.Tk()
root.title("POST Request GUI")

title_label = tk.Label(root, text="Yescoin Putih By APS Studio Team", font=("Helvetica", 16))
title_label.pack(pady=10)

start_stop_button = tk.Button(root, text="Start", command=on_start_stop_button_click)
start_stop_button.pack(pady=20)

log_text_widget = tk.Text(root, wrap='word', height=20, width=80)
log_text_widget.pack(pady=20)

sys.stdout = RedirectText(log_text_widget)

root.mainloop()

