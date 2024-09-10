import os
from pymongo import MongoClient
import gridfs
from logging_Utils import setup_logger
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
#env에서 로드
MONGO_URI=os.getenv("MONGO_URI")
# 로그 설정
log_file = r'C:\pymodules\log\file_encryption.log'
logger = setup_logger(log_file)

# MongoDB 연결 설정
client = MongoClient(MONGO_URI)
db = client['encrypted_files']  # encrypted_files DB 사용
fs = gridfs.GridFS(db)  # GridFS를 이용해 파일을 저장

def store_encrypted_file(encrypted_file_path, original_file_doc):
    """
    Themida로 보호된 파일을 GridFS에 저장하고, 관련 메타데이터를 MongoDB의 encrypted_files.filedata 컬렉션에 저장.
    
    :param encrypted_file_path: 보호된 파일 경로
    :param original_file_doc: 원본 파일의 메타데이터 (MongoDB에서 가져온 정보)
    """
    try:
        # 암호화된 파일을 읽어서 MongoDB에 저장
        with open(encrypted_file_path, "rb") as f:
            encrypted_file_data = f.read()

        # GridFS에 암호화된 파일 저장
        encrypted_file_id = fs.put(
            encrypted_file_data,
            filename=os.path.basename(encrypted_file_path),
            original_filename=original_file_doc["filename"],
            original_signature_id=original_file_doc["signature_id"],
            file_extension=os.path.splitext(encrypted_file_path)[1],
            encrypted=True  # 파일이 암호화되었음을 표시
        )

        # 메타데이터 저장: 암호화된 파일 정보
        encrypted_file_doc = {
            "signature_id": original_file_doc["signature_id"],  # 원본 파일의 signature_id 유지
            "original_filename": original_file_doc["filename"],  # 원본 파일명
            "encrypted_filename": os.path.basename(encrypted_file_path),  # 암호화된 파일명
            "original_upload_time": original_file_doc["upload_time"],  # 원본 파일 업로드 시간
            "encrypted_upload_time": datetime.now(),  # 암호화된 파일 저장 시간
            "upload_ip": original_file_doc["upload_ip"],  # 업로드한 IP 정보
            "gridfs_file_id": encrypted_file_id  # GridFS에 저장된 파일의 ID
        }

        # encrypted_files의 filedata 컬렉션에 메타데이터 저장
        db.filedata.insert_one(encrypted_file_doc)

        logger.info(f"Encrypted file {encrypted_file_path} has been stored in MongoDB successfully.")
        return True

    except Exception as e:
        logger.error(f"Error storing encrypted file {encrypted_file_path} in MongoDB: {e}", exc_info=True)
        return False
