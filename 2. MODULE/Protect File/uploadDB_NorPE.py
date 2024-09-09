from pymongo import MongoClient
import datetime
from logging_Utils import setup_logger  # 로깅 설정 함수 가져오기

# 로그 파일 설정
log_file = r'C:\pymodules\log\upload_db_norpe.log'
logger = setup_logger(log_file)

# 일반 파일의 PE 정보를 MongoDB에 저장하는 함수
def store_normal_file_pe_info(signature_id, filename, upload_ip, pe_info, encryption_status):
    try:
        # MongoDB 연결
        client = MongoClient('mongodb://admin:qwer1234!@predb.yeonharin.com:27017/?authSource=admin&directConnection=true')
        db = client['normal_files']
        normal_file_pe_info_collection = db['pe_info']

        # 업로드 시간을 현재 시각으로 설정
        upload_time = datetime.datetime.now()

        # MongoDB에 저장할 PE 데이터 생성
        pe_data = {
            "signature_id": signature_id,
            "filename": filename,
            "upload_time": upload_time,
            "upload_ip": upload_ip,
            "pe_info": pe_info,
            "encrypted": encryption_status
        }

        # MongoDB에 데이터 삽입
        normal_file_pe_info_collection.insert_one(pe_data)
        logger.info(f"PE information for file {filename} (signature_id: {signature_id}) successfully stored in MongoDB.")

    except Exception as e:
        logger.error(f"Error storing PE information for file {filename} (signature_id: {signature_id}): {e}", exc_info=True)
