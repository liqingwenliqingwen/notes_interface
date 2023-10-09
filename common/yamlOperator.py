import yaml

from main import DIR, ENVIRON


class YamlOperator:
    @staticmethod
    def env_config():
        """环境配置读取"""
        with open(file=DIR + f'/envConfig/{ENVIRON}/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def api_data_config(api):
        """接口数据读取"""
        with open(file=DIR + f'/data/{api}/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
