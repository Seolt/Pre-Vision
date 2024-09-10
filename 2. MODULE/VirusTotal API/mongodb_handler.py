from pymongo import MongoClient
import os
from dotenv import load_dotenv

# .env 파일에서 MongoDB URI 로드
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = "vsapi"
INFO_COLLECTION = "info"

# MongoDB 연결
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# MongoDB에 데이터 업로드
def upload_to_mongodb(data, collection_name=INFO_COLLECTION):
    collection = db[collection_name]

    # 데이터에서 '_id' 필드를 제거하여 MongoDB에서 자동 생성되도록 함
    if '_id' in data:
        del data['_id']
    
    collection.insert_one(data)
    print(f"Data uploaded to MongoDB: {collection_name}")

