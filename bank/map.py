import asyncio
import base64
import pickle
import pprint
import random
from dataclasses import dataclass
from pathlib import Path

from bank import models
from bank.region import RegionBlankRecord, RegionBlankDistractor, RegionBlankPossibleAnswer
import bank.region as bank_region
from gen.maps.main import get_optimized_map_base64
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class RegionData:
    name: str
    formal_kor_name: str
    formal_eng_name: str


def commit_db_data() -> None:
    region_keys: list[str] = []

    for record in bank_region.region_blank_records:
        region_keys.append(record.problem.answer)

        for possible_answer in record.possible_answers:
            region_keys.append(possible_answer.name)

        for distractor in record.distractors:
            region_keys.append(distractor.name)

    region_keys = sorted(list(set(region_keys)))

    handler = AiHandler()
    prompt = get_settings()["bank_map_get_location_prompt"]

    ret: list[RegionData] = []

    for idx, region_name in enumerate(region_keys):
        print("@" * 10, idx, '/', len(region_keys))

        response = asyncio.run(
            run_prompt(
                handler,
                prompt,
                user_vars={
                    "place": region_name,
                },
                system_vars=dict(),
            )
        )

        try:
            data = parse_llm_yaml(response)["place"]
            if isinstance(data, list):
                data = data[0]

            kor_name = data.get("kor_name", "").strip()
            eng_name = data.get("eng_name", "").strip()

            if kor_name and eng_name:
                ret.append(RegionData(
                    name=region_name,
                    formal_kor_name=kor_name,
                    formal_eng_name=eng_name,
                ))
        except:
            pass

    with open("map_region_data.pickle", "wb") as f:
        pickle.dump(ret, f)


regions_data: list[RegionData] = []


def load_db_region_data() -> None:
    raise NotImplementedError("Deprecated.")

    global regions_data

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "map_region_data.pickle.final", "rb") as f:
        regions_data = pickle.load(f)


def commit_db_resolved_data() -> None:
    global regions_data

    load_db_region_data()
    bank_region.load_db_possible_records()

    region_keys: list[str] = []
    for record in bank_region.region_blank_records:
        region_keys.append(record.problem.answer)

    # failed: list[str] = []
    #
    # for idx, region_data in enumerate(regions_data):
    #     print(region_data, idx, '/', len(regions_data))
    #
    #     base_str = get_optimized_map_base64(
    #         query_list=[region_data.formal_eng_name],
    #         use_points=True,
    #         annotated=False,
    #     )
    #
    #     if not base_str:
    #         failed.append(region_data.name)
    #         continue
    #
    #     image_data = base64.b64decode(base_str)
    #     with open(f"test-images/{region_data.name}.png", 'wb') as file:
    #         file.write(image_data)
    #
    # print(failed)

    data: dict[str, RegionData] = {
        region_data.name: region_data
        for region_data in regions_data
    }

    for name in ['교통수단', '교황령', '마라톤', '미드웨이', '유엔', '을사', '인도적', '일본 제국', '일본군', '조미', '중국군', '평안도', '한일']:
        data.pop(name)

    # 고구려
    # 고려
    # 그리스 -> "Athens, Greece"
    # 나일강
    # 당나라
    # 명나라
    # 모스크바 -> "Moscow, Russia"
    # 몽골 -> "Ulaanbaatar, Mongolia"
    # 발해
    # 베트남 북부
    # 송나라
    # 수나라
    # 시베리아 -> "Siberia, Russia"
    # 신라
    # 오나라
    # 오사카 -> "Osaka, Japan"
    # 오키나와 -> "Okinawa, Japan"
    # 요르단 -> "Amman, Jordan"
    # 우창
    # 우한 -> "Wuhan, China"
    # 원나라
    # 월나라
    # 위나라
    # 임안
    # 전진
    # 제나라
    # 중동
    # 진나라
    # 청나라
    # 초나라
    # 촉나라
    # 하얼빈 -> "Harbin, China"
    # 한나라
    # 화성 -> "Hwaseong, Gyeonggi, South Korea"
    # 황하
    # 황허
    # 후쿠시마 -> "Fukushima, Japan"
    # 히로시마 -> "Hiroshima, Japan"

    for name in ['고구려', '고려', '나일강', '당나라', '명나라', '발해', '베트남 북부', '송나라', '수나라', '신라', '오나라', '우창', '원나라', '월나라', '위나라', '임안', '전진', '제나라', '중동', '진나라', '청나라', '초나라', '촉나라', '한나라', '황하']:
        data.pop(name)

    # 개경
    # 강화
    # 경상북도
    # 남경
    # 랴오둥반도
    # 만주국
    # 만주군
    # 발칸 반도
    # 보스니아
    # 비엔나
    # 빈
    # 산둥
    # 상해
    # 서인도
    # 아라비아 반도
    # 알프스 산맥
    # 오스만 제국
    # 요동반도
    # 우크라이나 공화국
    # 워싱턴 D.C.
    # 인더스 강
    # 인더스강
    # 중원
    # 중화인민공화국
    # 충청남도
    # 콘스탄티노플
    # 티그리스강
    # 함경남도
    # 황허

    for name in ['개경', '강화', '경상북도', '남경', '랴오둥반도', '만주국', '만주군', '발칸 반도', '보스니아', '비엔나', '빈', '산둥', '상해', '서인도', '아라비아 반도', '알프스 산맥', '오스만 제국', '요동반도', '우크라이나 공화국', '워싱턴 D.C.', '인더스 강', '인더스강', '중원', '중화인민공화국', '충청남도', '콘스탄티노플', '티그리스강', '함경남도', '황허']:
        data.pop(name)

    # 고조선
    # 군사적 제재
    # 금강산
    # 금관가야
    # 낙랑군
    # 대야성
    # 대흥성
    # 독일령 남태평양
    # 독일령 남태평양 제도
    # 마야 문명
    # 몽골고원
    # 북간도
    # 비잔티움 제국
    # 비잔틴 제국
    # 사로국
    # 사파비 왕조
    # 서간도
    # 서태평양
    # 셀레우코스 제국
    # 소련
    # 신성 로마 제국
    # 신흥무관학교
    # 에도 막부
    # 여진
    # 연나라
    # 우크라이나 소비에트 사회주의 공화국
    # 인더스 문명
    # 졸본
    # 춘추전국시대
    # 칸발릭
    # 평양성
    # 함경북도
    # 흉노

    for name in ['고조선', '군사적 제재', '금강산', '금관가야', '낙랑군', '대야성', '대흥성', '독일령 남태평양', '독일령 남태평양 제도', '마야 문명', '몽골고원', '북간도', '비잔티움 제국', '비잔틴 제국', '사로국', '사파비 왕조', '서간도', '서태평양', '셀레우코스 제국', '소련', '신성 로마 제국', '신흥무관학교', '에도 막부', '여진', '연나라', '우크라이나 소비에트 사회주의 공화국', '인더스 문명', '졸본', '춘추전국시대', '칸발릭', '평양성', '함경북도', '흉노']:
        data.pop(name)

    # 모스크바 -> "Moscow, Russia"
    # 몽골 -> "Ulaanbaatar, Mongolia"
    # 시베리아 -> "Siberia, Russia"
    # 오사카 -> "Osaka, Japan"
    # 오키나와 -> "Okinawa, Japan"
    # 요르단 -> "Amman, Jordan"
    # 우한 -> "Wuhan, China"
    # 하얼빈 -> "Harbin, China"
    # 화성 -> "Hwaseong, Gyeonggi, South Korea"
    # 후쿠시마 -> "Fukushima, Japan"
    # 히로시마 -> "Hiroshima, Japan"

    data["모스크바"].formal_eng_name = "Moscow, Russia"
    data["몽골"].formal_eng_name = "Ulaanbaatar, Mongolia"
    data["시베리아"].formal_eng_name = "Siberia, Russia"
    data["오사카"].formal_eng_name = "Osaka, Japan"
    data["오키나와"].formal_eng_name = "Okinawa, Japan"
    data["요르단"].formal_eng_name = "Amman, Jordan"
    data["우한"].formal_eng_name = "Wuhan, China"
    data["하얼빈"].formal_eng_name = "Harbin, China"
    data["화성"].formal_eng_name = "Hwaseong, Gyeonggi, South Korea"
    data["후쿠시마"].formal_eng_name = "Fukushima, Japan"
    data["히로시마"].formal_eng_name = "Hiroshima, Japan"

    regions_data = list(data.values())

    with open("map_region_resolved_data.pickle", "wb") as f:
        pickle.dump(regions_data, f)


def load_db_resolved_region_data() -> None:
    global regions_data

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "map_region_resolved_data.pickle.final", "rb") as f:
        regions_data = pickle.load(f)


def commit_db_map_problems() -> None:
    regions_dict: dict[str, RegionData] = {
        region_data.name: region_data
        for region_data in regions_data
    }

    map_problems: list[models.Problem] = []

    for idx, record in enumerate(bank_region.region_blank_records):
        print("@" * 10, idx, '/', len(bank_region.region_blank_records))

        if 1 != len(record.possible_answers):
            continue

        if record.problem.answer not in regions_dict:
            continue

        choices: list[str] = sorted(list(set(
            [record.problem.answer]
            + [
                distractor.name
                for distractor in record.distractors
                if distractor.name in regions_dict
            ]
        )))

        if len(choices) < 3:
            continue

        random.shuffle(choices)

        map_base_str = get_optimized_map_base64(
            query_list=[
                regions_dict[region_name].formal_eng_name
                for region_name in choices
            ],
            use_points=False,
            annotated=True,
        )

        if not map_base_str:
            continue

        map_problems.append(
            models.Problem(
                id=f"gen.region.map.{idx}",
                statement=[
                    models.StatementElement(
                        type="text",
                        data=record.problem.statement[0].data[:-5] + "지도에서 고르세요.",
                    ),
                    record.problem.statement[1],
                    models.StatementElement(
                        type="embed_image",
                        data=map_base_str,
                    ),
                ],
                choice=[],
                answer=["가", "나", "다", "라", "마", "바", "사"][choices.index(record.problem.answer)],
                explanation=record.problem.answer,
            )
        )

        if idx % 20 == 0:
            with open(f"map_problems.{idx}.pickle", "wb") as f:
                pickle.dump(map_problems, f)

    with open("map_problems.pickle", "wb") as f:
        pickle.dump(map_problems, f)


map_problems: list[models.Problem] = []


def load_db_map_problems() -> None:
    global map_problems

    parent_dir = Path(__file__).resolve().parent
    for i in range(4):
        with open(parent_dir / f"map_problems.{i}.pickle.final", "rb") as f:
            map_problems.extend(pickle.load(f))


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    load_db_map_problems()

    print(len(map_problems))
