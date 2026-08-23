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

    prompt = """
You are a resume parser.

Extract the following information:

1. full_name
2. email
3. github
4. linkedin
5. employment
6. technical_skills
7. soft_skills

Return ONLY valid JSON.

Example:

{
    "full_name": "",
    "email": "",
    "github": "",
    "linkedin": "",
    "employment": [],
    "technical_skills": [],
    "soft_skills": []
}

Do not add markdown.
Do not add explanations.
"""

    # Prevent extremely large prompts
    resume_data = resume_data[:12000]

    full_prompt = prompt + "\n\nRESUME:\n" + resume_data

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": 500
            }
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]