import React, { useState } from 'react';
import {
    Button,
    CircularProgress,
    Container,
    CssBaseline,
    Box,
    Typography,
    Paper,
    Input,
    InputLabel,
    InputAdornment,
    IconButton,
} from '@mui/material';
import { styled } from '@mui/system';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const StyledContainer = styled(Container)({
    background: "aliceblue",
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: "center"
});

const StyledPaper = styled(Paper)({
    padding: '32px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
});

const StyledButton = styled(Button)({
    marginTop: '16px',
});

const Page = () => {
    const [base64String, setBase64String] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const convertToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const res = reader.result;
                resolve(res);
            };

            reader.readAsDataURL(file);
        });
    };

    const handleFileChange = async (event) => {
        const selectedFile = event.target.files[0];
        const base64 = await convertToBase64(selectedFile);
        const formattedString = base64.replace('data:image/png;base64,', '');
        setBase64String(formattedString);
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    image: base64String
                }),
            });

            const data = await response.json();

            setResult(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleBack = () => {
        setBase64String('');
        setLoading(false);
        setResult(null);
    };

    return (
        <StyledContainer component="main" maxWidth="100%">
            <CssBaseline />
            <StyledPaper elevation={3}>
                <Typography component="h1" variant="h5" gutterBottom>
                    {result ? 'Результат' : 'Завантажте картинку'}
                </Typography>
                {result ? (
                    <div>
                        {
                            Object.entries(result).map(([key, value]) => (
                                <Typography>{key}: {value}</Typography>
                            ))
                        }
                        <StyledButton
                            type="button"
                            fullWidth
                            variant="contained"
                            color="primary"
                            onClick={handleBack}
                            disabled={loading}
                        >
                            Повернутися назад
                        </StyledButton>
                    </div>
                ) : (
                    <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column">
                        <InputLabel htmlFor="file-input" style={{ marginBottom: '8px' }}>
                            Оберіть файл
                        </InputLabel>
                        <Input
                            id="file-input"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            endAdornment={
                                <InputAdornment position="end">
                                    <IconButton component="span">
                                        <CloudUploadIcon />
                                    </IconButton>
                                </InputAdornment>
                            }
                        />
                        <StyledButton
                            type="button"
                            fullWidth
                            variant="contained"
                            color="primary"
                            onClick={handleSubmit}
                            disabled={loading}
                        >
                            Відправити
                        </StyledButton>
                    </Box>
                )}
                {loading && <CircularProgress style={{ margin: '16px 0' }} />}
            </StyledPaper>
        </StyledContainer>
    );
};

export default Page;
