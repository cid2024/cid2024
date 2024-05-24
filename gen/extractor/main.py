import asyncio
import pprint
from dataclasses import dataclass

from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings

from gen.extractor.passage import get_passage
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class KeySentence:
    sentence: str
    keyword: str


def extract_key_sentences(handler: AiHandler, reference: str, expected_num: int) -> list[KeySentence]:
    extract_prompt = get_settings()["extractor_passage_key_sentences_prompt"]
    extract_response = asyncio.run(
        run_prompt(
            handler,
            extract_prompt,
            user_vars={
                "reference": reference,
                "num_sentences": expected_num,
            },
            system_vars=dict(),
        )
    )

    try:
        extract_response = parse_llm_yaml(extract_response)["key_sentences"]
    except:
        return []

    revise_prompt = get_settings()["extractor_passage_revise_sentence_prompt"]

    ret: list[KeySentence] = []
    for sample in extract_response:
        sentence = sample.get("sentence", "").strip()
        keyword = sample.get("keyword", "").strip()

        if not sentence or not keyword:
            continue

        revise_response = asyncio.run(
            run_prompt(
                handler,
                revise_prompt,
                user_vars={
                    "reference": reference,
                    "sentence": sentence,
                    "keyword": keyword,
                },
                system_vars=dict(),
            )
        )

        try:
            revise_response = parse_llm_yaml(revise_response)["revised_sentence"][0]
            sentence = revise_response.get("sentence", "").strip()
            if sentence and keyword:
                ret.append(KeySentence(sentence=sentence, keyword=keyword))
        except:
            pass

    return ret


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    handler = AiHandler()

    passage = get_passage()

    key_sentences = extract_key_sentences(handler, passage, 5)

    pp.pprint(key_sentences)
