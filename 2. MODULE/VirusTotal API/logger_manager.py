import logging
import os

def setup_logger(logger_name, log_file, level=logging.INFO):
    

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # 파일 핸들러 설정 (UTF-8 인코딩 추가)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger
