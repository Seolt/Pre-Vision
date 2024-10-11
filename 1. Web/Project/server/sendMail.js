import nodemailer from 'nodemailer';

async function sendMail(req, res) {
    // 클라이언트로부터 전달된 요청(body)에서 name, email, message 데이터를 추출
    const { name, email, message } = req.body;

    // Nodemailer 설정 - 네이버
    let transporter = nodemailer.createTransport({
        host: 'smtp.naver.com', // 네이버 SMTP 서버
        port: 587, // 네이버 SMTP 포트
        secure: false, // true는 SSL사용 false는 TLS사용
        auth: {
            user: process.env.EMAIL_USER, // 네이버 이메일 계정
            pass: process.env.EMAIL_PASS, // 네이버 이메일 비밀번호
        },
    });

    // 이메일 옵션 설정
    let mailOptions = {
        from: process.env.EMAIL_USER, // 네이버 SMTP 서버 제한때문에 발신자, 수신자 동일하게 함.
        to: process.env.EMAIL_USER, // 네이버 이메일로 수신
        subject: `문의사항: ${email}`, // 제목
        text: `${name} 님의 문의 내용:\n\n${message}\n\n\n\n\n\n발신자 이메일: ${email}`, // 내용과 발신자 이메일
        replyTo: email, // 답장 시 사용할 이메일
    };

    // try-catch를 사용해 이메일 전송 시도
    try {
        // 이메일을 async(비동기)로 전송하고, 전송 완료 시까지 기다림
        await transporter.sendMail(mailOptions);
        // 이메일이 성공적으로 전송되면 클라이언트에게 성공 응답을 보냄
        res.json({ success: true });
    } catch (error) {
        // 이메일 전송에 실패하면 오류 로그를 출력하고 실패 응답을 보냄
        console.error('이메일 전송 오류:', error);
        res.json({ success: false });
    }
} 

export default sendMail;