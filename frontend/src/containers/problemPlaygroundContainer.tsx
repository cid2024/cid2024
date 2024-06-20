import {Box, Button, Grid, Stack, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {ProblemViewer} from "../components/problemViewer";
import {Problem} from "../types/problem";
import {getProblemRecommendation, patchSolvingHistory} from "../api/recommendation";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';

interface ProblemPlaygroundContainerProps {

}

export const ProblemPlaygroundContainer = ({

}: ProblemPlaygroundContainerProps) => {
    const [isOpenSolution, setIsOpenSolution] = useState<boolean>(false)
    const [answer, setAnswer] = useState<string>('')
    const [problem, setProblem] = useState<Problem | null>(null)
    const [similarity, setSimilarity] = useState<number | null>(null)
    const [difficulty, setDifficulty] = useState<number | null>(null)

    const handleFetchRecommendedProblem = async () => {
        await getProblemRecommendation().then(data => {
            if(data) {
                setIsOpenSolution(false)
                setAnswer('')
                setProblem(data.problem)
                setSimilarity(data.similarity)
                setDifficulty(data.difficulty)
            }
        })
    };

    // const onFetchProblemButtonClick = () => {
    //     setProblem(null);
    //     handleFetchProblem();
    // };

    const handleOpenSolution = () => {
        setIsOpenSolution(true)
    }

    const handleSelfAnswering = async (solved: boolean) => {
        if(problem) {
            await patchSolvingHistory(problem.id, solved).then(() => {
                handleFetchRecommendedProblem()
            })
        }
    }

    useEffect(() => {
        handleFetchRecommendedProblem()
    }, []);

    return (
        <Box
            width={1}
        >
            <Grid
                container
                spacing={2}
            >
                {problem && (
                    <Grid
                        item
                        xs={12}
                    >
                        <ProblemViewer
                            problem={problem}
                            userAnswer={answer}
                            setUserAnswer={setAnswer}
                            onShowSolution={handleOpenSolution}
                            showSolution={isOpenSolution}
                        />
                    </Grid>
                )}
                {problem && isOpenSolution && (
                    <Grid
                        item
                        xs={12}
                        container
                        justifyContent="flex-end"
                    >
                        <Stack
                            direction="row"
                            spacing={1}
                        >
                            <Button
                                variant="contained"
                                color="success"
                                startIcon={<CheckCircleIcon />}
                                onClick={() => handleSelfAnswering(true)}
                            >
                                맞았어요!
                            </Button>
                            <Button
                                variant="contained"
                                color="error"
                                startIcon={<CancelIcon />}
                                onClick={() => handleSelfAnswering(false)}
                            >
                                틀렸어요
                            </Button>
                        </Stack>
                    </Grid>
                )}
                {problem && isOpenSolution && (
                    <Grid
                        item
                        xs={12}
                    >
                        <Stack
                            spacing={2}
                            sx={{
                                border: '2px solid #1976d2',
                                borderRadius: '16px',
                                padding: 2,
                            }}
                        >
                            <Typography
                                variant="subtitle1"
                            >
                                추천 문제 정보
                            </Typography>
                            <Typography
                                variant="body1"
                            >
                                · 유사도: {similarity}
                            </Typography>
                            <Typography
                                variant="body1"
                            >
                                · 난이도: {difficulty}
                            </Typography>
                        </Stack>
                    </Grid>
                )}
            </Grid>
        </Box>
    )
}
