import logging
import os

def setup_logger(log_file_path):
    """로그 파일 경로를 받아 로거를 설정"""
    logger = logging.getLogger(log_file_path)
    logger.setLevel(logging.INFO)

    # 중복 로그 방지
    if not logger.hasHandlers():
        # 로그 핸들러 설정
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
