from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB 연결
client = MongoClient('mongodb://admin:qwer1234!@predb.yeonharin.com:27017/?authSource=admin&directConnection=true')

# 데이터베이스 선택
db = client['normal_files']
collection = db['filedata']

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

# 파일 경로 지정
#file_path = r'C:\Users\Administrator\Desktop\sample_data\PEview.exe'
#file_path = r'C:\Users\Administrator\Desktop\sample_data\notepad.exe'
file_path = r'C:\Users\Administrator\Desktop\sample_data\calc.exe'
# 파일명과 확장자 추출
filename = os.path.basename(file_path)  # 파일명 추출
file_extension = os.path.splitext(filename)[1]  # 확장자 추출 (예: .exe)

# 파일을 읽어서 바이너리 데이터로 변환
with open(file_path, 'rb') as file:
    file_data = file.read()

# signature_id 생성
signature_id = generate_signature_id()

# 파일 정보를 MongoDB에 삽입
file_document = {
    "signature_id": signature_id,
    "filename": filename,
    "file_extension": file_extension,  # 확장자 추가
    "file_data": file_data,
    "upload_time": datetime.now(),
    "upload_ip": "192.168.0.1"  # 적절한 IP를 입력하세요
}

# 데이터 삽입
collection.insert_one(file_document)

print(f"파일이 MongoDB에 성공적으로 업로드되었습니다. Signature ID: {signature_id}")
