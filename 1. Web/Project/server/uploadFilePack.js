import { MongoClient, GridFSBucket } from 'mongodb'; // MongoDB 클라이언트와 GridFSBucket 모듈을 가져옴
import multer from 'multer'; // 파일 업로드 처리 모듈
import dotenv from 'dotenv'; // 환경 변수 로드를 위한 dotenv 모듈

dotenv.config(); // 환경 변수 로드

// MongoDB 연결 정보
const MONGO_URI = process.env.MONGO_URI; // .env 파일에서 MongoDB URI 로드
const FILES_COLLECTION = 'filedata'; // 파일 메타데이터가 저장될 컬렉션 이름
const PE_INFO_COLLECTION = 'pe_info'; // pe_info 컬렉션

let db, encryptedDb; // MongoDB 연결을 위한 변수

// Multer 설정: 메모리에서 파일을 처리하는 미들웨어
const packUpload = multer(); // Multer는 파일을 메모리 내에서 처리함

// MongoDB 연결 함수: 서버 시작 시 데이터베이스 연결 설정
const connectToMongoDB = async () => {
    try {
        const client = await MongoClient.connect(MONGO_URI);
        db = client.db('normal_files'); // normal_files DB
        encryptedDb = client.db('encrypted_files'); // encrypted_files DB
        console.log('uploadFilePack.js Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB Connection Error:', error);
    }
};

// signature_id 생성 함수: 고유한 signature_id를 생성 (오늘 날짜 기반)
const generateSignatureId = async () => {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD 형식
    const collection = db.collection(FILES_COLLECTION); // 'filedata' 컬렉션 선택

    // 오늘 날짜로 시작하는 signature_id의 개수를 확인하여 번호 매김
    const count = await collection.countDocuments({
        signature_id: { $regex: `^${today}-` }
    });
    const nextId = count + 1;

    // signature_id를 YYYYMMDD-001 형식으로 생성
    return `${today}-${nextId.toString().padStart(3, '0')}`;
};

// encrypted_Files의 filedata, pe_info 에서 signature_id를 기준으로 데이터를 조회하는 함수
const fetchMatchingFiledata = async (signature_id) => {
    const encryptedFileInfo = await encryptedDb.collection(PE_INFO_COLLECTION).find({ signature_id }).toArray();
    // encrypted_files에서 filedata 조회
    const encryptedFilesData = await encryptedDb.collection(FILES_COLLECTION).find({ signature_id }).toArray();

    return {
        encryptedFilesData,
        encryptedFileInfo,
    };
};

// 암호화된 파일이 저장되었는지 확인하는 함수
const checkEncryptedFileUpload = async (signature_id, res, filename) => {
    try {
        const maxRetries = 600; // 최대 600번(600초) 재시도
        let retries = 0;

        const checkIfFileExists = async () => {
            const encryptedFilesInfo = await encryptedDb.collection(PE_INFO_COLLECTION).find({ signature_id }).toArray();

            if (encryptedFilesInfo.length > 0) {
                // pe_info에서 해당 signature_id에 해당하는 데이터 가져오기
                const peInfo = await fetchMatchingFiledata(signature_id);

                // 클라이언트에 성공 응답 반환
                res.json({
                    message: 'File uploaded successfully',
                    filename: filename,
                    peInfo, // 조회된 pe_info 데이터
                });
            } else if (retries < maxRetries) {
                // 파일이 아직 저장되지 않았으면 재시도
                retries++;
                console.log(`Retry ${retries}: Checking if file is uploaded...`);
                setTimeout(checkIfFileExists, 1000); // 1초 후 다시 체크
            } else {
                // 최대 재시도 횟수 초과
                res.status(500).json({ message: 'File upload failed or timeout' });
            }
        };

        checkIfFileExists(); // 파일 확인 시작

    } catch (error) {
        console.error('Error checking encrypted file upload:', error);
        res.status(500).json({ error: 'Error checking encrypted file upload', details: error.message });
    }
}

// 파일 업로드를 처리하는 함수: 사용자가 업로드한 파일을 MongoDB GridFS에 저장하는 함수
const packUploadFile = async (req, res) => {
    try {
        const fileBuffer = req.file.buffer; // 업로드된 파일의 데이터를 가져옴
        const filename = req.file.originalname; // 파일의 이름을 가져옴
        const uploadIp = req.ip; // 사용자의 IP 주소를 가져옴

        // signature_id 생성
        const signature_id = await generateSignatureId();

        // GridFS에 파일 저장
        const bucket = new GridFSBucket(db);
        const uploadStream = bucket.openUploadStream(filename);

        // 파일 업로드를 처리하는 비동기 작업
        await new Promise((resolve, reject) => {
            uploadStream.end(fileBuffer); // 파일 데이터를 스트림에 기록하고 업로드 종료
            uploadStream.on('finish', () => {
                console.log('File uploaded to normal_files successfully.');
                resolve(); // 업로드 완료
            });
            uploadStream.on('error', reject); // 오류 발생 시 reject 호출
        });

        console.log('File uploaded successfully to GridFS');

        // 현재 시간(UTC)을 KST로 변환
        const now = new Date();
        now.setHours(now.getHours() + 9); // 한국 시간 기준

        // 파일의 메타데이터 저장
        const fileMetadata = {
            signature_id: signature_id, // 고유한 signature_id
            filename: filename, // 업로드된 파일의 이름
            file_extension: `.${filename.split('.').pop()}`, // 파일 확장자
            gridfs_file_id: uploadStream.id, // GridFS에서 저장된 파일 ID
            upload_time: now, // 업로드 시간
            upload_ip: uploadIp // 파일을 업로드한 사용자의 IP 주소
        };

        // 메타데이터를 'filedata' 컬렉션에 삽입
        await db.collection(FILES_COLLECTION).insertOne(fileMetadata);

        // 암호화된 파일이 저장되었는지 확인
        await checkEncryptedFileUpload(signature_id, res, filename); // encrypted_files에 파일 저장 확인

    } catch (error) {
        console.error('Error processing file upload:', error);
        res.status(500).json({ error: 'Error processing file upload', details: error.message });
    }
};

// MongoDB 연결
connectToMongoDB();

// 다른 모듈에서 사용할 수 있도록 Multer와 업로드 처리 함수를 내보냄
export { packUpload, packUploadFile };