import asyncio
import pprint
from dataclasses import dataclass

from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class DistractorInfo:
    distractor: str
    reason: str


def gen_distractors(handler: AiHandler, context: str) -> list[DistractorInfo]:
    rag_prompt = get_settings()["distractor_describe_related_prompt"]
    rag_context = asyncio.run(
        run_prompt(
            handler,
            rag_prompt,
            user_vars={
                "context": context,
            },
            system_vars=dict(),
        )
    )

    gen_prompt = get_settings()["distractor_gen_sentences_prompt"]
    response = asyncio.run(
        run_prompt(
            handler,
            gen_prompt,
            user_vars={
                "reference": rag_context,
                "sentence": context,
            },
            system_vars=dict(),
        )
    )

    try:
        data = parse_llm_yaml(response)["distractors"]

        ret: list[DistractorInfo] = []

        for item in data:
            distractor = item.get("sentence", None)
            reason = item.get("explanation", None)
            if distractor and reason:
                ret.append(DistractorInfo(distractor=distractor, reason=reason))

        return ret
    except:
        return []


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    handler = AiHandler()

    for context in [
        "서울은 대한민국의 수도이다.",
        "미국은 1776년에 영국으로부터 독립했다.",
        "성상숭배 문제로 크리스트교 세계가 분열되었다.",
        "고조선은 8조법을 만들어 사회질서를 유지하였다.",
        "서울대학교는 신림동 산56-1번지에 위치하고 있다.",
        "일본은 홋카이도와 도쿄도, 두 개의 부, 43개의 현으로 총 47개의 도도부현으로 구성되어 있다.",
    ]:
        data = gen_distractors(handler, context)

        pp.pprint(context)
        pp.pprint(data)
