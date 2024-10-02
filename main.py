import argparse
import asyncio

import discord
from discord.ext import commands

from bot.bot_actions import pull_request_summary_action, voice_channel_in_and_out_send
from bot.config import DevelopmentConfig, ProductionConfig
from bot.gemini_api import Gemini
from bot.github_api import Github

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
    client = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)
    intents.message_content = True

    gemini = Gemini(config)
    github = Github(config)

    # Botの起動処理
    @client.event
    async def on_ready():
        print(f'Bot is ready as {client.user}')
        await client.tree.sync()


    # チャンネル入退室時の通知処理
    @client.event
    async def on_voice_state_update(member, before, after):
        await voice_channel_in_and_out_send(member, before, after, client, config)
    
    if env == 'development':
        @client.command()
        async def sakura(ctx, prompt):
            user = ctx.author
            async with ctx.typing():
                response = gemini.generate_content(prompt=f"ちなみに私とは{user}のことです。"+prompt, category='question')
                message = response['candidates'][0]['content']['parts'][0]['text']
                await ctx.send(message)

    if env == 'production':
        @client.command()
        async def shizuku(ctx, prompt):
            user = ctx.author
            async with ctx.typing():
                response = gemini.generate_content(prompt=f"ちなみに私とは{user}のことです。"+prompt, category='question')
                message = response['candidates'][0]['content']['parts'][0]['text']
                await ctx.send(message)

    @client.command()
    async def pull_request_summary(ctx):
        async with ctx.typing():
            messages = pull_request_summary_action(github, gemini)
            for message in messages:
                await ctx.send(message)

    if env == 'development':
        client.run(config.get_discord_bot_token())

    if env == 'production':
        async def main():
            try:
                await client.start(config.get_discord_bot_token())
            except KeyboardInterrupt:
                await client.close()
            finally:
                await asyncio.sleep(0.1)
        
        asyncio.run(main())