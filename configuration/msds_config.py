from dataclasses import dataclass, field
from yamldataclassconfig.config import YamlDataClassConfig
from typing import List, Dict


@dataclass
class MSDSConfig(YamlDataClassConfig):
    OPENAI_KEY: str = ''
    OPENAI_ENDPOINT: str = ''
    OPENAI_API_VERSION: str = ''
    OPENAI_SEED: int = 123
    MSDS_SHEETS_PATH: str = ''
    MSDS_DOC_HEADING: str = ''
    MAP_DICT: Dict = field(default_factory=dict)
    MODEL_NAME: str = ''
    MODEL_TEMP: float = 0