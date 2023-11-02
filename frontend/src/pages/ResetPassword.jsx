import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // Import useParams to access route parameters

export default function ResetPasswordPage() {
    const { encoded_pk, token } = useParams(); // Access route parameters

    const [validLink, setValidLink] = useState(false);
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [formErrors, setFormErrors] = useState({});
    const [message, setMessage] = useState('');

    useEffect(() => {
        // Check if the reset link is valid by making a request to the backend.
        axios
            .patch(`http://localhost:8000/api/password-reset/${encoded_pk}/${token}/`)
            .then(() => {
                setValidLink(true);
            })
            .catch(() => {
                setValidLink(false);
            });
    }, [encoded_pk, token]); // Use the route parameters in the dependency array

    const handleResetPassword = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            setFormErrors({ confirmPassword: 'Passwords do not match' });
            return;
        }

        try {
            // Send a PATCH request to reset the password
            await axios.patch(`http://localhost:8000/api/password-reset/${encoded_pk}/${token}/`, {
                new_password: newPassword,
                confirm_password: confirmPassword,
            });

            setMessage('Password has been successfully reset.'); // Display a success message
        } catch (error) {
            // Handle any errors, such as invalid token or server issues
            setMessage('Password reset failed.');
        }
    };

    return (
        <div className="container py-5">
            {validLink ? (
                <div>
                    <h1 className="text-2xl m-10">🔑 Reset Password</h1>
                    <form onSubmit={handleResetPassword} className="bg-white shadow-md m-10 w-2/5 rounded px-8 pt-6 pb-8 mb-4">
                        {/* Add CSRF token if necessary */}
                        <div className="mb-2">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="newPassword">
                                New Password:
                            </label>
                            <div className="shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700">
                                <input
                                    type="password"
                                    id="newPassword"
                                    name="newPassword"
                                    placeholder="Enter your new password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    required
                                />
                            </div>
                            {formErrors.newPassword && (
                                <div className="text-red-500 text-sm">{formErrors.newPassword}</div>
                            )}
                        </div>
                        <div className="mb-2">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="confirmPassword">
                                Confirm Password:
                            </label>
                            <div className="shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700">
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    placeholder="Confirm your password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                />
                            </div>
                            {formErrors.confirmPassword && (
                                <div className="text-red-500 text-sm">{formErrors.confirmPassword}</div>
                            )}
                        </div>
                        <button type="submit" className="text-white bg-green-500 px-5 py-2 my-5">
                            Submit
                        </button>
                        {message && <p className="text-green-500">{message}</p>}
                    </form>
                </div>
            ) : (
                <h2 className="text-2xl m-10 text-red-500">❌ Password reset link is invalid</h2>
            )}
        </div>
    );
}
