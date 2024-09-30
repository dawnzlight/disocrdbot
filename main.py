import argparse
import asyncio

import discord

from bot.bot_actions import voice_channel_in_and_out_send
from bot.config import DevelopmentConfig, ProductionConfig

envs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Discord Botを起動します。')
    parser.add_argument('-e', '--env', type=str, default='development', help='環境を指定します。', choices=['development', 'production'])

    args = parser.parse_args()
    env = args.env

    config = envs[env]()

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    intents.message_content = True

    # Botの起動処理
    @client.event
    async def on_ready():
        print(f'Bot is ready as {client.user}')


    # チャンネル入退室時の通知処理
    @client.event
    async def on_voice_state_update(member, before, after):
        await voice_channel_in_and_out_send(member, before, after, client, config)


    async def main():
        try:
            await client.start(config.get_discord_bot_token())
        except KeyboardInterrupt:
            await client.close()
        finally:
            await asyncio.sleep(0.1)

    asyncio.run(main())
