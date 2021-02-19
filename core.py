import json
import os


class AppCore():
    def __init__(self) -> None:
        self.CONFIG_PATH = 'config.json'
        self.config = self.getConfig()

    def getConfig(self) -> dict:
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, 'r', encoding='UTF-8') as f:
                config: dict = json.load(f)
                return config
        return {}

    def setConfig(self, config: dict):
        with open(self.CONFIG_PATH, 'w', encoding='UTF-8') as f:
            json.dump(config, f, indent=4)

    def getDBPath(self) -> str:
        if 'dbPath' in self.config.keys():
            return self.config['dbPath']
        return None

    def setDBPath(self, path: str):
        self.config['dbPath'] = path
        self.setConfig(self.config)


if __name__ == '__main__':
    core = AppCore()
    print(core.getConfig())