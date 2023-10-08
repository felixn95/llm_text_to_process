
import json
import requests
import replicate

import os
import json
import requests

import requests
import json
import time

def extract_activities(pre_prompt: str, process_plaintext: str) -> str:
    api_token = "PLACE_YOUR_TOKEN_HERE"
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = "https://api.replicate.com/v1/predictions"

    # Prompts engineering
    process_plaintext_improved = f"### instruction: {process_plaintext} ### response:"
    full_prompt = f"{pre_prompt} {process_plaintext_improved}"

    payload = {
        "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        "input": {"prompt": full_prompt}
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



def assign_actor(pre_prompt: str, process_plaintext: str, activity: str) -> str:
    api_token = "PLACE_YOUR_TOKEN_HERE"
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = "https://api.replicate.com/v1/predictions"

    # Prompts engineering
    process_plaintext_improved = f"### Process Model: {process_plaintext}"
    question_prepared = f"### instruction: Who is the process participant performing '{activity}' activity in the process model? ### response:"
    full_prompt = f"{pre_prompt} {process_plaintext_improved} {question_prepared}"

    payload = {
        "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        "input": {"prompt": full_prompt}
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
            time.sleep(2)
        else:
            return f"Error: Unknown status {status}" 