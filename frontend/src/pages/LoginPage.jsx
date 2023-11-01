import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function LoginPage() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleLogin = () => {
        axios
            .post('http://127.0.0.1:8000/api/login/', formData)
            .then((response) => {
                localStorage.setItem('token', response.data.access);
                window.location.href = '/home';
            })
            .catch((error) => {
                console.error('Login failed', error);
            });
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded shadow-lg">
                <h1 className="text-2xl mb-6">🧔 Login User</h1>
                <form>
                    <div className="mb-4">
                        <label
                            className="block text-gray-700 text-sm font-bold mb-2"
                            htmlFor="username"
                        >
                            Username
                        </label>
                        <input
                            className="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            id="username"
                            type="text"
                            name="username"
                            placeholder="Username"
                            onChange={handleChange}
                        />
                    </div>
                    <div className="mb-6">
                        <label
                            className="block text-gray-700 text-sm font-bold mb-2"
                            htmlFor="password"
                        >
                            Password
                        </label>
                        <input
                            className="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            id="password"
                            type="password"
                            name="password"
                            placeholder="Password"
                            onChange={handleChange}
                        />
                    </div>

                    <div className="text-center mb-4">
                        <Link
                            to="/forget-password"
                            className="text-blue-500 hover:text-blue-700 font-bold"
                        >
                            Forget Password?
                        </Link>
                    </div>

                    <div className="flex items-center justify-center">
                        <button
                            type="button"
                            onClick={handleLogin}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        >
                            Log In
                        </button>
                        <Link
                            to="/register"
                            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ml-2"
                        >
                            Sign Up
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
}
