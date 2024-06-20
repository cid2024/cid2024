import axios from 'axios';
import {API_URL} from "./global";
import {ProblemRecommendation} from "../types/recommendation";

export const getProblemRecommendation = async (): Promise<ProblemRecommendation | null> => {
    return axios.get<ProblemRecommendation>(
        `${API_URL}/recommend`,
        {
            responseType: 'json',
        },
    ).then(response => {
        return response.data
    }).catch(error => {
        console.log(error)
        return null
    })
};

export const patchSolvingHistory = async (problemId: string, solved: boolean): Promise<void> => {
    return axios.patch(
        `${API_URL}/history/${problemId}/${solved ? 1 : 0}`,
        {
            responseType: 'json',
        },
    ).then(response => {
        return
    }).catch(error => {
        console.log(error)
        return
    })
};
