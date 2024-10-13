import requests

def upload_to_firebase(url, data):
    try:
        response = requests.put(f"{url}.json", json=data)
        if response.status_code == 200:
            print("Data uploaded successfully")
        else:
            print(f"Failed to upload data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_from_firebase(url):
    try:
        response = requests.get(f"{url}.json")
        if response.status_code == 200:
            data = response.json()
            print("Data retrieved successfully")
            return data
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")