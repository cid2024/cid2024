import {Problem} from "./problem";

export type ProblemRecommendation = {
    problem: Problem;
    similarity: number;
    difficulty: number;
}
