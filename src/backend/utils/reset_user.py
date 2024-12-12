import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_user.py <USER_ID>")
        sys.exit(1)

    user_id = sys.argv[1]
    endpoint = "http://localhost:5000/api/reset_cloud_progress"  # Replace with your actual endpoint

    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Replace with your token if required
        "Content-Type": "application/json"
    }

    # Sending the user_id as {"userID": user_id} in the POST request body.
    payload = {"userID": user_id}

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"200: {response.text}")
    elif response.status_code == 404:
        print(f"404: {response.text}")
    else:
        print(f"Failed to reset user {user_id}. Status code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    main()
