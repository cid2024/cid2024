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
    except yaml.YAMLError:
        yaml_response = postprocess_response(yaml_response)
        data = yaml.safe_load(yaml_response)

    return data
