import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function ProfilePage() {
    const [userData, setUserData] = useState({});
    const [profilePhoto, setProfilePhoto] = useState('');
    const [modalVisible, setModalVisible] = useState(false);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const accessToken = localStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:8000/api/profile/', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });

                const { user_data, data } = response.data;
                setUserData(user_data);
                setProfilePhoto(data.photo);
            } catch (error) {
                console.error('Failed to fetch user profile data', error);
            }
        };

        fetchUserProfile();
    }, []);

    const showModal = () => {
        setModalVisible(true);
    };

    const closeModal = () => {
        setModalVisible(false);
    };

    return (
        <div className="flex flex-col items-center mt-10">
            <div className="rounded-full h-40 w-40 overflow-hidden bg-gray-300 cursor-pointer" onClick={showModal}>
                <img className="h-full w-full object-cover" src={profilePhoto} alt="Profile Photo" />
            </div>
            <a href="/edit" className="mt-2 text-blue-600">Edit Profile</a>
            <div>
                <h1 className="text-2xl mt-4">{userData.first_name} {userData.last_name}</h1>
            </div>
            <h2 className="text-lg text-gray-600">Username: {userData.username}</h2>
            <p className="text-gray-600">Email: {userData.email}</p>

        </div>


    );
}
