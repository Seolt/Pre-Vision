from pymongo import MongoClient
import downloadDB_Nor  # 파일 저장 모듈
from logging_Utils import setup_logger  # 공통 로그 설정 함수

# 로그 설정
log_file = r'C:\pymodules\log\db_monitor.log'
logger = setup_logger(log_file)

def monitor_files():
    """MongoDB Change Stream을 사용하여 normal_files.filedata 테이블을 모니터링"""
    try:
        # MongoDB에 연결
        client = MongoClient('mongodb://admin:qwer1234!@predb.yeonharin.com:27017/?authSource=admin&directConnection=true')
        db = client['normal_files']

        # Change Streams로 normal_files에서 파일 업로드를 감시
        with db.filedata.watch() as stream:
            logger.info("Started monitoring new files in MongoDB using Change Streams.")
            for change in stream:
                if change["operationType"] == "insert":
                    file_doc = change["fullDocument"]
                    logger.info(f"New file detected: {file_doc['filename']}")
                    
                    # 2번째 단계: 파일을 로컬에 저장하는 모듈 호출
                    local_file_path = downloadDB_Nor.store_file(file_doc)
                    if local_file_path:
                        logger.info(f"File {file_doc['filename']} has been saved to {local_file_path}")
                    else:
                        logger.error(f"Failed to save file {file_doc['filename']} to local storage.")
                    
                else:
                    logger.info(f"Ignored operation: {change['operationType']}")
                    
    except Exception as e:
        logger.error(f"Error occurred during file monitoring: {e}", exc_info=True)

if __name__ == "__main__":
    monitor_files()
