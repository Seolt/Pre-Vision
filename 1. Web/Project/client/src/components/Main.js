import React from 'react';
import { Link } from 'react-router-dom'; // React Router의 Link 컴포넌트 임포트
import '../css/Main.css';
import codeImg from '../images/code.jpg';
import hackerImg from '../images/hacker.jpg';
import hacker2Img from '../images/hacker2.jpg';
import laptopImg from '../images/laptop.jpg';
import sourceImg from '../images/source.jpg';
import lockerImg from '../images/locker.jpg';
import malwarefoundImg from '../images/malwarefound.jpg';

function Main() {
    return (
        <>
            <div className="slider">
                <div className="slide">
                    <img src={codeImg} alt="Image 1" />
                </div>
                <div className="slide">
                    <img src={hackerImg} alt="Image 2" />
                </div>
                <div className="slide">
                    <img src={hacker2Img} alt="Image 3" />
                </div>
                <div className="slide">
                    <img src={laptopImg} alt="Image 4" />
                </div>
                <div className="slide">
                    <img src={sourceImg} alt="Image 5" />
                </div>
            </div>

            <div className="main-service">
                <h2 className="main-service__title">Main Service</h2>
                <h1 className="main-service__heading">바이러스를 분석하고 암호화하세요.</h1>
                <div className="main-service__content">
                    <div className="main-service__box">
                        <h3 className="main-service__subtitle">Virus Analyze</h3>
                        <h2 className="main-service__text">실행파일에 숨어있는<br />바이러스 및 멀웨어를 분석</h2>
                        <p>실행파일을 업로드하면 분석해서 파일구조를 보여드려요!</p>
                        <br />
                        <Link to="/virus-scan" className="main-service__a"><h2>Get Started!</h2></Link> {/* a 태그를 Link로 변환 */}
                    </div>
                    <div className="main-service__image">
                        <img src={malwarefoundImg} alt="Service Image 1" />
                    </div>
                    <div className="main-service__image">
                        <img src={lockerImg} alt="Service Image 2" />
                    </div>
                    <div className="main-service__box">
                        <h3 className="main-service__subtitle">Encryption</h3>
                        <h2 className="main-service__text">실행파일의 악의적인 변조를<br />막기위해 파일을 암호화</h2>
                        <p>실행파일을 암호화해서 악의적인 변조를 막으세요!</p>
                        <br />
                        <Link to="/packing" className="main-service__a"><h2>Get Started!</h2></Link> {/* a 태그를 Link로 변환 */}
                    </div>
                </div>
            </div>
        </>
    );
}

export default Main;
