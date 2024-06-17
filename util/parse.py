import re
import yaml


def postprocess_response(response) -> str:
    response = str(response)
    if response.endswith("stop"):
        response = response[:-4]
    pattern = r'```\w*\n(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        response = matches[0]
    response = response.replace('"', '\\"').replace("'", "\\'")
    return response


def parse_llm_yaml(yaml_response: str, strict: bool = False):
    if not strict:
        # Remove leading and trailing whitespaces
        yaml_response = '\n'.join(map(str.rstrip, yaml_response.split('\n'))).strip()

        # Remove "```yaml" in the first line
        if yaml_response.startswith("```"):
            yaml_response = '\n'.join(yaml_response.split('\n')[1:])

        # Remove "```" in the last line
        if yaml_response.endswith("```"):
            yaml_response = '\n'.join(yaml_response.split('\n')[:-1])

    data = None

    try:
        data = yaml.safe_load(yaml_response)
    except:
        yaml_response = postprocess_response(yaml_response)
        try:
            data = yaml.safe_load(yaml_response)
        except:
            data = None

    return data


if __name__ == "__main__":
    yaml_response = """\
```yaml
distractors:
- sentence: 무함마드가 사망한 후, 이슬람 세계의 지도자로 칼리프가 선출되지 않았고, 이 시기를 정통 칼리프 시대라고 한다.
  explanation: 무함마드 사망 후 실제로 칼리프가 선출되었으나, 부정형으로 표현하여 혼동을 줄 수 있다.
- sentence: 무함마드가 사망한 후, 이슬람 세계의 지도자로 칼리프가 선출되었고, 이 시기를 우마이야 왕조 시대라고 한다.
  explanation: 정통 칼리프 시대와 우마이야 왕조 시대를 혼동하게 만들어 학생들이 잘못된 선택을 할 수 있다.
- sentence: 무함마드가 사망한 후, 이슬람 세계의 지도자로 칼리프가 선출되었고, 이 시기를 아바스 왕조 시대라고 한다.
  explanation: 아바스 왕조는 정통 칼리프 시대 이후의 시기로, 시기를 혼동하게 만들어 학생들을 헷갈리게 할 수 있다.
- sentence: 무함마드가 사망한 후, 이슬람 세계의 지도자로 셰이크가 선출되었고, 이 시기를 정통 칼리프 시대라고 한다.
  explanation: 칼리프 대신 셰이크라는 다른 이슬람 지도자를 언급하여 혼란을 줄 수 있다.
- sentence: 무함마드가 사망한 후, 이슬람 세계의 지도자로 칼리프가 선출되었고, 이 시기를 초기 칼리프 시대라고 한다.
  explanation: '정통'과 '초기'라는 용어를 바꾸어 사용하여 시기 명칭에 대해 혼란을 줄 수 있다.
```
"""

    data = parse_llm_yaml(yaml_response)
    print(data)
