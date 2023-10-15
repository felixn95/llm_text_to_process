import json
import requests
import time
import PromptsReader
from PromptsReader import TextFiles
from dotenv import load_dotenv
import os

def is_valid_response(response):
    try:
        data = json.loads(response)
        if (
            isinstance(data, dict)
            and "activity-labels" in data
            and isinstance(data["activity-labels"], list)
        ):
            return True
        else:
            return False
    except json.JSONDecodeError:
        return False


def extract_activities_llama2(process_plaintext: str) -> str:
    load_dotenv() # Load environment variables from .env file
    api_token = os.environ.get('REPLICATE_API_TOKEN')
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json",
    }
    url = "https://api.replicate.com/v1/predictions"

    pre_prompt = PromptsReader.read_text_file(TextFiles.ACTIVITIES_PREPROMPT.value)
    post_prompt = PromptsReader.read_text_file(TextFiles.ACTIVITIES_POSTPROMPT.value)
    system_prompt = PromptsReader.read_text_file(
        TextFiles.ACTIVITIES_SYSTEMPROMPT.value
    )

    # Prompts engineering
    full_prompt = f"{pre_prompt} {process_plaintext} {post_prompt}"

    payload = {
        "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        "input": {
            "prompt": full_prompt,
            "max_new_tokens": 2048,
            "temperature": 0.5,
        },
    }

    # Initial request
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200 and response.status_code != 201:
        return f"Error: {response.status_code}"

    initial_output = json.loads(response.text)
    prediction_id = initial_output.get("id", "")

    start_time = time.time()
    max_wait_time = 60  # Maximum wait time in seconds

    # Polling with timeout
    while True:
        current_time = time.time()
        if current_time - start_time > max_wait_time:
            return "Error: Timeout reached"

        poll_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        poll_response = requests.get(poll_url, headers=headers)

        if poll_response.status_code != 200 and poll_response.status_code != 201:
            return f"Error: {poll_response.status_code}"

        poll_output = json.loads(poll_response.text)
        status = poll_output.get("status", "")

        if status == "succeeded":
            output = poll_output.get("output", "")
            full_response = ""
            for item in output:
                full_response += str(item)
            return full_response
        elif status in ["starting", "processing"]:
            time.sleep(2)  # Sleep for 2 seconds before polling again
        else:
            return f"Error: Unknown status {status}"
        
def extract_activities_openai(process_plaintext: str) -> str:
    load_dotenv() # Load environment variables from .env file
    api_token = os.environ.get('OPENAI_API_TOKEN') 
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    url = "https://api.openai.com/v1/chat/completions"
    
    pre_prompt = PromptsReader.read_text_file(TextFiles.ACTIVITIES_PREPROMPT.value)
    post_prompt = PromptsReader.read_text_file(TextFiles.ACTIVITIES_POSTPROMPT.value)
    system_prompt = PromptsReader.read_text_file(TextFiles.ACTIVITIES_SYSTEMPROMPT.value)

    print (f"{pre_prompt} {process_plaintext} {post_prompt}")

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"{pre_prompt} {process_plaintext} {post_prompt}"
        }
    ]
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error: {response.status_code}"
    
    assistant_reply = response.json()["choices"][0]["message"]["content"]
    
    return assistant_reply

