import time
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests
import json
from logger_manager import setup_logger

# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\DB_handler', r'C:\VTAPImodules\log\DB_handler.log')

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = "vsapi"
FILES_COLLECTION = "file"
INFO_COLLECTION = "info"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# MongoDB에서 변경 사항 감지하여 실행하는 함수
def watch_for_file_uploads():
    collection = db[FILES_COLLECTION]
    logger.info("파일 업로드 감시 시작")
    with collection.watch() as stream:
        for change in stream:
            if change["operationType"] == "insert":
                file_data = change["fullDocument"]
                file_hash = file_data.get('filehash')  # MD5 해시 가져오기
                if file_hash:
                    logger.info(f"새로운 파일 업로드 감지: {file_hash}")
                    return file_hash, file_data

# MongoDB 업로드
def upload_to_mongodb(data, collection_name=FILES_COLLECTION):
    collection = db[collection_name]
    try:
        collection.insert_one(data)
        logger.info(f"Data uploaded to MongoDB: {collection_name}")
    except Exception as e:
        logger.error(f"MongoDB 업로드 실패: {e}")

# 해시가 MongoDB 'info' 컬렉션에 있는지 확인하는 함수
def check_hash_in_mongodb(file_hash):
    collection = db[INFO_COLLECTION]
    try:
        existing_data = collection.find_one({"md5": file_hash})
        if existing_data:
            logger.info(f"{file_hash} 이미 MongoDB 'info' 컬렉션에 존재합니다.")
            return existing_data
        else:
            logger.info(f"{file_hash} MongoDB 'info' 컬렉션에 존재하지 않음.")
    except Exception as e:
        logger.error(f"MongoDB 해시 검사 실패: {e}")
    return None
