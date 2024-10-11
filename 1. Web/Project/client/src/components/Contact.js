import React from 'react';
import axios from 'axios';
import '../css/Contact.css';
import { useState } from 'react';

function Contact() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // axios로 POST 요청을 보내기
            const response = await axios.post('/send-email', formData);
            if (response.data.success) {
                alert('문의 사항이 성공적으로 전송되었습니다.');
            } else {
                alert('문의 사항 전송에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('문의 사항 전송 중 오류가 발생했습니다.');
        }
    };

    return (
        <div className="container">
            <div className="contact">
                <h1>Contact us</h1>
                <p>Contact the administrator if you have any questions.</p>
                <span>(It takes 1-2 business days.)</span>

                <form className="contact-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        placeholder="이름을 입력하세요"
                        value={formData.name}
                        onChange={handleChange}
                        required
                    />

                    <label htmlFor="email">E-mail</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="이메일을 입력하세요"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />

                    <label htmlFor="message">Message</label>
                    <textarea
                        id="message"
                        name="message"
                        rows="6"
                        placeholder="문의 내용을 입력하세요"
                        value={formData.message}
                        onChange={handleChange}
                        required
                    ></textarea>

                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default Contact;
