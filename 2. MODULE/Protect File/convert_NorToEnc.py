import subprocess
import os
from logging_Utils import setup_logger
from datetime import datetime
import uploadDB_Enc  # MongoDB에 암호화된 파일을 저장하는 모듈
import uploadDB_EncPE  # MongoDB에 암호화된 파일 PE를 저장하는 모듈
import check_Enc

# 로그 파일 설정
log_file = r'C:\pymodules\log\file_encryption.log'
logger = setup_logger(log_file)

def encrypt_with_themida(input_file, original_file_doc):
    """
    Themida로 파일 암호화하고, Themida 작업 완료 후 암호화된 파일의 PE를 분석하여 MongoDB에 저장
    :param input_file: 원본 파일 경로
    :param original_file_doc: 원본 파일의 메타데이터 (DB에서 가져온 정보)
    :return: 암호화된 파일 경로 또는 None
    """
    try:
        # 암호화된 파일을 저장할 경로 설정
        today_date = datetime.today().strftime('%Y-%m-%d')
        protected_folder_path = os.path.join(r'C:\DBFiles', today_date, 'protected')

        # 폴더가 존재하지 않으면 생성
        if not os.path.exists(protected_folder_path):
            os.makedirs(protected_folder_path)

        # 암호화된 파일명을 설정
        file_name, file_extension = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(protected_folder_path, f"{file_name}_protected{file_extension}")

        logger.info(f"Starting encryption for file: {input_file}")

        # 배치 파일 경로 (환경에 맞게 수정)
        bat_file_path = r"C:\pymodules\bat\themida_encrypt.bat"

        # 배치 파일 실행, stdout과 stderr를 로그로 기록
        result = subprocess.run([bat_file_path, input_file, output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # 배치 파일 실행 후 결과 확인
        if result.returncode == 0:
            logger.info(f"File {input_file} has been encrypted successfully to {output_file}")
            logger.info(f"Batch file output: {result.stdout.decode()}")  # 배치 파일 출력 로그

            # 암호화가 완료된 파일을 MongoDB에 저장
            uploadDB_Enc.store_encrypted_file(output_file, original_file_doc)  # MongoDB에 저장
            logger.info(f"Encrypted file {output_file} has been saved to MongoDB.")
            
            # Themida 암호화 작업이 완료된 후, PE 섹션 분석 진행
            analyze_and_store_pe(output_file, original_file_doc)

            return output_file
        else:
            logger.error(f"Error in Themida encryption for {input_file}: Return code {result.returncode}")
            logger.error(f"Error message: {result.stderr.decode()}")  # 배치 파일 오류 로그
            return None

    except Exception as e:
        logger.error(f"Error during encryption for {input_file}: {e}", exc_info=True)
        return None

def analyze_and_store_pe(encrypted_file, original_file_doc):
    """
    Themida 암호화 작업이 끝난 후 암호화된 파일의 PE를 분석하고, MongoDB에 저장
    :param encrypted_file: 암호화된 파일 경로
    :param original_file_doc: 원본 파일의 메타데이터 (DB에서 가져온 정보)
    """
    try:
        # 1: 파일 PE 섹션 분석
        pe_info = check_Enc.analyze_pe_sections(encrypted_file, is_path=True)
        
        # 2: 섹션 암호화 여부 확인
        encryption_status = check_Enc.check_file_encryption(pe_info)

        # 3: MongoDB에 PE 정보와 암호화 여부 저장
        signature_id = original_file_doc["signature_id"]
        uploadDB_EncPE.store_encrypted_file_pe_info(signature_id, encrypted_file, original_file_doc["upload_ip"], pe_info, encryption_status)

        logger.info(f"PE information and encryption status for encrypted file {encrypted_file} successfully stored in MongoDB.")

    except Exception as e:
        logger.error(f"Error during PE analysis for encrypted file {encrypted_file}: {e}", exc_info=True)
