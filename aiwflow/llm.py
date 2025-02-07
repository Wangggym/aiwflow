from openai import OpenAI
from aiwflow.util import get_env_variable
from aiwflow.config import Config

OPENAI_KEY = get_env_variable('OPENAI_KEY')
DEEPSEEK_KEY = get_env_variable('DEEPSEEK_KEY', required=False)
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
# Add environment variables for proxy
OPENAI_PROXY_URL = get_env_variable('OPENAI_PROXY_URL', required=False)
OPENAI_PROXY_KEY = get_env_variable('OPENAI_PROXY_KEY', required=False) 

class AI:
    translate_prompt = "You're a multilingual assistant skilled in translating content into concise English github pull request titles, within 8 words, and without any punctuation."

    def __init__(self) -> None:
        self.config = Config()
        provider = self.config.get_llm_provider()
        
        if provider == 'deepseek':
            if not DEEPSEEK_KEY:
                raise ValueError("DEEPSEEK_KEY environment variable is required when using DeepSeek")
            self.client = OpenAI(
                api_key=DEEPSEEK_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
            self.model = "deepseek-chat"
            print(f"Using DeepSeek LLM provider")
        elif provider == 'proxy':
            if not OPENAI_PROXY_URL:
                raise ValueError("OPENAI_PROXY_URL environment variable is required when using proxy")
            if not OPENAI_PROXY_KEY:
                raise ValueError("OPENAI_PROXY_KEY environment variable is required when using proxy")
            self.client = OpenAI(
                api_key=OPENAI_PROXY_KEY,  # Use proxy-specific API key
                base_url=OPENAI_PROXY_URL
            )
            self.model = "gpt-3.5-turbo"
            print(f"Using OpenAI with proxy: {OPENAI_PROXY_URL}")
        else:  # default to openai
            self.client = OpenAI(api_key=OPENAI_KEY)
            self.model = "gpt-3.5-turbo"
            print(f"Using OpenAI LLM provider")

    @classmethod
    def switch_provider(cls, provider: str):
        """Switch LLM provider
        
        Args:
            provider: 'openai', 'deepseek' or 'proxy'
        """
        if provider not in ['openai', 'deepseek', 'proxy']:
            raise ValueError("Provider must be one of: openai, deepseek, proxy")
        config = Config()
        config.set_llm_provider(provider)

    def translate(self, desc: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.translate_prompt},
                {"role": "user", "content": f"{desc}"}
            ],
            timeout=60,
            max_tokens=60,
        )
        return completion.choices[0].message.content
