import asyncio
import pprint
from dataclasses import dataclass

from gen.distractor import DistractorInfo, gen_distractors
from gen.distractor.generate import improve_distractor
from gen.extractor import extract_key_sentences
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from settings.textbook_loader import get_textbook
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class DistractorScore:
    accuracy_score: int
    accuracy_reason: str
    sense_score: int
    sense_reason: str


def evaluate_distractor(
        handler: AiHandler,
        reference: str,
        distractors: list[DistractorInfo],
) -> list[DistractorScore]:
    ret: list[DistractorScore] = [
        DistractorScore(
            accuracy_score=-1,
            accuracy_reason="",
            sense_score=-1,
            sense_reason="",
        )
        for _ in distractors
    ]

    prompt = get_settings()["distractor_eval_distractors_prompt"]
    response = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "reference": reference,
                "distractors": (
                    "\n\n".join([
                        f"선택지 {chr(ord('A') + idx)}) {distractor.distractor}\n"
                        f"출제 의도: {distractor.reason}"
                        for idx, distractor in enumerate(distractors)
                    ])
                ),
            },
            system_vars=dict(),
        )
    )

    try:
        data = parse_llm_yaml(response)["evaluations"]
        for item in data:
            idx = item.get("index", "").strip()
            if 1 != len(idx) or not (ord('A') <= ord(idx) <= ord('Z')):
                continue
            idx = ord(idx) - ord('A')
            if idx < 0 or idx >= len(distractors):
                continue

            score: int
            try:
                score = int(item.get("score", 0))
                score = max(0, min(10, score))
            except:
                score = 0

            reason = item.get("explanation", "").strip()

            if reason:
                ret[idx].accuracy_score = score
                ret[idx].accuracy_reason = reason
    except:
        pass

    prompt = get_settings()["distractor_eval_make_sense_prompt"]
    response = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "reference": reference,
                "choices": (
                    "\n\n".join([
                        f"선택지 {chr(ord('A') + idx)}) {distractor.distractor}\n"
                        f"출제 의도: {distractor.reason}\n"
                        f"오답 근거: {ret[idx].accuracy_reason}"
                        for idx, distractor in enumerate(distractors)
                    ])
                ),
            },
            system_vars=dict(),
        )
    )

    try:
        data = parse_llm_yaml(response)["evaluations"]
        for item in data:
            idx = item.get("index", "").strip()
            if 1 != len(idx) or not (ord('A') <= ord(idx) <= ord('Z')):
                continue
            idx = ord(idx) - ord('A')
            if idx < 0 or idx >= len(distractors):
                continue

            score: int
            try:
                score = int(item.get("score", 0))
                score = max(0, min(10, score))
            except:
                score = 0

            reason = item.get("explanation", "").strip()

            if reason:
                ret[idx].sense_score = score
                ret[idx].sense_reason = reason
    except:
        pass

    return ret


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    handler = AiHandler()
    textbook = get_textbook("korean")

    for i in range(len(textbook)):
        print(i, textbook[i][:50])

    n = 123

    keys = extract_key_sentences(handler, '\n'.join(textbook[n:n+3]), 7)

    pp.pprint(keys)

    data = []

    for key in keys:
        gen_distrs_ret = gen_distractors(handler, key.sentence)
        if not gen_distrs_ret:
            continue

        improved_ret = []

        for distr in gen_distrs_ret.distractors:
            improved = improve_distractor(handler, key.sentence, distr)
            if improved:
                improved_ret.append(improved)

        mock_distrs = [
            DistractorInfo(
                distractor=improved.improved_distractor,
                reason=improved.improved_reason,
            )
            for improved in improved_ret
        ]

        scores = evaluate_distractor(handler, gen_distrs_ret.rag_context, mock_distrs)

        pp.pprint(key)
        pp.pprint(mock_distrs)
        pp.pprint(scores)
        print("\n" * 5)
