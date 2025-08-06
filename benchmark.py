import requests 
import threading
import time 

base_url = "http://192.168.1.100"
model = "ai model"
token = "token"

def read_file(file):
    prompts = open(file, 'r')
    lines = prompts.readlines()

    return lines

def chat_with_model(prompt):
    try:
        start = time.perf_counter()
        url = f'{base_url}/api/chat/completions'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {
        "model": model,
        "messages": [
            {
            "role": "user",
            "content": prompt
            }
        ]
        }
    response = requests.post(url, headers=headers, json=data)
    end = time.perf_counter()
    print(f"Timer {end - start:0.4f} seconds")
    return response.json()
    except Exeption as e:
            print("Error")
        

lines = read_file('prompts.txt')

def api_calls():
    threads = []
    for line in lines:
        thread = threading.Thread(target = chat_with_model, args = (line,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

threads = []
for i in range(10):
    thread = threading.Thread(target = chat_with_model, args = ())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

   
