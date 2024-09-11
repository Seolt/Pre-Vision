import requests
import time
import os
from dotenv import load_dotenv
from logger_manager import setup_logger

# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\virustotal_api', r'C:\VTAPImodules\log\virustotal_api.log')

load_dotenv()
API_KEY = os.getenv('VT_API_KEY')

# VirusTotal에서 해시로 검색하는 함수 (재시도 포함)
def search_file_by_hash_with_retry(file_hash, retries=5, wait_time=60):
    for i in range(retries):
        logger.info(f"해시 검색 시도 {i + 1}/{retries}: {file_hash}")
        
        response_json = search_file_by_hash(file_hash)
        if response_json:
            logger.info(f"{file_hash} 해시 검색 성공")
            return response_json
        else:
            logger.info(f"{file_hash} 파일이 아직 처리되지 않았습니다. {wait_time}초 대기 후 다시 시도합니다...")
            time.sleep(wait_time)
    logger.error(f"{file_hash} 최대 재시도 횟수 초과")
    return None

# VirusTotal 해시 검색
def search_file_by_hash(hash_value, endpoint=""):
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"
    if endpoint:
        url = f"https://www.virustotal.com/api/v3/files/{hash_value}/{endpoint}"

    headers = {"accept": "application/json", "x-apikey": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:  # 성공 시
        logger.info(f"{hash_value} 해시 검색 성공")
        return response.json()
    else:
        logger.error(f"{hash_value} 해시 검색 실패: {response.status_code}")
        return None

# VirusTotal 파일 업로드
def upload_file_to_virustotal(file_data):
    logger.info("VirusTotal 파일 업로드 시작")
    
    upload_url_response = requests.get("https://www.virustotal.com/api/v3/files/upload_url", headers={"x-apikey": API_KEY})
    
    if upload_url_response.status_code == 200:
        upload_url = upload_url_response.json().get('data', None)
        
        if upload_url:
            files = {'file': file_data}
            upload_response = requests.post(upload_url, files=files, headers={"x-apikey": API_KEY})
            
            if upload_response.status_code == 200:
                logger.info("파일 업로드 성공")
                return True
            else:
                logger.error(f"파일 업로드 실패: {upload_response.status_code} - {upload_response.text}")
        else:
            logger.error("업로드 URL 획득 실패")
    else:
        logger.error(f"업로드 URL 요청 실패: {upload_url_response.status_code} - {upload_url_response.text}")
    
    return None
