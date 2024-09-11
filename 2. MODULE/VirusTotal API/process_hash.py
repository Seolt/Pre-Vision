import time
import json
import re
from hash_handler import read_hashes_from_csv, load_processed_hashes, save_processed_hashes
from virustotal_API import search_file_by_hash
from data_converter import convert_data
from DB_handler import upload_to_mongodb
from logger_manager import setup_logger

# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\process_hash', r'C:\VTAPImodules\log\process_hash.log')

# 설정
MAX_EXECUTIONS_PER_MINUTE = 2  # 분당 최대 2번 실행
MAX_EXECUTIONS_PER_DAY = 250  # 하루 최대 250번 실행

# 분당 5번 실행을 위한 제한 함수
def rate_limiter():
    time.sleep(30)  # 30초마다 1번 실행 -> 분당 2번 실행 가능
    logger.info("Rate limiter: 30초 대기")

# MD5 해시가 유효한지 확인하는 함수
def is_valid_md5(md5_hash):
    """MD5 해시가 32자리의 16진수인지 확인"""
    valid = re.match(r"^[a-fA-F0-9]{32}$", md5_hash) is not None
    if not valid:
        logger.warning(f"유효하지 않은 MD5 해시: {md5_hash}")
    return valid

def process_hash(hash_value, processed_hashes):
    if hash_value in processed_hashes:
        logger.info(f"{hash_value} 이미 처리됨. 스킵합니다.")
        return False  # 이미 처리된 경우 False 반환

    # 유효한 MD5 해시인지 확인
    if not is_valid_md5(hash_value):
        logger.warning(f"{hash_value} 유효하지 않은 MD5 해시입니다. 스킵합니다.")
        return False  # 유효하지 않은 해시는 처리하지 않음

    # VirusTotal API 호출
    details = search_file_by_hash(hash_value)
    if details is None:
        logger.error(f"{hash_value} 처리 실패. 파일을 찾을 수 없습니다.")
        return False

    behavior = search_file_by_hash(hash_value, "behaviour_summary")
    if behavior is None:
        logger.warning(f"{hash_value} 행동 분석 정보를 찾을 수 없습니다.")

    if details:
        # 데이터 변환
        logger.info(f"{hash_value} 데이터 변환 중...")
        converted_data = convert_data(details, behavior)

        # MongoDB에 업로드
        upload_to_mongodb(converted_data, "info")
        logger.info(f"{hash_value} MongoDB에 저장 완료.")

        # 처리된 해시 기록
        processed_hashes.append(hash_value)
        save_processed_hashes(processed_hashes)
        logger.info(f"{hash_value} 처리된 해시 기록에 추가.")
        return True  # 성공적으로 처리된 경우 True 반환
    else:
        logger.error(f"{hash_value} 처리 실패.")
        return False  # 처리 실패 시 False 반환

    rate_limiter()

if __name__ == "__main__":
    logger.info("처리된 해시 로드 시작")
    
    # 처리된 해시 로드
    processed_hashes = load_processed_hashes()

    # 해시값 처리
    execution_count = 0
    hashes = read_hashes_from_csv()

    for hash_value in hashes:
        if execution_count >= MAX_EXECUTIONS_PER_DAY:
            logger.info("오늘의 최대 실행 횟수에 도달했습니다.")
            break

        if process_hash(hash_value, processed_hashes):
            execution_count += 1  # 실제로 처리된 경우에만 증가
