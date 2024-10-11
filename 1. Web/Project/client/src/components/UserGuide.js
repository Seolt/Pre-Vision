import React from 'react';
import '../css/UserGuide.css';
import virusScanGuide from '../images/virus-scan-guide.gif';
import packingGuide1 from '../images/packing-guide_1.gif';
import packingGuide2 from '../images/packing-guide_2.gif';
import packingGuide3 from '../images/packing-guide_3.gif';

function UserGuide() {
    return (
        <div>
            {/* UserGuide */}
            <div className="guide-container">
                <p className='guide-header'>사용자를 위한 시작 가이드👻</p>
                <div className="virus-guide-container">
                    <h1>Virus Scan👾</h1>
                    <br />
                    <br />
                    <h2>1. 파일을 업로드하고 구조를 확인해보세요.</h2>
                    <br />
                    <div className='guide-gif'>
                        <img src={virusScanGuide} alt='virus-scan-guide' />
                    </div>
                    <br />
                    <h2>💡사용자를 위한 데이터 구조 확인하기 Tip</h2>
                    <br />
                    <div className='virus-guide-container__tip'>
                        <h2 className='virus-guide-container__tip__h2'>Details</h2>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>Hash</h3>
                        <ul>
                            <li>- md5 : 파일의 MD5 해시값</li>
                            <li>- sha1 : 파일의 SHA1 해시값</li>
                            <li>- sha256 : 파일의 SHA256 해시값</li>
                            <li>- vhash : 파일의 VHash 해시값</li>
                            <li>- auth_hash : 인증 해시값</li>
                            <li>- imphash : Import Hash 해시값</li>
                            <li>- ssdeep : SSDEEP 해시값</li>
                            <li>- tlsh : TLSH 해시값</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>file_info</h3>
                        <ul>
                            <li>- md5 : 파일의 MD5 해시값</li>
                            <li>- file_type : 파일의 유형</li>
                            <li>- magic : 파일의 매직 넘버 또는 식별자</li>
                            <li>- file_size : 파일 크기</li>
                            <li>- PEID_packer : 파일에 사용된 패커 정보</li>
                            <li>- first_seen_time : 파일이 처음 발견된 시간</li>
                            <li>- name : 파일의 이름</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>signature</h3>
                        <p>파일 서명 데이터를 저장, 파일이 디지털 서명되어 있거나 인증된 경우 그 정보를 저장</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>pe_info</h3>
                        <p>PE(Portable Executable)파일에 대한 정보 PE 파일은 주로 Windows 운영 체제에서 실행되는 파일, PE 구조와 관련된 추가 정보</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>dot_net_assembly</h3>
                        <p>.NET 어셈블리 파일에 대한 정보를 저장 .NET 파일이 실행되는 동안 사용되는 메타데이터 및 코드 모듈 정보</p>
                        <br />

                        {/* behavior */}
                        <h2 className='virus-guide-container__tip__h2'>behavior</h2>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>mitre</h3>
                        <p>MITRE ATT&CK 프레임워크에 기반한 공격 기법 분석 정보를 저장 파일의 악성 활동이 MITRE ATT&CK의 어떤 공격 기법에 해당하는지에 대한 정보</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>Capabilities</h3>
                        <p>파일이 실행될 때 수행할 수 있는 기능에 대한 정보 (예 : 파일이 시스템 권한 상승, 키로깅, 백도어 생성 등의 악성 행동을 수행할 수 있는지에 대한 데이터)</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>tags</h3>
                        <p>분석된 파일의 행동에 따라 붙여진 태그를 저장 (예 : "ransomware", "spyware")</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>network_communications</h3>
                        <ul>
                            <li>- http_conversations : 파일이 서버와 주고받은 HTTP 요청 및 응답 정보</li>
                            <li>- ja3_digests : JA3 지문은 TLS 연결에서 클라이언트 측 정보를 해싱한 값, 특정 네트워크 패턴을 식별하는 데 사용</li>
                            <li>- memory_pattern_domains : 메모리에서 발견된 악성 도메인</li>
                            <li>- memory_pattern_ips : 메모리에서 발견된 IP 주소</li>
                            <li>- memory_pattern_urls : 메모리에서 발견된 URL 정보</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>file_system_actions</h3>
                        <ul>
                            <li>- files_opened : 파일이 열린 기록</li>
                            <li>- files_written : 파일이 작성된 기록</li>
                            <li>- files_deleted : 파일이 삭제된 기록</li>
                            <li>- files_attribute_changed : 파일 속성(예: 읽기 전용)이 변경된 기록</li>
                            <li>- files_dropped : 실행 도중 생성되거나 드롭된 파일에 대한 정보</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>registry_actions</h3>
                        <ul>
                            <li>- registry_keys_opened : 파일이 접근한 레지스트리 키</li>
                            <li>- registry_keys_set : 파일이 설정한 레지스트리 키</li>
                            <li>- registry_keys_deleted : 파일이 삭제한 레지스트리 키</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>process_and_service_actions</h3>
                        <ul>
                            <li>- processes_created : 파일이 생성한 프로세스 정보</li>
                            <li>- command_executions : 파일이 실행한 명령어</li>
                            <li>- processes_injected : 파일이 다른 프로세스에 주입한 내용</li>
                            <li>- processes_terminated : 파일이 종료한 프로세스</li>
                            <li>- services_opened : 파일이 실행한 서비스 관련 정보</li>
                            <li>- processes_tree : 파일이 생성한 프로세스 트리 구조</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>synchronization_mechanisms_signals</h3>
                        <ul>
                            <li>- mutexes_created : 파일이 생성한 mutex 객체</li>
                            <li>- mutexes_opened : 파일이 열린 mutex 객체</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>modules_loaded</h3>
                        <p>파일이 실행 중에 로드한 모듈을 기록, 악성 파일이 추가적으로 로드하는 라이브러리나 코드</p>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>highlighted_actions</h3>
                        <ul>
                            <li>- calls_highlighted : 중요하거나 특이한 시스템 호출</li>
                            <li>- text_decoded : 실행 중에 디코딩된 텍스트</li>
                        </ul>
                        <br />
                        <h3 className='virus-guide-container__tip__h3'>system_property_lookups</h3>
                        <p>파일이 조회한 시스템 속성 정보(예 :  파일이 시스템 버전, 사용자 정보, 설치된 소프트웨어 정보를 확인하려는 시도 등)</p>
                        <br />
                    </div>
                </div>
                <div className="packing-guide-container">
                    <h1>Packing🔒</h1>
                    <br />
                    <br />
                    <h2>1. 보호하고 싶은 파일을 업로드해주세요.</h2>
                    <br />
                    <div className='guide-gif'>
                        <img src={packingGuide1} alt='packing-guide1' />
                    </div>
                    <br />
                    <h2>2. 파일 보호화가 진행되는 동안 기다려주세요.</h2>
                    <br />
                    <div className='guide-gif'>
                        <span className='packing-guide-container__forward'>⏩6X</span>
                        <img src={packingGuide2} alt='packing-guide2' />
                    </div>
                    <br />
                    <h2>3. 보호된 파일을 다운받아 안전하게 사용하세요.</h2>
                    <br />
                    <div className='guide-gif'>
                        <img src={packingGuide3} alt='packing-guide3' />
                    </div>
                    <br />
                    <h2>💡사용자를 위한 데이터 구조 확인하기 Tip</h2>
                    <br />
                    <div className='packing-guide-container__tip'>
                        <h2 className='packing-guide-container__tip__h2'>Encrypted_filename</h2>
                        <p>암호화된 파일의 파일 경로 (예:
                            "20240909-002_protected.exe")</p>
                        <br />
                        <h2 className='packing-guide-container__tip__h2'>encrypted_upload_time</h2>
                        <p>암호화된 파일의 업로드 시간</p>
                        <br />
                        <h2 className='packing-guide-container__tip__h2'>upload_ip</h2>
                        <p>파일을 업로드한 IP 주소</p>
                        <br />
                        <h2 className='packing-guide-container__tip__h2'>pe_info </h2>
                        <p>암호화된 파일의 PE 분석 정보가 포함된 객체</p>
                        <br />
                        <h2 className='packing-guide-container__tip__h2'>encrypted</h2>
                        <p>암호화된 섹션 정보가 포함된 객체</p>
                        <br />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default UserGuide;
