import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/';

function RegisterPage() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        firstName: '',
        lastName: '',
        password1: '',
        password2: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const registrationData = {
            username: formData.username,
            email: formData.email,
            first_name: formData.firstName,
            last_name: formData.lastName,
            password1: formData.password1,
            password2: formData.password2,
        };

        axios
            .post(`${API_URL}api/register/`, registrationData)
            .then((response) => {
                // Handle successful registration
                console.log('Registration successful:', response.data);

            })
            .catch((error) => {
                // Handle registration error
                console.error('Registration error:', error);


                if (error.response) {
                    // Response status code (e.g., 400, 404, 500)
                    console.log('Status:', error.response.status);


                    console.log('Error response data:', error.response.data);
                } else {
                    // Network error or no response from the server
                    console.error('Network error:', error.message);
                }
            });
    };


    return (

        <div className="min-h-screen flex items-center justify-center">
            <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
                <h1 class="text-2xl m-10">🧔 Register User</h1>
                <div className="mb-2">
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        value={formData.username}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3 mr-10"
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3"
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="text"
                        name="firstName"
                        placeholder="First Name"
                        value={formData.firstName}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3"
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="text"
                        name="lastName"
                        placeholder="Last Name"
                        value={formData.lastName}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3"
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="password"
                        name="password1"
                        placeholder="Password"
                        value={formData.password1}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3"
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="password"
                        name="password2"
                        placeholder="Confirm Password"
                        value={formData.password2}
                        onChange={handleChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3"
                    />
                </div>
                <div className="mb-6">
                    <button
                        type="submit"
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Register
                    </button>
                </div>
                <div className="text-center">
                    <p>Already have an account? <Link to="/login" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</Link></p>
                </div>
            </form>
        </div>
    );
}

export default RegisterPage;
