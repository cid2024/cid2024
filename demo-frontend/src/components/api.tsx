import axios from 'axios';
import { Problem } from './types';

const API_URL = 'http://127.0.0.1:6610';

export const getProblemById = (id: string): Promise<Problem | null> => {
  return axios.get<Problem>(`${API_URL}/problems/${id}`, {responseType: 'json'})
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.log(error);
      return null;
    })
}