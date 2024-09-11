from DB_handler import watch_for_file_uploads, upload_to_mongodb, check_hash_in_mongodb
from virustotal_API import search_file_by_hash_with_retry, upload_file_to_virustotal, search_file_by_hash
from hash_handler import save_processed_hashes, load_processed_hashes
from data_converter import convert_data
from logger_manager import setup_logger
import time
# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\process_new_file', r'C:\VTAPImodules\log\process_new_file.log')

# 새 파일이 업로드되었을 때 VirusTotal에서 처리하는 함수
def process_new_file(file_hash, file_data, processed_hashes):
    logger.info(f"새로운 파일 업로드 감지: {file_hash}")

    # DB에 hash가 있는 경우 종료
    if check_hash_in_mongodb(file_hash):
        logger.info(f"{file_hash} 이미 DB에 존재함. 처리 종료.")
        return

    # VirusTotal에서 해시 검색
    details = search_file_by_hash(file_hash)
    if not details:
        logger.info(f"{file_hash} VirusTotal에 없음, 파일 업로드 중...")
        flag = upload_file_to_virustotal(file_data['file_data'])  # 파일 내용 업로드
        if flag:
            # 파일 해시로 검색 (없으면 반복)
            search_result = search_file_by_hash_with_retry(file_hash)
            if search_result:
                details = search_result
                behavior = search_file_by_hash(file_hash, "behaviour_summary")
    else:
        logger.info(f"{file_hash} 이미 VirusTotal에 존재함. 데이터 가져오는 중...")
        behavior = search_file_by_hash(file_hash, "behaviour_summary")

    # 데이터 변환 후 DB에 추가
    if details:
        logger.info(f"{file_hash} 데이터 변환 중...")
        converted_data = convert_data(details, behavior)

        # MongoDB에 업로드
        upload_to_mongodb(converted_data, 'info')
        # 처리된 해시 기록 추가
        processed_hashes.append(file_hash)
        save_processed_hashes(processed_hashes)
        logger.info(f"{file_hash} 분석 및 행동 분석 완료 후 MongoDB에 저장.")
    else:
        logger.error(f"{file_hash} 처리 실패.")

if __name__ == "__main__":
    logger.info("파일 업로드 감시 시작")
    filehash, filedata = watch_for_file_uploads()
    processed_hashes = load_processed_hashes()

    if filehash:
        process_new_file(filehash, filedata, processed_hashes)
        filehash = None
