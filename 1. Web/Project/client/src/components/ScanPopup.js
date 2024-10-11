import React, { useEffect } from 'react';
import '../css/ScanPopup.css';

// 팝업 컴포넌트 정의
function ScanPopup({ isVisible, onClose, data }) {

    // 팝업이 보이지 않으면 아무것도 렌더링하지 않음
    if (!isVisible) {
        return null;
    }

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
                    <h2>File Details</h2>
                    <button className="popup-close" onClick={onClose}>✖</button>
                </div>
                <div className="info-data">
                    {/* 데이터가 있을 경우 출력 */}
                    {data.length > 0 ? (
                        data.map((item, index) => (
                            <div key={index}>{renderJson(item)}</div>
                        ))
                    ) : (
                        <p>No matching data found</p> // 데이터가 없을 때 메시지 출력
                    )}
                </div>
            </div>
        </>
    );
}

export default ScanPopup; // Popup 컴포넌트를 외부에서 사용 가능하도록 export
