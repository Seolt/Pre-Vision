import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import sendMail from './sendMail.js';
import { scanUpload, scanUploadFile } from './uploadFileScan.js';
import { packUpload, packUploadFile } from './uploadFilePack.js';
import { downloadEncryptedFile } from './downloadFile.js';
// 환경 변수 설정을 위한 dotenv.config() 호출
dotenv.config();

const app = express();

// const corsOptions = {
//     origin: 'http://localhost:3000', // React 주소 (포트 3000)
//     methods: ['GET', 'POST'], // 허용할 HTTP 메서드
// };

// CORS 옵션을 적용
app.use(cors());

// JSON 형식의 데이터 처리
app.use(express.json());

// 이메일 전송을 위한 POST 요청
app.post('/send-email', sendMail);

// 파일 업로드를 위한 POST 요청(VirusScan)
app.post('/upload-file-scan', scanUpload.single('file'), scanUploadFile);

// 파일 업로드를 위한 POST 요청(Packing)
app.post('/upload-file-pack', packUpload.single('file'), packUploadFile);

// 파일 다운로드를 위한 GET 요청(Packing)
app.get('/download-file/:fileId', (req, res) => {
    console.log(`Received download request for file ID: ${req.params.fileId}`);
    downloadEncryptedFile(req, res);
});

// 서버 실행
app.listen(5000, () => {
    console.log('서버가 5000번 포트에서 실행 중입니다.');
});


