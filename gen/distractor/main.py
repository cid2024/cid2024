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


@dataclass(kw_only=True)
class GenDistractorsRet:
    distractors: list[DistractorInfo]
    rag_context: str


def gen_distractors(handler: AiHandler, context: str) -> GenDistractorsRet | None:
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
    ).strip()

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
            distractor = item.get("sentence", "").strip()
            reason = item.get("explanation", "").strip()

            if distractor and reason:
                ret.append(DistractorInfo(distractor=distractor, reason=reason))

        if not ret:
            return None

        return GenDistractorsRet(distractors=ret, rag_context=rag_context)
    except:
        return None


def gen_korean_history_distractors(handler: AiHandler, context: str) -> GenDistractorsRet | None:
    rag_prompt = get_settings()["distractor_history_korean_describe_related_prompt"]
    rag_context = asyncio.run(
        run_prompt(
            handler,
            rag_prompt,
            user_vars={
                "context": context,
            },
            system_vars=dict(),
        )
    ).strip()

    gen_prompt = get_settings()["distractor_history_korean_gen_sentences_prompt"]
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
            distractor = item.get("sentence", "").strip()
            reason = item.get("explanation", "").strip()
            if distractor and reason:
                ret.append(DistractorInfo(distractor=distractor, reason=reason))

        if not ret:
            return None

        return GenDistractorsRet(distractors=ret, rag_context=rag_context)
    except:
        return None


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    handler = AiHandler()

    # for context in [
    #     "서울은 대한민국의 수도이다.",
    #     "미국은 1776년에 영국으로부터 독립했다.",
    #     "성상숭배 문제로 크리스트교 세계가 분열되었다.",
    #     "고조선은 8조법을 만들어 사회질서를 유지하였다.",
    #     "서울대학교는 신림동 산56-1번지에 위치하고 있다.",
    #     "일본은 홋카이도와 도쿄도, 두 개의 부, 43개의 현으로 총 47개의 도도부현으로 구성되어 있다.",
    # ]:
    #     data = gen_distractors(handler, context)
    #
    #     pp.pprint(context)
    #     pp.pprint(data)

    for context in [
        "서학은 조선의 과학 기술 발전과 지식인들의 세계관 형성에 중요한 영향을 미쳤다.",
        # "실증적인 연구 방법을 통해 사회 모순을 해결하려는 실학이 등장하였다.",
        # "유형원은 신분에 따라 차등을 두어 일정한 면적의 토지를 분배하는 균전론을 제시하였다.",
        # "정약용은 토지를 공동으로 경작한 후 수확물을 분배하는 여전제를 주장하였다.",
        # "박지원은 수레와 선박의 필요성 및 화폐 유통의 중요성을 강조하였으며, 박제가는 수레와 배의 이용을 주장하고 소비 촉진을 통한 경제 활성화를 강조하였다.",
        # "18세기 후반에 정권에서 밀려난 남인 계열의 실학자들이 천주교를 서양의 학문이 아닌 신앙으로 받아들이기 시작했다.",
        # "동학은 '사람이 곧 하늘'이라는 인내천 사상을 바탕으로 인간의 평등을 강조하여 하층민들의 큰 호응을 얻었다.",
    ]:
        data = gen_korean_history_distractors(handler, context)

        pp.pprint(context)
        pp.pprint(data)
