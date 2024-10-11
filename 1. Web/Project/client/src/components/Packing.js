import React, { useState } from 'react';
import '../css/Packing.css';
import axios from 'axios';
import PackPopup from './PackPopup.js';

function Packing() {
    const [files, setFiles] = useState([]); // 업로드한 파일 리스트
    const [uploadStatus, setUploadStatus] = useState(''); // 업로드 상태 메시지 관리
    const [isUploading, setIsUploading] = useState(false); // 업로드 중 여부 상태 관리
    const [isPopupVisible, setIsPopupVisible] = useState(false); // 팝업창 표시 여부 상태 관리
    const [popupData, setPopupData] = useState([]); // 팝업에 표시할 데이터 상태 추가
    const [tooltipVisible, setTooltipVisible] = useState(false); // 툴팁 표시 여부 상태
    const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 }); // 툴팁 위치

    // 파일 선택 시 호출되는 함수
    const handleFileSelect = (e) => {
        const selectedFiles = e.target.files;
        handleFiles(selectedFiles);
    };

    // 파일 드래그 앤 드롭 시 호출되는 함수
    const handleDrop = (e) => {
        e.preventDefault();
        const droppedFiles = e.dataTransfer.files;
        handleFiles(droppedFiles);
    };

    // 드래그 중인 상태에서의 처리
    const handleDragOver = (e) => {
        e.preventDefault();
    };

    // 드래그 앤 드롭 존에 마우스를 올릴 때 툴팁 표시
    const handleMouseOver = (e) => {
        setTooltipVisible(true);
        setTooltipPosition({ x: e.clientX, y: e.clientY });
    };

    // 드래그 앤 드롭 존에서 마우스가 벗어날 때 툴팁 숨김
    const handleMouseOut = () => {
        setTooltipVisible(false);
    };

    // 드래그 앤 드롭 존에서 마우스가 이동할 때 툴팁 위치 갱신
    const handleMouseMove = (e) => {
        setTooltipPosition({ x: e.clientX, y: e.clientY });
    };

    // 파일 크기 및 확장자 제한을 처리하는 함수임
    const handleFiles = (fileList) => {
        const maxFileSize = 300 * 1024 * 1024; // 300MB로 제한
        const allowedExtensions = ['exe', 'dll'];

        // 파일을 하나만 허용함
        const file = fileList[0];
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (file.size > maxFileSize) {
            alert('파일은 300MB를 초과합니다.');
            return;
        }

        if (!allowedExtensions.includes(fileExtension)) {
            alert('허용되지 않는 파일 형식입니다. exe 또는 dll 파일만 업로드할 수 있습니다.');
            return;
        }

        setFiles([file]); // 파일을 상태에 저장
        setTooltipVisible(false); // 파일이 선택되면 툴팁을 숨김
    };

    // 파일을 서버에 업로드하는 함수
    const uploadFileToServer = async () => {
        if (files.length === 0) {
            alert('업로드할 파일이 없습니다.');
            return;
        }

        const formData = new FormData();
        formData.append('file', files[0]); // 첫 번째 파일만 업로드

        try {
            setIsUploading(true); // 업로드 시작 시 로딩 상태 활성화
            setUploadStatus(''); // 상태 초기화

            // 파일을 Express 서버로 POST 요청
            const response = await axios.post('/upload-file-pack', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            // 팝업에서 pe_info 데이터와 함께 표시
            setPopupData(response.data.peInfo);
            setUploadStatus(`파일이 성공적으로 업로드되었습니다: ${response.data.filename}`);
        } catch (error) {
            setUploadStatus('파일 업로드 중 오류가 발생했습니다.');
            console.error('Error uploading file:', error);
        } finally {
            setIsUploading(false); // 업로드가 완료되면 로딩 상태 비활성화
        }
    };

    return (
        <div className="packing-container">
            <h1>🔒</h1>
            <h2>안전하게 파일을 암호화하여 데이터를 보호하세요!</h2>

            {/* 파일이 업로드되었는지 확인 후 업로드된 파일이 없을 때만 파일 선택 창을 보여줌 */}
            {files.length === 0 ? (
                <div
                    id="drop-zone"
                    className="drop-zone"
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    onClick={() => document.getElementById('file-input').click()}
                    onMouseOver={handleMouseOver}
                    onMouseOut={handleMouseOut}
                    onMouseMove={handleMouseMove}
                >
                    <p>Drag & Drop your files here or click to select files</p>
                    <input
                        type="file"
                        id="file-input"
                        style={{ display: 'none' }}
                        onChange={handleFileSelect}
                    />
                </div>
            ) : (
                <button className='uploadBtn' onClick={uploadFileToServer} disabled={isUploading}>
                    Get Started!
                </button>
            )}

            {/* 업로드 중일 때 로딩 UI 표시 */}
            {isUploading && (
                <div className="loading-spinner">
                    <p>업로드 및 스캔 중... 잠시만 기다려 주세요.</p>
                    <div className="spinner"></div>
                </div>
            )}

            <ul id="file-list">
                {files.map((file, index) => {
                    // 파일 이름이 60글자를 넘으면 잘라내고 '...'을 추가
                    const shortenedName = file.name.length > 60 ? file.name.slice(0, 60) + '...' : file.name;
                    return <p key={index}>{`${shortenedName} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`}</p>;
                })}
            </ul>

            {/* 업로드 상태 메시지 */}
            {uploadStatus && <p>{uploadStatus}</p>}

            {/* 팝업을 띄우는 버튼 추가 */}
            {uploadStatus && (
                <button onClick={() => setIsPopupVisible(true)} className="open-popup-btn">
                    파일 구조 보기
                </button>
            )}

            {/* 팝업 컴포넌트 */}
            <PackPopup isVisible={isPopupVisible} onClose={() => setIsPopupVisible(false)} data={popupData} />

            {/* 툴팁 추가 */}
            {tooltipVisible && (
                <div
                    style={{
                        position: 'fixed',
                        top: tooltipPosition.y + 15,
                        left: tooltipPosition.x + 15,
                        backgroundColor: '#333',
                        color: 'white',
                        padding: '5px',
                        borderRadius: '5px',
                        fontSize: '12px',
                        zIndex: 1000,
                    }}
                >
                    Max size: 300MB
                </div>
            )}
        </div>
    );
}

export default Packing;
