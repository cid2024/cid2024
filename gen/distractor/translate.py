from transformers import pipeline


# Initialize translation pipelines
translator_to_english = pipeline('translation_ko_to_en', model='Helsinki-NLP/opus-mt-ko-en')
translator_to_korean = pipeline('translation_en_to_ko', model='Helsinki-NLP/opus-mt-en-ko')


if __name__ == "__main__":
    # Example sentence
    sentence_ko = "한국의 역사는 매우 흥미롭습니다."

    # Translate to English and back to Korean
    translated_to_en = translator_to_english(sentence_ko)[0]['translation_text']
    back_translated_to_ko = translator_to_korean(translated_to_en)[0]['translation_text']

    print("Original:", sentence_ko)
    print("Translated to English:", translated_to_en)
    print("Back-translated to Korean:", back_translated_to_ko)
