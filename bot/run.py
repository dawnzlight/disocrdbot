import discord


def client_run(config):
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    client.run(config.get_discord_bot_token())