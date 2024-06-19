export type StatementElementType = "text" | "image" | "embed_image" | "math";

export type StatementElement = {
  type: StatementElementType;
  data: string;
  align?: string;
  border?: boolean;
  title?: string;
}

export type Choice = [string, StatementElement[]];

export type Problem = {
  id: string;
  statement: StatementElement[];
  choice: Choice[];
  answer: string;
}
