import asyncio
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings

from transformers import BertTokenizer, BertModel
import torch

import json

model = None
tokenizer = None

def get_parameters(problem):
    meta = problem.get_attribute("code")

    description = ""
    problem_array = meta.get_attribute("problem_array")
    for piece in json.loads(problem_array):
        typename = piece["type"]
        if (typename == "image"):
            pass
        else:
            description += piece[typename] + "\n"
    
    selections = []
    for i in range(1, 6):
        selection_text = "s" + str(i)
        if meta.has_attribute(selection_text):
            selection = meta.get_attribute(selection_text)
            if len(selection) > 0:
                selections.append(selection)
    
    answer = json.loads(meta.get_attribute("answer_grading"))[0]

    if len(selections) > 0:
        try:
            answer = selections[int(answer)-1]
        except:
            pass # Do nothing, 'answer' remains unchanged

    return description, selections, answer

def encode (description, selections, answer):
    handler = AiHandler()
    
    prompt = get_settings()["similarity_util_translate"]
    translated_problem = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "description": description,
                "answer": answer
            },
            system_vars=dict(),
        )
    )

    prompt = get_settings()["similarity_util_explain"]
    explanation = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "problem": translated_problem,
            },
            system_vars=dict(),
        )
    )

    prompt = get_settings()["similarity_util_keyword"]
    keywords = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "passage": explanation
            },
            system_vars=dict(),
        )
    )

    # Load pre-trained model tokenizer (vocabulary)
    global tokenizer
    if tokenizer == None:
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Load pre-trained model (weights)
    global model
    if model == None:
        model = BertModel.from_pretrained('bert-base-uncased')
        model.eval()

    # Tokenize the text
    inputs = tokenizer(keywords, return_tensors='pt', max_length=512, truncation=True, padding=True)

    # Get the hidden states from BERT
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract the last hidden state
    last_hidden_states = outputs.last_hidden_state

    # Mean of the last hidden states
    sentence_vector = last_hidden_states.mean(dim=1)

    return sentence_vector.flatten()

def encode_problem (problem):
    description, selections, answer = get_parameters(problem)
    return encode(description, selections, answer)
