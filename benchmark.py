import requests 
import threading
import time 
import json

base_url = "http://192.168.1.2:42004"
model = "llama3.1:8b"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM4ZjdhMmZkLWVhNGEtNGU5ZC1iZWUwLWY0ODc3MTU1NzliZCJ9.wdIAjhuISs8e9hicy_EhAFsmUd2OKvLGqZ8nughPkCI"

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
        data = json.loads(response.content)
        total_duration = data['usage']['total_duration']
        load_duration = data['usage']['load_duration']
        response_tokens_per_second = data['usage']['response_token/s']
        prompt_tokens_per_second = data['usage']['prompt_token/s']

        average_response_time = total_duration / len(data['choices'])
        utilization = (data['usage']['eval_count'] + data['usage']['completion_tokens']) / (total_duration / 1000) * 100 

        print("JSON Response: ")
        print(json.dumps(data, indent = 4))
        print("\nMetrics:")
        print(f"Average response time: {average_response_time}ms ")
        print(f"Response tokens per second {response_tokens_per_second}")
        print(f"Prompt tokens per second {prompt_tokens_per_second}")
        print(f"Utilization: {utilization}%")

        return response.json()
    except Exception as e:
        print(e)

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
for _ in range(10):
    thread = threading.Thread(target=api_calls, args=())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
