import hashlib
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 MongoDB URI 로드
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = "vsapi"
FILES_COLLECTION = "file"

# MongoDB 연결
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[FILES_COLLECTION]

# MD5 해시 계산 함수
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):  # 파일을 8192 바이트씩 읽어서 해시 계산
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# signature_id 생성 함수
def generate_signature_id():
    # 오늘의 날짜 (YYYYMMDD 형식)
    today = datetime.now().strftime("%Y%m%d")

    # 오늘 날짜로 시작하는 signature_id의 개수를 확인하여 번호를 매김
    count = collection.count_documents({"signature_id": {"$regex": f"^{today}-"}})
    next_id = count + 1

    # signature_id를 YYYYMMDD-번호 형식으로 생성
    signature_id = f"{today}-{next_id:03d}"
    return signature_id

# 파일 업로드 함수
def upload_file_to_mongodb(file_path, upload_ip):
    filehash = calculate_md5(file_path)
    filename = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        file_data = f.read()

    # 고유한 signature_id 생성
    signature_id = generate_signature_id()

    file_metadata = {
        "signature_id": signature_id,
        "filehash": filehash,
        "filename": filename,
        "file_data": file_data,  # 실제 파일 데이터
        "upload_time": datetime.now(),
        "upload_ip": upload_ip
    }

    # MongoDB에 저장
    collection.insert_one(file_metadata)
    print(f"파일 {filename}가 MongoDB에 업로드되었습니다. MD5: {filehash}, Signature ID: {signature_id}")


# 테스트 파일 경로와 IP
test_file_path = r"C:\Users\Administrator\Desktop\sample_data\Acrobat_protected.exe"
test_upload_ip = "192.168.0.1"

# 파일을 MongoDB에 업로드
upload_file_to_mongodb(test_file_path, test_upload_ip)
