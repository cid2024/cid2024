import axios from 'axios';
import {API_URL} from "./global";
import {Problem} from "../types/problem";

export const getProblemById = async (id: string): Promise<Problem | null> => {
    return axios.get<Problem>(
        `${API_URL}/problems/${id}`,
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
