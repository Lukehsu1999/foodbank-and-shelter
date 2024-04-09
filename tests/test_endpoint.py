import requests

# Define the URL endpoint of your Flask application
url = 'http://127.0.0.1:5000/chat'  # Replace 'your_endpoint' with the actual endpoint

# Define the JSON data to be sent in the request body
data = {
    "session_id": "Andrew",
    "input_message": "What is my name?"
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    print("POST request successful!")
    print("Response JSON:", response.json())  # Print the response JSON data
else:
    print("POST request failed with status code:", response.status_code)


