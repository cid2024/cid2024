import axios from 'axios';

type StatementElementType = "text" | "image" | "embed_image";

type StatementElement = {
  type: StatementElementType;
  data: string;
}

type Choice = {
  id: string;
  statement: StatementElement[];
}

type Problem = {
  id: string;
  statement: StatementElement[];
  choices: Choice[];
  answer: string;
}

export const getProblemById = (id: number): Promise<Problem | null> => {
  return axios.get<Problem>(`/problems/${id}`, {responseType: 'json'})
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.log(error);
      return null;
    })
}