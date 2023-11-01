import React, { useState } from 'react';
import axios from 'axios';

export default function ForgetPassword() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleForgetPassword = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/api/password-reset/', {
                email: email,
            });

            setMessage(`Please check your email for reset link.`);
        } catch (error) {

            setMessage('Password reset request failed');
        }
    };

    return (
        <div className="container py-5 mx-10">
            <form onSubmit={handleForgetPassword} className="bg-white shadow-md m-10 w-2/5 rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-2">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                        Email:
                    </label>
                    <div className="shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700">
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                </div>
                <button type="submit" className="text-white bg-green-500 px-5 py-2 my-5">
                    Reset Password
                </button>
                {message && <p className="text-green-500">{message}</p>}
            </form>
        </div>
    );
}
