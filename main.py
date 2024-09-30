import argparse

from bot.config import DevelopmentConfig
from bot.run import client_run

envs = {
    'development': DevelopmentConfig,
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Discord Botを起動します。')

    parser.add_argument('-e', '--env', type=str, default='development', help='環境を指定します。', choices=['development', 'production'])

    args = parser.parse_args()

    env = args.env

    if env == 'development':
        config = envs[env]()
        client_run(config)
