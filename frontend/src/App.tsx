import React from 'react';
import { Button, Container, Typography } from '@mui/material';
import {ProblemViewer} from "./components/problemViewer";
import {ProblemPlaygroundContainer} from "./containers/problemPlaygroundContainer";

function App() {
    return (
        <Container
            sx={{
                marginTop: 4,
                marginBottom: 4,
                marginLeft: 2,
                marginRight: 2,
            }}
        >
            <ProblemPlaygroundContainer />
        </Container>
    );
}

export default App;
