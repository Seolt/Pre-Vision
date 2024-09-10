import os
from pymongo import MongoClient
from datetime import datetime
import convert_NorToEnc  # 암호화 모듈
import uploadDB_NorPE  # PE 섹션 분석 및 저장 모듈
import check_Enc  # 암호화 확인 모듈
from logging_Utils import setup_logger  # 로그 설정 함수
from dotenv import load_dotenv
load_dotenv()

#env에서 로드
MONGO_URI=os.getenv("MONGO_URI")
# 로그 파일 설정
log_file = r'C:\pymodules\log\db_file_store.log'
logger = setup_logger(log_file)

# MongoDB 연결 설정
client = MongoClient(MONGO_URI)
db = client['normal_files']
collection = db['filedata']

def store_file(file_doc):
    """DB에서 파일을 다운로드하고 signature_id로 로컬에 저장 (확장자 필드 사용)"""
    try:
        signature_id = file_doc["signature_id"]
        file_extension = file_doc.get("file_extension", "")
        
        # 확장자가 없거나 잘못된 형식일 경우 수정
        if not file_extension.startswith("."):
            file_extension = f".{file_extension}"

        # 오늘 날짜를 기준으로 폴더 생성
        today_date = datetime.today().strftime('%Y-%m-%d')
        local_folder_path = os.path.join(r'C:\DBFiles', today_date, 'origin_files')

        # 로컬 폴더가 존재하지 않으면 생성
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        # 파일명을 signature_id로 하고, 확장자를 적용
        local_file_path = os.path.join(local_folder_path, f"{signature_id}{file_extension}")

        # MongoDB에서 파일 데이터 다운로드 및 로컬에 저장
        with open(local_file_path, "wb") as f:
            f.write(file_doc["file_data"])  # 파일 데이터를 바이너리로 저장

        logger.info(f"File with signature_id {signature_id} has been saved to {local_file_path}")

        # 3-1: 파일 PE 섹션 분석
        pe_info = check_Enc.analyze_pe_sections(file_doc["file_data"], is_path=False)
        
        # 3-2: 섹션 암호화 여부 확인
        encryption_status = check_Enc.check_file_encryption(pe_info)

        # 3-3: PE 섹션 정보를 MongoDB에 저장
        uploadDB_NorPE.store_normal_file_pe_info(signature_id, file_doc["filename"], file_doc["upload_ip"], pe_info, encryption_status)

        # 3-4: 파일 암호화 작업 실행
        encrypted_file_path = convert_NorToEnc.encrypt_with_themida(local_file_path, file_doc)
        if encrypted_file_path:
            logger.info(f"File {local_file_path} has been successfully encrypted.")
        else:
            logger.error(f"Encryption failed for file {local_file_path}.")

    except Exception as e:
        logger.error(f"Error storing file with signature_id {file_doc.get('signature_id', 'unknown')}: {e}", exc_info=True)
        print(f"Error storing file with signature_id {file_doc.get('signature_id', 'unknown')}. Check log for details.")
