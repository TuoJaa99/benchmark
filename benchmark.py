import requests 
import threading 
import json

base_url = "http://127.0.0.1:42004"
model = "llama3.1:8b"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM4ZjdhMmZkLWVhNGEtNGU5ZC1iZWUwLWY0ODc3MTU1NzliZCJ9.wdIAjhuISs8e9hicy_EhAFsmUd2OKvLGqZ8nughPkCI"
timeout = 30
rounds = 5
prompt_file = 'prompts.txt'

def read_file(file):
    with open(file, 'r') as prompts:
        return prompts.readlines()

def data_calculations(response):
    data = json.loads(response.content)
    total_duration = data['usage']['total_duration']
    load_duration = data['usage']['load_duration']
    response_tokens_per_second = data['usage']['response_token/s']
    prompt_tokens_per_second = data['usage']['prompt_token/s']

    average_response_time = total_duration / len(data['choices'])
    utilization = (data['usage']['eval_count'] + data['usage']['completion_tokens']) / (total_duration / 1000) * 100 

    return data, average_response_time, response_tokens_per_second, prompt_tokens_per_second, utilization

def print_data(data, prompt, average_response_time, response_tokens_per_second, prompt_tokens_per_second, utilization):
    print("\nPrompt:")
    print(data['model'])
    print(f"{prompt.strip()}")
    print("\nResponse:")
    print(data['choices'][0]['message']['content'][:100])
    print("\nMetrics:")
    print(f"Average response time: {average_response_time} ms")
    print(f"Response tokens per second: {response_tokens_per_second}")
    print(f"Prompt tokens per second: {prompt_tokens_per_second}")
    print(f"Utilization: {utilization:.2f}%")
    print("="*50)

def chat_with_model(prompt):
    try:
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

        response = requests.post(url, headers=headers, json=data, timeout=timeout)

        if response.status_code == 200:
            data, avg_time, resp_tps, prompt_tps, util = data_calculations(response)
            print_data(data, prompt, avg_time, resp_tps, prompt_tps, util)
        else:
            print(f"Request failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error during API call: {e}")

lines = read_file('prompts.txt')

def api_calls(prompts):
    threads = []
    for line in lines:
        thread = threading.Thread(target=chat_with_model, args=(line,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    lines = read_file(prompt_file)

    threads = []

    for _ in range(rounds):
        thread = threading.Thread(target = api_calls, args = (lines,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
