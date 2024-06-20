import {Problem, StatementElement} from "../types/problem";
import {Box, Stack, Typography} from "@mui/material";


interface StatementElementViewerProps {
    element: StatementElement;
}

const StatementElementViewer = ({
    element,
}: StatementElementViewerProps) => {
    if(element.type === "text") {
        return (
            <Typography
                variant="body1"
            >
                {element.data}
            </Typography>
        )
    }
    if(element.type === "image") {
        return (
            <Box
                component="img"
                sx={{
                    width: '600px',
                    height: 'auto',
                    borderRadius: '16px',
                }}
                alt="Problem Image"
                src={element.data}
            />
        )
    }
    if(element.type === "embed_image") {
        return (
            <Box
                component="img"
                sx={{
                    width: '800px',
                    height: 'auto',
                    borderRadius: '16px',
                }}
                alt="Problem Embedded Image"
                src={"data:image/png;base64," + element.data}
            />
        )
    }
    return (
        <>
            Not implemented.
        </>
    )
}


interface ProblemViewerProps {
    problem: Problem;
    showSolution?: boolean;
}

export const ProblemViewer = ({
    problem,
    showSolution = false,
}: ProblemViewerProps) => {
    return (
        <Box width={1}>
            <Stack
                spacing={1}
            >
                <Stack
                    spacing={2}
                    sx={{
                        border: '2px solid #1976d2',
                        borderRadius: '16px',
                        padding: 2,
                    }}
                >
                    {problem.statement.map(element => (
                        <StatementElementViewer
                            element={element}
                            key={element.data}
                        />
                    ))}
                    {problem.choice.map(([choice, statement], index) => (
                        <Stack
                            key={choice}
                            direction="row"
                            spacing={2}
                        >
                            <Typography
                                variant="button"
                                sx={{
                                    whiteSpace: 'nowrap',
                                }}
                            >
                                {choice + ")"}
                            </Typography>
                            <Stack
                                spacing={1}
                            >
                                {statement.map(element => (
                                    <StatementElementViewer
                                        element={element}
                                        key={element.data}
                                    />
                                ))}
                            </Stack>
                        </Stack>
                    ))}
                </Stack>
                {showSolution && (
                    <Stack
                        spacing={2}
                        sx={{
                            border: '2px solid #1976d2',
                            borderRadius: '16px',
                            padding: 2,
                        }}
                    >
                        <Stack
                            direction="row"
                            spacing={2}
                        >
                            <Typography
                                variant="button"
                                sx={{
                                    whiteSpace: 'nowrap',
                                }}
                            >
                                정답)
                            </Typography>
                            <Typography
                                variant="body1"
                            >
                                {problem.answer}
                            </Typography>
                        </Stack>
                        {problem.explanation && (
                            <Stack
                                direction="row"
                                spacing={2}
                            >
                                <Typography
                                    variant="button"
                                    sx={{
                                        whiteSpace: 'nowrap',
                                    }}
                                >
                                    해설)
                                </Typography>
                                <Typography
                                    variant="body1"
                                >
                                    {problem.explanation}
                                </Typography>
                            </Stack>
                        )}
                    </Stack>
                )}
            </Stack>
        </Box>
    );
};
