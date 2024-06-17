import re
import numpy as np

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from settings.textbook_loader import get_textbook


class TextbookProcessor:
    def __init__(self, textbook_data):
        self.text_data = textbook_data
        self.vectorizer = TfidfVectorizer()
        self.text_vectors = None

    def preprocess_text(self):
        self.text_data = re.sub(r'\s+', ' ', self.text_data)
        self.text_data = re.sub(r'[^\w\s]', '', self.text_data)
        self.text_data = self.text_data.lower()

    def vectorize_text(self):
        self.text_vectors = self.vectorizer.fit_transform([self.text_data])

    def find_relevant_section(self, query):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.text_vectors)
        relevant_index = np.argmax(similarities)
        return relevant_index


class SentenceValidator:
    def __init__(self, model_name='t5-small'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.lm_pipeline = pipeline(
            task='text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
        )

    def generate_response(self, prompt):
        response = self.lm_pipeline(prompt, max_length=50)
        return response[0]['generated_text']

    def validate_sentence(self, context, sentence):
        prompt = f"Context: {context} Sentence: {sentence} Is this sentence appropriate? Yes or No"
        return self.generate_response(prompt)


if __name__ == "__main__":
    textbook_names = [
        "eastasia",
        "korean",
        "world",
    ]

    query_sentence = "박지원은 수레와 선박의 필요성 및 화폐 유통의 중요성을 강조하였으며, 박제가는 수레와 배의 이용을 주장하고 소비 촉진을 통한 경제 활성화를 강조하였다."

    for textbook_name in textbook_names:
        reference = '\n'.join(get_textbook(textbook_name))

        processor = TextbookProcessor(reference)
        processor.preprocess_text()
        processor.vectorize_text()

        validator = SentenceValidator()

        section_index = processor.find_relevant_section(query_sentence)
        context = processor.text_data[section_index:section_index+1000]  # 문맥 추출

        validation_result = validator.validate_sentence(context, query_sentence)
        print(f"Validation result: {validation_result}")
