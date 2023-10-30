import React, { useEffect } from 'react';
import axios from 'axios';

export default function LogoutPage() {
    useEffect(() => {
        const logout = async () => {
            try {
                const refresh_token = localStorage.getItem('refresh');

                await axios.post('http://127.0.0.1:8000/api/logout/', { refresh_token });

                localStorage.removeItem('refresh');

            } catch (error) {
                console.error('Logout failed', error);
            }
        };
        logout();
    }, []);

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-2xl mb-6">You have been logged out</h1>
            <a href="/login" className="text-indigo-500 underline">Click here to log in</a>
        </div>
    );
}