from openai import OpenAI

from aiwflow.util import get_env_variable

OPENAI_KEY = get_env_variable('OPENAI_KEY')


class AI:
    translate_prompt = "You're a multilingual assistant skilled in translating content into concise English github pull request titles, within 8 words, and without any punctuation."

    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_KEY)

    def translate(self, desc: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.translate_prompt},
                {"role": "user",
                    "content": f"{desc}"}
            ],
            timeout=60,
            max_tokens=60,
        )
        return completion.choices[0].message.content
