import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import '../css/Donation.css';

function Donation() {
    const [startDate, setStartDate] = useState(null);
    
    return (
        <div className="container">
            <div className="container__head">
                <h1>Donation</h1>
                <p>Your support helps create a better world.</p>
            </div>

            <div className="container__main">
                <section className="bank-details">
                    <h2>Donation account</h2>
                    <p className='bank-details__p'>Bank :
                        <span className='bank-details__p2'>&nbsp;KakaoBank</span>
                    </p>
                    <p className='bank-details__p'>Account number :
                        <span className='bank-details__p2'>&nbsp;3333-03-9932704</span>
                    </p>
                    <p className='bank-details__p'>Account holder :
                        <span className='bank-details__p2'>&nbsp;Kimsunwoo</span>
                    </p>
                </section>

                <section className="donation-confirmation">
                    <h2>Donation confirmation</h2>
                    <form className="donation-form">
                        <label htmlFor="name">Name</label>
                        <input type="text" id="name" name="name" placeholder="Please enter your name" required />

                        <label htmlFor="email">E-mail</label>
                        <input type="email" id="email" name="email" placeholder="Please enter your email" required />

                        <label htmlFor="transfer-amount">Donation amount</label>
                        <input type="number" id="transfer-amount" name="transfer-amount" placeholder="Please enter the donation amount" step="10000" required />

                        <label htmlFor="transfer-date">Donation date</label>
                        <DatePicker
                            className='datePicker'
                            selected={startDate}
                            onChange={(date) => setStartDate(date)}
                            dateFormat="yyyy-MM-dd" // 날짜 형식을 영어로 표시
                            placeholderText="Please enter the donation date"
                            required
                        />

                        <button type="submit">submit</button>
                    </form>
                </section>
            </div>

            <div className="container__foot">
                <br />
                <p>&copy; 2024 Pre-Vision</p>
            </div>
        </div>
    );
}

export default Donation;
