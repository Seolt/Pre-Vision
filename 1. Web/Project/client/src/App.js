import './css/App.css';
import { Route, Routes } from 'react-router-dom';
import { Link } from 'react-router-dom'; // React Router의 Link 컴포넌트 임포트
import Main from './components/Main.js';
import Contact from './components/Contact.js';
import Donation from './components/Donation.js';
import Packing from './components/Packing.js';
import VirusScan from './components/VirusScan.js';
import UserGuide from './components/UserGuide.js';
import TermsOfUse from './components/TermsOfUse.js';
import PrivacyPolicy from './components/PrivacyPolicy.js';
import PreVision from './images/Pre-Vision.png';
function App() {
  return (
    <>
      {/* 네비게이션 바 */}
      <div className="nav">
        <Link className="nav__logo" to="/"><img className="nav__logo__img" src={PreVision} alt="TeamLogo" /></Link>
        <div className="nav__right">
          <Link to="/user-guide" className="nav__right__a"><h2>User Guide </h2></Link>
          <Link to="/virus-scan" className="nav__right__a"><h2>Virus Scan </h2></Link>
          <Link to="/packing" className="nav__right__a"><h2>Packing</h2></Link>
        </div>
      </div>

      {/* 각 페이지 컴포넌트화 */}
      <div className="content">
        <Routes>
          <Route path="/" element={<Main/>} />
          <Route path="/contact" element={<Contact/>} />
          <Route path="/donation" element={<Donation/>} />
          <Route path="/Packing" element={<Packing/>} />
          <Route path="/virus-scan" element={<VirusScan/>} />
          <Route path="/user-guide" element={<UserGuide/>} /> 
          <Route path="/terms" element={<TermsOfUse/>} />
          <Route path="/privacy" element={<PrivacyPolicy/>} />
        </Routes>
      </div>

      {/* 푸터 */}
      <footer className="footer">
        <div className="footer__nav">
          <a href="https://github.com/" className="footer__link" target="_blank" rel="noopener noreferrer">Team Github</a> {/* 외부 링크는 a 태그 유지 */}
          <Link to="/contact" className="footer__link">Contact Us</Link>
          <Link to="/donation" className="footer__link">Donation</Link>
        </div>
        <div className="footer__legal">
          <p><Link to="/terms">Terms of Use</Link> | <Link to="/privacy">Privacy Policy</Link></p>
          <p>&copy; Copyright 2024. All Rights Reserved. Hosted by Pre-Vision</p>
        </div>
      </footer>
    </>
  );
}

export default App;
