import { MongoClient, GridFSBucket, ObjectId } from 'mongodb'; // MongoDB 클라이언트와 GridFSBucket 모듈을 가져옴
import fs from 'fs'; // 파일 시스템 모듈
import os from 'os'; // 임시 디렉토리 경로 사용
import path from 'path'; // 경로 설정 관련 모듈
import AdmZip from 'adm-zip'; // 압축 모듈
import dotenv from 'dotenv'; // 환경 변수 설정
dotenv.config(); // 환경 변수 로드

// MongoDB 연결 정보
const MONGO_URI = process.env.MONGO_URI;
let encryptedDb; // MongoDB 연결을 위한 변수

// MongoDB 연결 함수
const connectToMongoDB = async () => {
    try {
        const client = await MongoClient.connect(MONGO_URI);
        encryptedDb = client.db('encrypted_files'); // 'encrypted_files' DB 사용
        console.log('downloadFile.js Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB Connection Error:', error);
    }
};

// GridFS에서 파일을 다운로드하는 함수
const downloadEncryptedFile = async (req, res) => {
    const fileId = req.params.fileId; // 클라이언트에서 넘어온 파일 ID

    try {
        const bucket = new GridFSBucket(encryptedDb); // GridFSBucket 객체 생성
        
        // 여기서 ObjectId 생성 시 new 키워드를 추가
        const downloadStream = bucket.openDownloadStream(new ObjectId(`${fileId}`)); // 해당 파일을 가져오는 스트림

        // 응답 헤더 설정: 다운로드할 파일의 MIME 타입과 이름 설정
        res.set({
            'Content-Type': 'application/octet-stream', // 기본 바이너리 파일로 설정
            'Content-Disposition': `attachment; filename="${fileId}"`, // 파일명 설정
        });

        // 파일 데이터를 클라이언트로 바로 전송
        downloadStream.pipe(res);

        // 파일을 찾을 수 없을 때
        downloadStream.on('error', (err) => {
            console.error('File not found:', err);
            res.status(500).send('File not found');
        });

        // 다운로드 완료 후
        downloadStream.on('end', () => {
            console.log(`File ${fileId} successfully downloaded.`);
        });

    } catch (error) {
        console.error('Failed to download file:', error);
        res.status(500).json({ error: 'Failed to download file' });
    }
};

// MongoDB 연결 호출
connectToMongoDB();

// export를 통해 다른 모듈에서 이 함수 사용 가능하게 함
export { downloadEncryptedFile };
