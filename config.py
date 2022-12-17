from dataclasses import dataclass
from dataclasses_json import dataclass_json
import yaml
import os.path

@dataclass_json
@dataclass
class BotConfig:
    proxy: str
    token: str
    chat_id: str


if os.path.isfile('config.yaml'):
    with open('config.yaml', encoding='utf-8') as f:
        bot_config: BotConfig = BotConfig.from_dict(yaml.full_load((f.read())))
elif os.path.isfile('config.json'):
    with open('config.json', encoding='utf-8') as f:
        bot_config: BotConfig = BotConfig.from_json(f.read())
else:
    s = 'Not found config file config.yaml or config.json'
    print(f'ERROR: {s}')
    raise s

__all__ = [
    'bot_config'
]
