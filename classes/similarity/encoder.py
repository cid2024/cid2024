import asyncio
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from classes.common.textify import textify_mise, textify_gen
from classes.common.data_entry import DataEntry
from bank.models import Problem

from transformers import BertTokenizer, BertModel
import torch

model = None
tokenizer = None

def encode (problem_text:str) -> torch.Tensor:
    handler = AiHandler()
    
    prompt = get_settings()["similarity_util_translate"]
    translated_problem = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "problem": problem_text
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

def encode_mise (problem:DataEntry) -> torch.Tensor:
    return encode(textify_mise(problem))

def encode_gen (problem:Problem) -> torch.Tensor:
    return encode(textify_gen(problem))
