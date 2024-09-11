import json
import os
from logger_manager import setup_logger

# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\data_converter', r'C:\VTAPImodules\log\data_converter.log')

def convert_data(details, behavior):
    logger.info("데이터 변환 시작")

    try:
        template_file_path = r"C:\VTAPImodules\template.json"
        with open(template_file_path, 'r', encoding='utf-8') as template_file:
            json_data = json.load(template_file)

        detail_data_attribute = details.get("data", {}).get("attributes", {})
        json_data["md5"] = detail_data_attribute.get("md5", None)

        # 해시 정보
        json_data["details"]["hash"]["md5"] = detail_data_attribute.get("md5", None)
        json_data["details"]["hash"]["sha1"] = detail_data_attribute.get("sha1", None)
        json_data["details"]["hash"]["sha256"] = detail_data_attribute.get("sha256", None)
        json_data["details"]["hash"]["vhash"] = detail_data_attribute.get("vhash", None)
        json_data["details"]["hash"]["auth_hash"] = detail_data_attribute.get("authentihash", None)
        json_data["details"]["hash"]["imphash"] = detail_data_attribute.get("pe_info", {}).get("imphash", None)
        json_data["details"]["hash"]["ssdeep"] = detail_data_attribute.get("ssdeep", None)
        json_data["details"]["hash"]["tlsh"] = detail_data_attribute.get("tlsh", None)

        # 파일 정보
        json_data["details"]["file_info"]["md5"] = detail_data_attribute.get("md5", None)
        json_data["details"]["file_info"]["file_type"] = detail_data_attribute.get("type_tags", None)
        json_data["details"]["file_info"]["magic"] = detail_data_attribute.get("magic", None)
        json_data["details"]["file_info"]["file_size"] = detail_data_attribute.get("size", None)
        json_data["details"]["file_info"]["PEID_packer"] = detail_data_attribute.get("packers", {}).get("PEiD", None)
        json_data["details"]["file_info"]["first_seen_time"] = detail_data_attribute.get("first_submission_date", None)

        # 이름 정보
        json_data["details"]["file_info"]["name"] = detail_data_attribute.get("names", None)

        # 시그니처 정보
        json_data["details"]["signature"] = detail_data_attribute.get("signature_info", {})

        json_data["details"]["pe_info"] = detail_data_attribute.get("pe_info", {})
        json_data["details"]["dot_net_assembly"] = detail_data_attribute.get("dot_net_assembly", {})

        if behavior is None or behavior.get("data") is None:
            logger.info("Behavior 데이터가 없음")
            return json_data

        # MITRE 공격 기법 정보 추가
        mitre_techniques = behavior.get("data", {}).get("mitre_attack_techniques", {})
        for technique in mitre_techniques:
            technique_id = technique.get("id")
            description = technique.get("signature_description")
            severity = technique.get("severity", "")

            json_data["behavior"]["mitre"][technique_id] = {
                "description": description,
                "severity": severity
            }

        # 행동 정보 추가
        json_data["behavior"]["modules_loaded"] = behavior.get("data", {}).get("modules_loaded", {})
        json_data["behavior"]["tags"] = behavior.get("data", {}).get("tags", {})

        # Capabilities 처리
        capabilities_comms = behavior.get("data", {}).get("signature_matches", {})
        for comm in capabilities_comms:
            if comm.get("format") == "SIG_FORMAT_CAPA":
                capa_name = comm.get("name")
                description = comm.get("description")
                authors = comm.get("authors")
                rule_src = comm.get("rule_src")
                refs = comm.get("refs", {})
                json_data["behavior"]["Capabilities"][capa_name] = {
                    "authors": authors,
                    "description": description,
                    "rule": rule_src,
                    "refs": refs
                }

        # 네트워크 통신 정보
        network_communications = ["ja3_digests", "http_conversations", "memory_pattern_domains", "memory_pattern_urls",
                                  "memory_pattern_ips", "tls"]
        for net_comm in network_communications:
            col = behavior.get("data", {}).get(net_comm, {})
            json_data["behavior"]["network_communications"][net_comm] = col

        # 파일 작업 정보
        file_actions = ["files_opened", "files_written", "files_deleted", "files_attribute_changed", "files_dropped"]
        for file_comm in file_actions:
            col = behavior.get("data", {}).get(file_comm, {})
            json_data["behavior"]["file_system_actions"][file_comm] = col

        # 레지스트리 작업 정보
        registry_actions = ["registry_keys_opened", "registry_keys_set", "registry_keys_deleted"]
        for reg_comm in registry_actions:
            col = behavior.get("data", {}).get(reg_comm, {})
            json_data["behavior"]["registry_actions"][reg_comm] = col

        # 프로세스 및 서비스 작업 정보
        process_and_service_actions = ["processes_created", "command_executions", "processes_injected",
                                       "processes_terminated", "services_opened", "processes_tree"]
        for pas_comm in process_and_service_actions:
            col = behavior.get("data", {}).get(pas_comm, {})
            json_data["behavior"]["process_and_service_actions"][pas_comm] = col

        # 동기화 메커니즘 정보
        synchronization_mechanisms_signals = ["mutexes_created", "mutexes_opened"]
        for sms_comm in synchronization_mechanisms_signals:
            col = behavior.get("data", {}).get(sms_comm, {})
            json_data["behavior"]["synchronization_mechanisms_signals"][sms_comm] = col

        # 강조된 작업 정보
        highlighted_actions = ["calls_highlighted", "text_decoded"]
        for high_comm in highlighted_actions:
            col = behavior.get("data", {}).get(high_comm, {})
            json_data["behavior"]["highlighted_actions"][high_comm] = col

        # 시스템 속성 조회
        system_property_lookups = behavior.get("data", {}).get("system_property_lookups", {})
        json_data["behavior"]["system_property_lookups"] = system_property_lookups

        logger.info("데이터 변환 완료")
        return json_data

    except Exception as e:
        logger.error(f"데이터 변환 중 오류 발생: {e}")
        return None
