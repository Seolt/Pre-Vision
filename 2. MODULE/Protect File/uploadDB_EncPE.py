from pymongo import MongoClient
import datetime
from logging_Utils import setup_logger  # 로깅 설정 함수 가져오기
from dotenv import load_dotenv
import os

load_dotenv()
#env에서 로드
MONGO_URI=os.getenv("MONGO_URI")
# 로그 파일 설정
log_file = r'C:\pymodules\log\upload_db_encpe.log'
logger = setup_logger(log_file)

# 암호화된 파일의 PE 정보를 MongoDB에 저장하는 함수
def store_encrypted_file_pe_info(signature_id, encrypted_filename, upload_ip, pe_info, encryption_status):
    try:
        # MongoDB 연결 설정
        client = MongoClient(MONGO_URI)
        db = client['encrypted_files']
        encrypted_file_pe_info_collection = db['pe_info']

        # 업로드 시간을 현재 시간으로 설정
        upload_time = datetime.datetime.now()

        # MongoDB에 저장할 PE 데이터 생성
        pe_data = {
            "signature_id": signature_id,
            "encrypted_filename": encrypted_filename,
            "encrypted_upload_time": upload_time,
            "upload_ip": upload_ip,
            "pe_info": pe_info,  # PE 정보 저장
            "encrypted": encryption_status  # 섹션 암호화 여부 저장
        }

        # MongoDB에 데이터 삽입
        encrypted_file_pe_info_collection.insert_one(pe_data)
        logger.info(f"PE information and encryption status for encrypted file {encrypted_filename} (signature_id: {signature_id}) successfully stored in MongoDB.")

    except Exception as e:
        logger.error(f"Error storing PE information for encrypted file {encrypted_filename} (signature_id: {signature_id}): {e}", exc_info=True)
