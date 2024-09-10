import os
import gridfs
from pymongo import MongoClient
from bson import ObjectId
from logging_Utils import setup_logger
from dotenv import load_dotenv

load_dotenv()
#env에서 로드
MONGO_URI=os.getenv("MONGO_URI")
# 로그 설정
log_file = r'C:\pymodules\log\file_retrieval.log'
logger = setup_logger(log_file)

# MongoDB 연결 설정
client = MongoClient(MONGO_URI)
db = client['encrypted_files']  # 'encrypted_files' 데이터베이스 사용
fs = gridfs.GridFS(db)  # GridFS 객체 생성

def retrieve_encrypted_file(file_id):
    """
    GridFS에서 파일 ID를 사용해 파일을 다운로드합니다.
    :param file_id: GridFS에 저장된 파일의 ID (ObjectId)
    :return: 파일 데이터 (바이너리) 또는 None
    """
    try:
        # GridFS에서 파일 ID를 이용해 파일을 가져옴
        file_data = fs.get(file_id).read()  # 파일 데이터를 읽음
        logger.info(f"File with ID {file_id} has been retrieved from MongoDB.")
        return file_data
    except Exception as e:
        logger.error(f"Error retrieving file with ID {file_id}: {e}", exc_info=True)
        return None

def save_file_to_local(file_data, save_path):
    """
    파일 데이터를 로컬에 저장합니다.
    :param file_data: 가져온 파일의 바이너리 데이터
    :param save_path: 파일을 저장할 경로
    """
    try:
        # 로컬 경로에 파일 저장
        with open(save_path, 'wb') as f:
            f.write(file_data)
        logger.info(f"File has been saved to {save_path}")
        print(f"File saved successfully to {save_path}")
    except Exception as e:
        logger.error(f"Error saving file to {save_path}: {e}", exc_info=True)

if __name__ == "__main__":
    # 사용자로부터 파일 ID 입력 받음 (실제 MongoDB GridFS에 저장된 파일의 ObjectId)
    file_id_str = input("Enter the GridFS file ID (ObjectId format): ")

    try:
        # 입력된 문자열을 ObjectId로 변환
        file_id = ObjectId(file_id_str)
    except Exception as e:
        print(f"Invalid ObjectId format: {e}")
        logger.error(f"Invalid ObjectId format: {e}")
        exit(1)

    # GridFS에서 파일 가져오기
    file_data = retrieve_encrypted_file(file_id)

    if file_data:
        # 가져온 파일 데이터를 로컬 파일로 저장
        save_path = input("Enter the path where you want to save the file: ")
        save_file_to_local(file_data, save_path)
    else:
        print("Failed to retrieve the file from MongoDB.")
