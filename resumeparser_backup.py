import requests
import yaml

CONFIG_PATH = r"config.yaml"

with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

OLLAMA_URL = data.get(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = data.get(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)


def ats_extractor(resume_data):

    prompt = '''
You are an AI bot designed to act as a professional resume parser.

You are given a resume and your job is to extract the following information:

1. full name
2. email id
3. github portfolio
4. linkedin id
5. employment details
6. technical skills
7. soft skills

Return the extracted information in valid JSON format only.

Do not use markdown.
Do not add explanations.
Do not write anything before or after the JSON.
'''

    full_prompt = prompt + "\n\nRESUME:\n" + resume_data

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]