import requests
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv('VT_API_KEY')

# VirusTotal API 호출
def call_virustotal_api(hash_value, endpoint=""):
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"
    if endpoint:
        url = f"https://www.virustotal.com/api/v3/files/{hash_value}/{endpoint}"

    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None