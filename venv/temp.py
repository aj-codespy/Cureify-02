import requests


url = "http://127.0.0.1:5001/process"


prompt = "I have a fever"

try:
    response = requests.post(url, json={"prompt": prompt, "img": "wound.jpeg"})

    if response.status_code == 200:

        data = response.json()
        print("Output:", data.get("result"))
    else:
        print(f"Error: {response.status_code}, {response.text}")
except Exception as e:
    print("Error occurred:", e)
    

