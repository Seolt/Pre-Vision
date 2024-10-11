import { MongoClient, GridFSBucket } from 'mongodb'; // MongoDB 클라이언트와 GridFSBucket 모듈을 가져옴
import crypto from 'crypto'; // 파일의 MD5 해시를 계산하기 위해 crypto 모듈을 가져옴
import multer from 'multer'; // 파일 업로드를 처리하기 위한 multer 모듈을 가져옴
import dotenv from 'dotenv'; // 환경 변수를 로드하기 위한 dotenv 모듈을 가져옴

dotenv.config(); // .env 파일에 저장된 환경 변수를 로드

// MongoDB 연결 정보 (환경 변수로부터 MongoDB URI를 로드)
const MONGO_URI = process.env.MONGO_URI; // MongoDB URI를 환경 변수에서 가져옴
const DB_NAME = 'vsapi'; // MongoDB에서 사용할 데이터베이스 이름
const FILES_COLLECTION = 'file'; // 파일 메타데이터가 저장될 컬렉션 이름

let db; // MongoDB 데이터베이스 연결을 위한 변수

// Multer 설정: 메모리에서 파일을 처리하는 미들웨어
const scanUpload = multer(); // Multer는 파일을 메모리 내에서 처리함

// MongoDB 연결 함수: 서버 시작 시 데이터베이스 연결을 설정하는 함수
const connectToMongoDB = async () => {
    try {
        // MongoDB에 연결 (MONGO_URI를 사용)
        const client = await MongoClient.connect(MONGO_URI);
        db = client.db(DB_NAME); // 데이터베이스 객체를 설정
        console.log('uploadFileScan.js Connected to MongoDB'); // 연결 성공 메시지 출력
    } catch (error) {
        // 연결 실패 시 오류 메시지 출력
        console.error('MongoDB Connection Error:', error);
    }
};

// MD5 해시 계산 함수: 파일 데이터에 대해 MD5 해시값을 계산
const calculateMd5 = (fileBuffer) => {
    return crypto.createHash('md5').update(fileBuffer).digest('hex'); // 파일 버퍼 데이터를 MD5 해시로 변환
};

// Signature ID 생성 함수: 고유한 signature_id를 생성 (오늘 날짜 기반)
const generateSignatureId = async () => {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, ''); // 현재 날짜를 YYYYMMDD 형식으로 변환
    const collection = db.collection(FILES_COLLECTION); // 'file' 컬렉션을 선택

    // 오늘 날짜로 시작하는 signature_id의 개수를 세서 다음 번호를 생성
    const count = await collection.countDocuments({
        signature_id: { $regex: `^${today}-` }, // 오늘 날짜로 시작하는 signature_id를 찾음
    });
    const nextId = count + 1; // 다음 ID 번호를 결정
    return `${today}-${nextId.toString().padStart(3, '0')}`; // YYYYMMDD-001 형식으로 signature_id 생성
};

// 지연 함수
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 파일 업로드를 처리하는 함수: 사용자가 업로드한 파일을 MongoDB GridFS에 저장하는 함수
const scanUploadFile = async (req, res) => {
    try {
        const fileBuffer = req.file.buffer; // multer를 통해 업로드된 파일의 데이터를 메모리에서 가져옴
        const filename = req.file.originalname; // 업로드된 파일의 원본 파일명을 가져옴
        const uploadIp = req.ip; // 파일을 업로드한 사용자의 IP 주소를 가져옴

        // 파일의 MD5 해시값을 계산하여 무결성을 확인
        const filehash = calculateMd5(fileBuffer);

        let signature_id;

        // GridFS에 파일을 저장: MongoDB의 GridFS를 사용하여 파일을 저장
        const bucket = new GridFSBucket(db); // GridFSBucket 객체 생성

        const uploadStream = bucket.openUploadStream(filename); // 파일을 GridFS에 업로드할 스트림을 엶
        
        // 기존에 동일한 파일이 있는지 확인
        const existingFile = await db.collection(FILES_COLLECTION).findOne({ filehash: filehash });

        if (existingFile) {
            console.log('Existing file found with the same hash. Deleting old file...');

            // 기존 파일이 있으면 그 파일의 signature_id를 재사용
            signature_id = existingFile.signature_id;

            // 기존 파일 삭제 (메타데이터와 GridFS 파일 모두 삭제)
            await db.collection(FILES_COLLECTION).deleteOne({ _id: existingFile._id }); // 메타데이터 삭제
            await bucket.delete(existingFile.gridfs_file_id); // GridFS 파일 삭제

            console.log('Old file deleted successfully.');
        } else {
            // 기존 파일이 없으면 새로운 signature_id 생성
            signature_id = await generateSignatureId();
        }

        // 파일 데이터를 업로드하는 비동기 작업을 기다림
        await new Promise((resolve, reject) => {
            uploadStream.end(fileBuffer); // 업로드 스트림에 파일 데이터를 쓰고 끝냄
            uploadStream.on('finish', resolve); // 업로드가 끝나면 resolve 호출
            uploadStream.on('error', reject); // 업로드 중 에러가 발생하면 reject 호출
        });

        console.log('File uploaded successfully to GridFS');

        // 현재 UTC시간을 가져옴
        const now = new Date();
        now.setHours(now.getHours() + 9); // 9시간을 더해 KST(한국 표준시)로 변환

        // 업로드가 완료되면 파일 메타데이터를 MongoDB 컬렉션에 저장
        const fileMetadata = {
            signature_id: signature_id, // 고유한 signature_id
            filehash: filehash, // 파일의 MD5 해시값
            filename: filename, // 업로드된 파일의 이름
            gridfs_file_id: uploadStream.id, // GridFS에 저장된 파일의 ID
            upload_time: now, // 업로드 시간
            upload_ip: uploadIp, // 파일을 업로드한 사용자의 IP 주소
        };

        await db.collection(FILES_COLLECTION).insertOne(fileMetadata); // 파일 메타데이터를 'file' 컬렉션에 삽입

        // 2초 지연을 추가
        await delay(2000);

        // info 컬렉션에서 업로드된 파일의 MD5 해시값과 일치하는 문서를 찾음
        const infoCollection = db.collection('info'); // 'info' 컬렉션 선택
        const infoDocuments = await infoCollection.find({ md5: filehash }).toArray(); // MD5 값이 일치하는 문서들을 찾음

        // 성공적인 응답을 클라이언트에 반환 (일치하는 문서와 함께)
        res.json({
            filename: `${filename}`, // 성공 메시지
            infoDocuments: infoDocuments, // 일치하는 문서들 반환
        });
    } catch (error) {
        // 파일 처리 중에 발생한 에러를 처리
        console.error('Error processing file upload:', error.message);
        console.error(error.stack); // 에러 스택을 출력하여 상세 정보를 확인
        res.status(500).json({ error: 'Error processing file upload', details: error.message });
    }
};

connectToMongoDB(); // 서버가 시작되면 MongoDB에 연결

// 다른 모듈에서 사용할 수 있도록 Multer와 업로드 처리 함수를 내보냄
export { scanUpload, scanUploadFile };
