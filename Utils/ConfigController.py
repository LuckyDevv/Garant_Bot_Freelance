import yaml
import json
import os
from enum import Enum


class ConfigType(Enum):
    DETECT = 0
    YAML = 1
    JSON = 2
    SERIALIZED = 3
    ENUM = 4


class ConfigController:

    def __init__(self, filename='default.txt', config_type=ConfigType.DETECT, default=None):
        self.filename = filename
        self.config = {}
        self.type = config_type
        self.formats = {
            "json": ConfigType.JSON,
            "js": ConfigType.JSON,
            "yml": ConfigType.YAML,
            "yaml": ConfigType.YAML,
            "sl": ConfigType.SERIALIZED,
            "serialize": ConfigType.SERIALIZED
        }
        self.init(filename, config_type, default or {})

    def init(self, filename, config_type, default):
        self.filename = filename
        self.type = config_type
        if config_type == ConfigType.DETECT:
            self.type = ConfigType.ENUM
            if '.' in filename:
                expansion = filename.split('.')[-1].lower()
                if expansion in self.formats:
                    self.type = self.formats[expansion]

        if not os.path.exists(filename):
            self.config = default
            self.save()
        else:
            with open(filename, 'r') as f:
                content = f.read()
            if self.type == ConfigType.YAML:
                import re
                content = re.sub(r"^( *)([a-zA-Z_] *):$", r'\1"\2":', content, flags=re.MULTILINE)
                self.config = yaml.safe_load(content)
            elif self.type == ConfigType.JSON:
                self.config = json.loads(content)
            elif self.type == ConfigType.SERIALIZED:
                import pickle
                self.config = pickle.loads(content.encode())
            elif self.type == ConfigType.ENUM:
                self.config = dict.fromkeys(self.parse_list(content), True)

            if not isinstance(self.config, dict):
                self.config = default

    def save(self):
        content = ""
        if self.type == ConfigType.YAML:
            content = yaml.dump(self.config, encoding='utf-8', allow_unicode=True)
        elif self.type == ConfigType.JSON:
            content = json.dumps(self.config)
        elif self.type == ConfigType.SERIALIZED:
            import pickle
            content = pickle.dumps(self.config).decode()
        elif self.type == ConfigType.ENUM:
            content = "\n".join(self.config.keys())
        else:
            raise ValueError("An attempt was made to save an unsupported configuration format")

        with open(self.filename, 'w') as f:
            f.write(content)
        return True

    def get_file_name(self):
        return self.filename

    def get(self, key, default=False):
        return self.config.get(key, default)

    def get_all(self, keys=False):
        return list(self.config.keys()) if keys else self.config

    def set(self, key, value=True):
        self.config[key] = value

    def set_all(self, value):
        self.config = value

    def remove(self, key):
        self.config.pop(key, None)

    def exists(self, key):
        return key in self.config

    def parse_list(self, content):
        result = []
        for v in content.replace('\r\n', '\n').strip().split('\n'):
            v = v.strip()
            if v:
                result.append(v)
                self.config[v] = True
        return result
