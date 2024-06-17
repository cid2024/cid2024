import pprint
from dataclasses import dataclass
from random import randint

from gen.distractor import gen_distractors
from gen.distractor.evaluate import evaluate_distractor
from gen.distractor.generate import ImprovedDistractorInfo, improve_distractor, DistractorInfo
from gen.extractor import extract_key_sentences, KeySentence
from llm.ai_handler import AiHandler
from settings.textbook_loader import get_textbook


@dataclass(kw_only=True)
class ChoiceStatement:
    correct_text: str
    wrong_text: str
    wrong_reason: str


def gen_choice_statements(
        handler: AiHandler,
        reference: str,
        choice_num: int,
) -> list[tuple[str, list[ChoiceStatement]]]:
    ret: list[tuple[str, list[ChoiceStatement]]] = []

    key_sentences = extract_key_sentences(handler, reference, int(choice_num * 1.5))
    for key_sentence in key_sentences:
        distractors = gen_distractors(handler, key_sentence.sentence)
        if not distractors:
            continue

        improved_distractors: list[ImprovedDistractorInfo] = []
        for distractor in distractors.distractors:
            improved_distractor = improve_distractor(handler, key_sentence.sentence, distractor)
            if improved_distractor:
                improved_distractors.append(improved_distractor)

        mock_distractors = [
            DistractorInfo(
                distractor=improved_distractor.improved_distractor,
                reason=improved_distractor.improved_reason,
            )
            for improved_distractor in improved_distractors
        ]

        distractor_scores = evaluate_distractor(handler, distractors.rag_context, mock_distractors)

        indices = [
            idx
            for idx, distractor_score in enumerate(distractor_scores)
            if 9 <= distractor_score.accuracy_score and 8 <= distractor_score.sense_score
        ]
        indices.sort(key=lambda x: distractor_scores[x].accuracy_score + distractor_scores[x].sense_score, reverse=True)

        if indices:
            ret.append((
                key_sentence.keyword,
                [
                    ChoiceStatement(
                        correct_text=key_sentence.sentence,
                        wrong_text=mock_distractors[idx].distractor,
                        wrong_reason=mock_distractors[idx].reason,
                    )
                    for idx in indices
                ],
            ))

    return ret


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    handler = AiHandler()

    page = 180
    reference = get_textbook("korean")[page: page+3]
    expected_num = 4

    choice_statements = gen_choice_statements(handler, reference, expected_num)
    pp.pprint(choice_statements)
