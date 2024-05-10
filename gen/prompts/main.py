
import asyncio
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from settings.db_loader import get_full_data

from gen.prompts.passage import get_passage

NUM_SENTENCES = 5

def get_all_items():
    data = get_full_data()
    cnt = 0
    for id, problem in data["Problem"].items():
        print(problem)
        if cnt == 0: break
        

if __name__ == "__main__":
    passage = get_passage()

    handler = AiHandler()

    prompt = get_settings()["passage_get_sentences_prompt"]

    response = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "passage": passage,
                "num_sentences": NUM_SENTENCES,
            },
            system_vars=dict(),
        )
    )


    print(f"{response = }")

    sentences = list(response.split("\n"))
    
    items = []

    prompt = get_settings()["sentence_to_item_prompt"]

    for sentence in sentences:
      response = asyncio.run(
          run_prompt(
              handler,
              prompt,
              user_vars={
                  "sentence": sentence,
              },
              system_vars=dict(),
          )
      )

      print(f"{response = }")

