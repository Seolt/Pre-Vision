import json


def convert_data(details, behavior, template):
    
    detail_data_attribute = details.get("data", {}).get("attributes", {})
    template["md5"]=detail_data_attribute.get("md5", None)
    # 해시 정보
    template["details"]["hash"]["md5"] = detail_data_attribute.get("md5", None)
    template["details"]["hash"]["sha1"] = detail_data_attribute.get("sha1", None)
    template["details"]["hash"]["sha256"] = detail_data_attribute.get("sha256", None)
    template["details"]["hash"]["vhash"] = detail_data_attribute.get("vhash", None)
    template["details"]["hash"]["auth_hash"] = detail_data_attribute.get("authentihash", None)
    template["details"]["hash"]["imphash"] = detail_data_attribute.get("pe_info", {}).get("imphash", None)
    template["details"]["hash"]["ssdeep"] = detail_data_attribute.get("ssdeep", None)
    template["details"]["hash"]["tlsh"] = detail_data_attribute.get("tlsh", None)

    # 파일 정보
    template["details"]["file_info"]["md5"] = detail_data_attribute.get("md5", None)
    template["details"]["file_info"]["file_type"] = detail_data_attribute.get("type_tags", None)
    template["details"]["file_info"]["magic"] = detail_data_attribute.get("magic", None)
    template["details"]["file_info"]["file_size"] = detail_data_attribute.get("size", None)
    template["details"]["file_info"]["PEID_packer"] = detail_data_attribute.get("packers", {}).get("PEiD", None)
    template["details"]["file_info"]["first_seen_time"] = detail_data_attribute.get("first_submission_date",
                                                                                           None)

    # 이름 정보
    template["details"]["file_info"]["name"] = detail_data_attribute.get("names", None)

    # 시그니처 정보
    template["details"]["signature"] = detail_data_attribute.get("signature_info", {})

    template["details"]["pe_info"] = detail_data_attribute.get("pe_info", {})
    template["details"]["dot_net_assembly"] = detail_data_attribute.get("dot_net_assembly", {})
    if behavior is None or behavior.get("data") is None:
        return template  # 혹은 적절한 리턴 값을 설정
        
    # virustotal_behavior.json에서 행동 정보 추가
    # MITRE 공격 기법 정보 추가
    mitre_techniques = behavior.get("data", {}).get("mitre_attack_techniques", {})
    for technique in mitre_techniques:
        technique_id = technique.get("id")
        description = technique.get("signature_description")
        severity = technique.get("severity", "")

        template["behavior"]["mitre"][technique_id] = {
            "description": description,
            "severity": severity
        }

    template["behavior"]["modules_loaded"] = behavior.get("data", {}).get("modules_loaded", {})
    template["behavior"]["tags"] = behavior.get("data", {}).get("tags", {})

    capabilities_comms = behavior.get("data", {}).get("signature_matches", {})
    for comm in capabilities_comms:
        if comm.get("format") == "SIG_FORMAT_CAPA":
            capa_name = comm.get("name")
            description = comm.get("description")
            authors = comm.get("authors")
            rule_src = comm.get("rule_src")
            refs = comm.get("refs", {})
            template["behavior"]["Capabilities"][capa_name] = {
                "authors": authors,
                "description": description,
                "rule": rule_src,
                "refs": refs
            }

    network_communications = ["ja3_digests", "http_conversations", "memory_pattern_domains", "memory_pattern_urls",
                              "memory_pattern_ips", "tls"]
    for net_comm in network_communications:
        col = behavior.get("data", {}).get(net_comm, {})
        template["behavior"]["network_communications"][net_comm] = col

    file_actions = ["files_opened", "files_written", "files_deleted", "files_attribute_changed", "files_dropped"]
    for file_comm in file_actions:
        col = behavior.get("data", {}).get(file_comm, {})
        template["behavior"]["file_system_actions"][file_comm] = col

    registry_actions = ["registry_keys_opened", "registry_keys_set", "registry_keys_deleted"]
    for reg_comm in registry_actions:
        col = behavior.get("data", {}).get(reg_comm, {})
        template["behavior"]["registry_actions"][reg_comm] = col

    process_and_service_actions = ["processes_created", "command_executions", "processes_injected",
                                   "processes_terminated", "services_opened", "processes_tree"]
    for pas_comm in process_and_service_actions:
        col = behavior.get("data", {}).get(pas_comm, {})
        template["behavior"]["process_and_service_actions"][pas_comm] = col

    synchronization_mechanisms_signals = ["mutexes_created", "mutexes_opened"]
    for sms_comm in synchronization_mechanisms_signals:
        col = behavior.get("data", {}).get(sms_comm, {})
        template["behavior"]["synchronization_mechanisms_signals"][sms_comm] = col

    highlighted_actions = ["calls_highlighted", "text_decoded"]
    for high_comm in highlighted_actions:
        col = behavior.get("data", {}).get(high_comm, {})
        template["behavior"]["highlighted_actions"][high_comm] = col

    system_property_lookups = behavior.get("data", {}).get("system_property_lookups", {})
    template["behavior"]["system_property_lookups"] = system_property_lookups

    return template
