from dataclasses import dataclass, field
from yamldataclassconfig.config import YamlDataClassConfig
from typing import List, Dict


@dataclass
class MSDSConfig(YamlDataClassConfig):
    OPENAI_KEY: str = ''
    MSDS_SHEETS_PATH: str = ''
    MSDS_DOC_HEADING: str = ''
    MAP_DICT: Dict = field(default_factory=dict)
    MODEL_NAME: str = ''
    MODEL_TEMP: float = 0
    GPT_PROMPT: str = ''