from pymongo import MongoClient
import gridfs
import downloadDB_Nor  # 파일 저장 모듈
from logging_Utils import setup_logger  # 공통 로그 설정 함수
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# 로그 설정
log_file = r'C:\pymodules\log\db_monitor.log'
logger = setup_logger(log_file)

def monitor_files():
    """MongoDB Change Stream을 사용하여 normal_files.filedata 테이블을 모니터링"""
    try:
        # MongoDB에 연결
        client = MongoClient(MONGO_URI)
        db = client['normal_files']
        fs = gridfs.GridFS(db)  # GridFS 인스턴스 생성

        # Change Streams로 normal_files에서 파일 업로드를 감시
        with db.filedata.watch() as stream:
            logger.info("Started monitoring new files in MongoDB using Change Streams.")
            for change in stream:
                if change["operationType"] == "insert":
                    file_doc = change["fullDocument"]
                    logger.info(f"New file detected: {file_doc['filename']}")
                    
                    # GridFS에서 파일 가져오기 (gridfs_file_id를 사용)
                    gridfs_file_id = file_doc.get('gridfs_file_id')
                    if gridfs_file_id:
                        try:
                            # GridFS에서 파일 데이터를 가져옴
                            grid_out = fs.get(gridfs_file_id)
                            file_data = grid_out.read()
                            
                            # 로컬에 파일 저장 (파일 저장 모듈에 맞게 수정 필요)
                            local_file_path = downloadDB_Nor.store_file(file_doc, file_data)
                            if local_file_path:
                                logger.info(f"File {file_doc['filename']} has been saved to {local_file_path}")
                            else:
                                logger.error(f"Failed to save file {file_doc['filename']} to local storage.")
                        except gridfs.errors.NoFile:
                            logger.error(f"File not found in GridFS for file ID: {gridfs_file_id}")
                    else:
                        logger.error(f"No gridfs_file_id found in the document for file: {file_doc['filename']}")
                    
                else:
                    logger.info(f"Ignored operation: {change['operationType']}")
                    
    except Exception as e:
        logger.error(f"Error occurred during file monitoring: {e}", exc_info=True)

if __name__ == "__main__":
    monitor_files()
