import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { loginUser } from '../redux/userSlice'; // Redux action
import { useNavigate } from 'react-router-dom'; // For redirect after login
import {
    Avatar,
    Button,
    CssBaseline,
    TextField,
    FormControlLabel,
    Checkbox,
    Link,
    Grid,
    Box,
    Typography,
    Container
} from '@mui/material'; // Or your UI library's components
import LockOutlinedIcon from '@mui/icons-material/LockOutlined'; // Example icon


function Copyright(props) {
    return (
      <Typography variant="body2" color="text.secondary" align="center" {...props}>
        {'Copyright © '}
        <Link color="inherit" href="https://mui.com/">
          Your Website
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }



const Login = ({ onLogin }) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [error, setError] = useState(null); // Add error state


    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);  // Clear any previous errors
        try {
          const userData = await dispatch(loginUser(formData)).unwrap(); //Handle potential rejections with unwrap.

          onLogin(userData);  // Call onLogin prop with user data
          navigate('/profile'); // Or wherever you want to redirect after login
        } catch (err) {
          console.error("Login failed:", err);
          setError(err.message);  // Set the error message
          //Optionally, show error message to user:  alert(err.message);
        }


    };


    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });  //Controlled component handling.
    };




    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xs"> {/*For centering */}
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}> {/*Optional icon/avatar.  */}
                        <LockOutlinedIcon />  {/*Replace or modify if necessary.  */}

                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>


                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>

                        <TextField  //Email field.
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            value={formData.email}
                            onChange={handleChange}

                        />
                        <TextField //Password field.
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={formData.password}
                            onChange={handleChange}

                        />
                        <FormControlLabel //Remember me checkbox.
                            control={<Checkbox value="remember" color="primary" />}
                            label="Remember me"
                        />
                        {error && <Typography color="error">{error}</Typography>} {/*Error message display.  */}


                        <Button //Login button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign In
                        </Button>
                        <Grid container> {/*Optional links for signup/forgot password.  Modify as needed for your app.  */}

                            <Grid item xs>
                                <Link href="#" variant="body2">
                                    Forgot password?
                                </Link>

                            </Grid>

                            <Grid item>
                                <Link href="#" variant="body2">
                                    {"Don't have an account? Sign Up"}
                                </Link>
                            </Grid>

                        </Grid>

                    </Box>
                </Box>
                <Copyright sx={{ mt: 8, mb: 4 }} /> {/*Optional.  */}

            </Container>

        </ThemeProvider>


    );

};



export default Login;