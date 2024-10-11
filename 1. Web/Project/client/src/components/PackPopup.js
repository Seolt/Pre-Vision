import React from 'react';
import '../css/PackPopup.css';
import axios from 'axios';
import exeImg from '../images/exe.png';
import lockImg from '../images/lock.png';
import arrowGif from '../images/arrow.gif';
import { useState } from 'react';

// 팝업 컴포넌트 정의
function PackPopup({ isVisible, onClose, data }) {
    const [isChildPopupVisible, setIsChildPopupVisible] = useState(false); // child 팝업창을 만들기 위한 state

    // 팝업이 보이지 않으면 아무것도 렌더링하지 않음
    if (!isVisible) {
        return null;
    }

    const handleDownload = async (fileId, filename) => {
        try {
            // axios를 사용하여 파일 다운로드 요청
            const response = await axios.get(`/download-file/${fileId}`, {
                responseType: 'blob', // 서버로부터 binary 파일 데이터를 받을 수 있게 설정
            });

            const blob = new Blob([response.data], { type: 'application/octet-stream' }); // 받은 데이터를 Blob으로 변환
            const link = document.createElement('a');
            const url = window.URL.createObjectURL(blob);

            link.href = url;
            link.download = `Protected${filename}`;
            link.click();

            // 다운로드 후 URL 객체 해제
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error downloading the file:', error);
        }
    };

    const ShowChildPopup = () => {
        setIsChildPopupVisible(true); // 버튼을 누르면 내부 팝업 상태를 true로 변경
    };

    const CloseChildPopup = () => {
        setIsChildPopupVisible(false); // 내부 팝업을 닫기 위한 함수
    };

    function renderJson(obj) {
        return (
            <ul className="json">
                {Object.entries(obj).map(([key, value], index) => (
                    <li key={index}>
                        <span className="json-key">"{key}"</span>:{" "}
                        <span className="json-value">
                            {typeof value === 'object' && value !== null ? renderJson(value) : JSON.stringify(value)}
                        </span>
                    </li>
                ))}
            </ul>
        );
    }

    return (
        <>
            {/* 오버레이 추가: 배경을 검게 만들고 클릭 불가하게 */}
            <div className={`popup-overlay ${isVisible ? 'show' : ''}`}></div>
            {/* 팝업 오버레이 및 내용 */}
            <div className={`popup-container ${isVisible ? 'show' : ''}`}>
                <div className="popup-header">
                    <h2>File Information</h2>
                    <button className="popup-close" onClick={onClose}>✖</button>
                </div>
                <div className="info-data">
                    <div className="file-section-container">
                        <div>
                            <h3>Normal Files</h3>
                            <img className='exeImg' src={exeImg} alt="exe" />
                        </div>

                        {/* 가운데에 화살표 이미지 추가 */}
                        <div className="arrow-section">
                            <img className="arrowImg" src={arrowGif} alt="arrow" />
                        </div>

                        <div>
                            <h3>Encrypted Files</h3>
                            <img className='lockImg' src={lockImg} alt="lock" />
                        </div>
                    </div>
                    <br />
                    <br />
                    <div className="download-section">
                        {/* 다운로드 버튼 추가 */}
                        {data.encryptedFilesData.length > 0 ? (
                            data.encryptedFilesData.map((file, index) => (
                                <div key={index}>
                                    <p>Protected{file.original_filename}</p>
                                    <br />
                                        <button className='showPopupBtn' onClick={ShowChildPopup}>Protected File Info</button>
                                        <button className='downloadBtn' onClick={() => handleDownload(file.gridfs_file_id, file.original_filename)}>
                                            Download Protected File
                                        </button>
                                </div>
                            ))
                        ) : (
                            <p>No matching encrypted file data found</p> 
                        )}
                    </div>
                </div>
            </div>
            {/* 내부 팝업 */}
            {isChildPopupVisible && (
                <div className={`child-popup-overlay ${isChildPopupVisible ? 'show' : ''}`}>
                    <div className={`child-popup-container ${isChildPopupVisible ? 'show' : ''}`}>
                        <div className="child-popup-header">
                            <h2>Protected File Info</h2>
                            <button className="popup-close" onClick={CloseChildPopup}>✖</button>
                        </div>
                        <div className="child-info-data">
                            {data.encryptedFileInfo.length > 0 ? (
                                data.encryptedFileInfo.map((item, index) => (
                                    <div key={index}>{renderJson(item)}</div>
                                ))
                            ) : (
                                <p>No encrypted file info available</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

export default PackPopup;
