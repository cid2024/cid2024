import pickle
import pprint
from dataclasses import dataclass

from gen.distractor import gen_distractors
from gen.distractor.evaluate import evaluate_distractor, DistractorScore
from gen.distractor.generate import ImprovedDistractorInfo, improve_distractor, DistractorInfo, GenDistractorsRet
from gen.extractor import extract_key_sentences, KeySentence
from llm.ai_handler import AiHandler
from settings.textbook_loader import get_textbook


@dataclass(kw_only=True)
class ReferenceRecord:
    textbook_name: str
    page: int
    key_sentence: KeySentence
    orig_distractors_data: GenDistractorsRet
    improved_distractors: list[ImprovedDistractorInfo]
    improved_distractor_scores: list[DistractorScore]


def commit_db():
    handler = AiHandler()

    for textbook_name in [
        # "eastasia",
        "korean",
        # "world",
    ]:
        textbook = list(map(str, filter(None, get_textbook(textbook_name))))
        n_pages = len(textbook)
        if n_pages < 5:
            continue

        textbook_data: list[ReferenceRecord] = []

        file_path = f"gen_distractors_data__{textbook_name}.56.pkl.final"
        with open(file_path, 'rb') as f:
            textbook_data = pickle.load(f)

        run_cnt = 56
        for page in range(115, n_pages - 4, 4):
            reference = '\n'.join(textbook[page: page+5])
            key_sentences = extract_key_sentences(handler, reference, 8)
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

                textbook_data.append(ReferenceRecord(
                    textbook_name=textbook_name,
                    page=page,
                    key_sentence=key_sentence,
                    orig_distractors_data=distractors,
                    improved_distractors=improved_distractors,
                    improved_distractor_scores=distractor_scores,
                ))

            run_cnt += 1
            if run_cnt % 4 == 0:
                file_path = f"gen_distractors_data__{textbook_name}.{run_cnt}.pkl"
                with open(file_path, 'wb') as f:
                    pickle.dump(textbook_data, f)

            print("@" * 10 + f" End {page}/{n_pages} of {textbook_name}")

        file_path = f"gen_distractors_data__{textbook_name}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(textbook_data, f)


if __name__ == "__main__":
    # pp = pprint.PrettyPrinter(indent=4)

    commit_db()

    # with open("gen_distractors_data__korean.pkl", 'rb') as f:
    #     data = pickle.load(f)
    #     pp.pprint(data)
