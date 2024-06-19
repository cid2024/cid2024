export type StatementElementType = "text" | "image" | "embed_image";

export type StatementElement = {
    type: StatementElementType;
    data: string;
}

export type Choice = [string, StatementElement[]];

export type Problem = {
    id: string;
    statement: StatementElement[];
    choice: Choice[];
    answer: string;
    explanation: string;
}
