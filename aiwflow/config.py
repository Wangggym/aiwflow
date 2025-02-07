import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / '.aiwflow'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            'llm_provider': 'openai'  # 默认使用 openai
        }
        self._ensure_config_exists()
        self._load_config()

    def _ensure_config_exists(self):
        """Ensure config directory and file exist"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self._save_config(self.default_config)

    def _load_config(self):
        """Load configuration"""
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def _save_config(self, config):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def get_llm_provider(self) -> str:
        """Get current LLM provider"""
        return self.config.get('llm_provider', 'openai')

    def set_llm_provider(self, provider: str):
        """Set LLM provider
        
        Args:
            provider: 'openai', 'deepseek' or 'proxy'
        """
        if provider not in ['openai', 'deepseek', 'proxy']:
            raise ValueError("Provider must be one of: 'openai', 'deepseek', or 'proxy'")
        self.config['llm_provider'] = provider
        self._save_config(self.config) 