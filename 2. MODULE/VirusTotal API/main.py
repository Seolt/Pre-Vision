import time
import json
import re
from csv_reader import read_hashes_from_csv
from virustotal_api import call_virustotal_api
from data_converter import convert_data
from mongodb_handler import upload_to_mongodb



# 설정
MAX_EXECUTIONS_PER_MINUTE = 5  # 분당 최대 5번 실행
MAX_EXECUTIONS_PER_DAY = 250  # 하루 최대 250번 실행
PROCESSED_HASHES_FILE = 'processed_hashes.json'  # 처리된 해시 기록

# 분당 5번 실행을 위한 제한 함수
def rate_limiter():
    time.sleep(12)  # 12초에 1번 실행 -> 분당 5번 실행 가능
# 처리된 해시 기록 로드
def load_processed_hashes():
    try:
        with open(PROCESSED_HASHES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# MD5 해시가 유효한지 확인하는 함수
def is_valid_md5(md5_hash):
    """MD5 해시가 32자리의 16진수인지 확인"""
    return re.match(r"^[a-fA-F0-9]{32}$", md5_hash) is not None
# 처리된 해시 기록 저장
def save_processed_hashes(processed_hashes):
    with open(PROCESSED_HASHES_FILE, 'w') as f:
        json.dump(processed_hashes, f)


def process_hash(hash_value, processed_hashes, template):
    if hash_value in processed_hashes:
        print(f"{hash_value} 이미 처리됨. 스킵합니다.")
        return

    # 유효한 MD5 해시인지 확인
    if not is_valid_md5(hash_value):
        print(f"{hash_value} 유효하지 않은 MD5 해시입니다. 스킵합니다.")
        return

    # VirusTotal API 호출
    details = call_virustotal_api(hash_value)
    if details is None:
        print(f"{hash_value} 처리 실패. 파일을 찾을 수 없습니다.")
        return

    behavior = call_virustotal_api(hash_value, "behaviour_summary")
    if behavior is None:
        print(f"{hash_value} 처리 실패. 행동 분석 정보를 찾을 수 없습니다.")
        return

    if details and behavior:
        # 데이터 변환
        converted_data = convert_data(details, behavior, template)

        # MongoDB에 업로드
        upload_to_mongodb(converted_data)

        # 처리된 해시 기록
        processed_hashes.append(hash_value)
        save_processed_hashes(processed_hashes)
    else:
        print(f"{hash_value} 처리 실패.")


if __name__ == "__main__":
    # CSV에서 해시값 읽기
    csv_file_path = "dataset.csv"
    template_file_path = "template.json"

    # 템플릿 파일을 미리 로드하여 딕셔너리로 변환
    with open(template_file_path, 'r', encoding='utf-8') as template_file:
        template = json.load(template_file)

    # 처리된 해시 로드
    processed_hashes = load_processed_hashes()

    # 해시값 처리
    execution_count = 0
    hashes = read_hashes_from_csv(csv_file_path)

    for hash_value in hashes:
        if execution_count >= MAX_EXECUTIONS_PER_DAY:
            print("오늘의 최대 실행 횟수에 도달했습니다.")
            break

        process_hash(hash_value, processed_hashes, template)
        execution_count += 1
        rate_limiter()
