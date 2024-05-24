import asyncio
import pprint
from dataclasses import dataclass
from random import random, randint

from gen.distractor import gen_distractors, DistractorInfo
from gen.extractor import extract_key_sentences
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from settings.textbook_loader import get_textbook
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class DistractorScore:
    index: int
    score: int
    reason: str


def evaluate_distractor(
        handler: AiHandler,
        reference: str,
        distractors: list[DistractorInfo],
) -> list[DistractorScore]:
    prompt = get_settings()["abcselect_eval_distractors_prompt"]
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

        ret: list[DistractorScore] = []

        for item in data:
            idx = item.get("index", "").strip()
            if 1 != len(idx) or not (ord('A') <= ord(idx) <= ord('Z')):
                continue
            idx = ord(idx) - ord('A')
            if idx < 0 or idx >= len(distractors):
                continue

            score = 0
            try:
                score = int(item.get("score", 0))
                score = max(0, min(10, score))
            except:
                score = 0

            reason = item.get("explanation", "").strip()

            if reason:
                ret.append(DistractorScore(index=idx, score=score, reason=reason))

        return ret
    except:
        return []


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

        if gen_distrs_ret:
            scores = evaluate_distractor(handler, gen_distrs_ret.rag_context, gen_distrs_ret.distractors)

            data.append((key, gen_distrs_ret, scores))

    pp.pprint(data)

    fuck = []

    for i in range(len(data)):
        key, gen_distrs_ret, scores = data[i]
        scores = [s for s in scores if s.score >= 9]

        if scores and random() < 0.6:
            j = randint(0, len(scores) - 1)
            j = scores[j].index

            fuck.append((
                gen_distrs_ret.distractors[j].distractor,
                "Wrong bitch",
                key.sentence,
                gen_distrs_ret.distractors[j].reason,
            ))
        else:
            fuck.append((
                key.sentence,
                "Correct",
                None,
                None,
            ))

    for i in range(len(fuck)):
        print("가나다라마바사아자차"[i] + ")", fuck[i][0])

    print("\n" * 10)

    pp.pprint(fuck)
