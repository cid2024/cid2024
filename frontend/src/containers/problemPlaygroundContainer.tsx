import {Box, Button, Grid, TextField} from "@mui/material";
import {useState} from "react";
import {ProblemViewer} from "../components/problemViewer";
import {Problem} from "../types/problem";
import {getProblemById} from "../api/problem";

interface ProblemPlaygroundContainerProps {

}

export const ProblemPlaygroundContainer = ({

}: ProblemPlaygroundContainerProps) => {
    const [problemId, setProblemId] = useState<string>('')
    const [problem, setProblem] = useState<Problem | null>(null);

    const handleFetchProblem = async () => {
        const data = await getProblemById(problemId);
        setProblem(data);
    };

    const onFetchProblemButtonClick = () => {
        setProblem(null);
        handleFetchProblem();
    };

    return (
        <Box
            width={1}
        >
            <Grid
                container
                spacing={2}
            >
                <Grid
                    item
                    xs={8}
                >
                    <TextField
                        id="problem-id"
                        label="Problem ID"
                        value={problemId}
                        onChange={(e) => setProblemId(e.target.value)}
                        fullWidth
                    />
                </Grid>
                <Grid
                    item
                    xs={4}
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                    }}
                >
                    <Button
                        id="fetch-problem"
                        variant="contained"
                        color="primary"
                        onClick={onFetchProblemButtonClick}
                    >
                        View Problem
                    </Button>
                </Grid>
                {problem && (
                    <Grid
                        item
                        xs={12}
                    >
                        <ProblemViewer
                            problem={problem}
                            showSolution
                        />
                    </Grid>
                )}
            </Grid>
        </Box>
    )
}
