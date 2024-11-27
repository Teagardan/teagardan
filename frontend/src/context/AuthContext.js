import React, { createContext, useState, useEffect, useContext } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser, logoutUser, selectUser } from '../redux/userSlice'; // Redux integration
import jwtDecode from 'jwt-decode'; // For JWT decoding (if using JWTs)
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const dispatch = useDispatch();
    const user = useSelector(selectUser); //Use selector to access user from Redux store.
    const [authStatus, setAuthStatus] = useState('pending'); // 'pending', 'logged in', 'logged out'.
    const [error, setError] = useState(null); //Error state for login.

    useEffect(() => { //Check local storage or Redux for existing token on mount.
        const storedToken = localStorage.getItem('token'); //Or wherever you're storing it.
        if (storedToken) {
            try {
                const decodedToken = jwtDecode(storedToken); //Decode if JWT
                // Verify token expiry (if applicable) and other checks
                dispatch(loginUser({ token: storedToken, ...decodedToken })); //Or appropriate data
                setAuthStatus('logged in'); //If they're logged in, then their auth status is 'logged in'.


            } catch (err) {
                console.error('Invalid or expired token:', err);
                localStorage.removeItem('token'); //Remove invalid token.
                setAuthStatus('logged out'); //If the token is not valid, then their status is 'logged out'.

            }
        } else {

            setAuthStatus('logged out');  //Initial state
        }
    }, [dispatch]);




    const login = async ({ email, password }) => { //Use async/await
        try {

            setAuthStatus('pending');
            const response = await dispatch(loginUser({ email, password })).unwrap(); // Handle potential rejections

            const token = response.token; //Get token from response
            localStorage.setItem('token', token); //Store the token
            setAuthStatus('logged in'); //Update auth status.  This should trigger UI changes throughout the app.
            return response;
        } catch (err) {
            console.error('Login failed:', err);
            setAuthStatus('logged out');
            setError(err.message); //Set error state for display in UI
            throw err; //Re-throw the error to be handled by Login component

        }

    };



    const logout = () => {
        localStorage.removeItem('token');
        dispatch(logoutUser()); //Dispatch logout action
        setAuthStatus('logged out');
        navigate('/login'); //Redirect to login page after logout
    };


    const contextValue = {  //Context value to be used in components throughout the app.
        user,
        authStatus,
        error,        
        login,
        logout
    };



    return (
        <AuthContext.Provider value={contextValue}>
            {authStatus === 'pending' ? (  //Conditional rendering to handle cases where app state or context is not set.
                <Typography variant="body1">Loading...</Typography> //Or a loading spinner component
            ) : (

                children  // Render children when auth status is resolved (avoids rendering issues if the store or context isn't initialized)
            )}
        </AuthContext.Provider>
    );
};



export const useAuth = () => {  //Custom hook for easier access to context throughout the application.
    return useContext(AuthContext);  //Use this in any component that needs to access auth state or login/logout functions.
};