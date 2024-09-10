CREATE TABLE details (
    id SERIAL PRIMARY KEY
);

CREATE TABLE hash (
    id SERIAL PRIMARY KEY,
    details_id INT REFERENCES details(id),
    md5 VARCHAR(255),
    sha1 VARCHAR(255),
    sha256 VARCHAR(255),
    vhash VARCHAR(255),
    auth_hash VARCHAR(255),
    imphash VARCHAR(255),
    ssdeep VARCHAR(255),
    tlsh VARCHAR(255)
);

CREATE TABLE file_info (
    id SERIAL PRIMARY KEY,
    details_id INT REFERENCES details(id),
    md5 VARCHAR(255),
    file_type VARCHAR(255),
    magic VARCHAR(255),
    file_size VARCHAR(255),
    PEID_packer VARCHAR(255),
    first_seen_time VARCHAR(255)
);

CREATE TABLE name (
    id SERIAL PRIMARY KEY,
    file_info_id INT REFERENCES file_info(id),
    name1 VARCHAR(255),
    name2 VARCHAR(255)
);

CREATE TABLE signature (
    id SERIAL PRIMARY KEY,
    details_id INT REFERENCES details(id),
    verification VARCHAR(255)
);

CREATE TABLE pe_info (
    id SERIAL PRIMARY KEY,
    details_id INT REFERENCES details(id),
    net_details TEXT,
    header TEXT,
    sections TEXT,
    imports TEXT,
    contained_resources TEXT
);

CREATE TABLE dot_net_assembly (
    id SERIAL PRIMARY KEY,
    details_id INT REFERENCES details(id),
    general TEXT,
    streams TEXT,
    manifest_resource TEXT,
    external_assemblies TEXT,
    assembly_data TEXT,
    type_definitions TEXT,
    external_modules TEXT,
    unmanaged_method_list TEXT
);

CREATE TABLE behavior (
    id SERIAL PRIMARY KEY
);

CREATE TABLE behavior_tags (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id)
);

CREATE TABLE mitre (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    privilege_escalation TEXT,
    defense_evasion TEXT,
    discovery TEXT,
    collection TEXT,
    command_and_control TEXT
);

CREATE TABLE capabilities (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id)
);

CREATE TABLE network_communications (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    DNS_resolutions TEXT,
    IP_traffic TEXT,
    JA3_digests TEXT,
    TLS TEXT
);

CREATE TABLE behavior_similarity_hashes (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    CAPA VARCHAR(255),
    Microsoft_Sysinternals VARCHAR(255),
    Tencent_HABO VARCHAR(255),
    Yomi_Hunter VARCHAR(255),
    Zenbox VARCHAR(255)
);

CREATE TABLE file_system_actions (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    file_opened TEXT,
    files_written TEXT,
    files_deleted TEXT,
    files_copied TEXT,
    files_dropped TEXT
);

CREATE TABLE registry_actions (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    registry_keys_opened TEXT,
    registry_keys_set TEXT
);

CREATE TABLE process_and_service_actions (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    processes_created TEXT,
    shell_commands TEXT,
    processes_terminated TEXT,
    process_tree TEXT
);

CREATE TABLE synchronization_mechanisms_signal (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    mutexes_created TEXT,
    mutexes_opened TEXT
);

CREATE TABLE modules_loaded (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    runtime_modules TEXT
);

CREATE TABLE highlighted_actions (
    id SERIAL PRIMARY KEY,
    behavior_id INT REFERENCES behavior(id),
    calls_highlighted TEXT,
    highlighted_text TEXT
);
