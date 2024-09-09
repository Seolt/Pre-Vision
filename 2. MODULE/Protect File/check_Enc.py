from pefile import PE
from logging_Utils import setup_logger  # logging_Utils에서 로거 설정 함수 가져오기
import hashlib

# 로그 파일 설정
log_file = r'C:\pymodules\log\check_enc.log'
logger = setup_logger(log_file)  # logging_utils의 setup_logger 사용

def analyze_pe_sections(file_input, is_path=False):
    """
    PE 파일의 섹션을 분석하고, 필요한 섹션 정보를 추출
    :param file_input: 파일 경로 또는 파일 데이터
    :param is_path: True면 파일 경로로 처리, False면 파일 데이터로 처리
    :return: 섹션 정보가 담긴 딕셔너리
    """
    try:
        # 파일 경로로 분석할지, 파일 데이터로 분석할지 결정
        if is_path:
            pe = PE(file_input)  # 파일 경로를 사용한 경우
        else:
            pe = PE(data=file_input)  # 파일 데이터를 사용한 경우

        sections = {}

        for section in pe.sections:
            section_name = section.Name.decode('utf-8').rstrip('\x00')

            # 섹션의 MD5 해시 계산
            section_data = section.get_data()
            section_md5 = hashlib.md5(section_data).hexdigest()

            # 추가적인 섹션 정보 추출
            sections[section_name] = {
                "virtual_address": section.VirtualAddress,  # 메모리 상의 가상 주소
                "virtual_size": section.Misc_VirtualSize,  # 메모리 로드 시 크기
                "raw_size": section.SizeOfRawData,  # 실제 파일에서의 크기
                "entropy": section.get_entropy(),  # 엔트로피
                "md5_hash": section_md5,  # 섹션의 MD5 해시
                "characteristics": section.Characteristics,  # 섹션의 권한 정보 (읽기/쓰기/실행)
                "permissions": {
                    "readable": bool(section.Characteristics & 0x40000000),
                    "writable": bool(section.Characteristics & 0x80000000),
                    "executable": bool(section.Characteristics & 0x20000000),
                },
                # PE 값 추가
                "pointer_to_raw_data": section.PointerToRawData,  # 파일 내에서 섹션의 시작 위치
                "section_alignment": pe.OPTIONAL_HEADER.SectionAlignment  # 섹션의 메모리 정렬 값
            }

        logger.info("PE section analysis completed successfully.")
        return sections

    except Exception as e:
        logger.error(f"Error during PE section analysis: {e}", exc_info=True)
        return {}

# 섹션이 암호화되었는지 확인하는 함수
def is_section_encrypted(section):
    entropy_threshold = 7.0  # 예시 임계값 (일반적으로 7.0 이상이 암호화된 섹션으로 간주됨)
    return section['entropy'] > entropy_threshold

# 파일의 섹션 암호화 상태를 확인하는 함수
def check_file_encryption(pe_info):
    encryption_status = {}

    try:
        for section_name, section_data in pe_info.items():
            encrypted = is_section_encrypted(section_data)
            encryption_status[section_name] = encrypted
            logger.info(f"Section {section_name}: {'Encrypted' if encrypted else 'Not Encrypted'} (Entropy: {section_data['entropy']})")

        logger.info("File encryption status check completed successfully.")
        return encryption_status

    except Exception as e:
        logger.error(f"Error during file encryption status check: {e}", exc_info=True)
        return {}
