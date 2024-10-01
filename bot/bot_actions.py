async def voice_channel_in_and_out_send(member, before, after, client, config):
    """
    ボイスチャンネルに入退室した際に通知を行う関数
    :param
        member: discord.Member
        before: discord.VoiceState
        after: discord.VoiceState
        client: discord.Client
        config: Config
    """

    # 通知メッセージを書き込むチャンネルを取得（チャンネルIDを指定）
    text_channel_in_and_out_send = client.get_channel(int(config.get_text_channel('notification')))

    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        # 入室時の処理
        if after.channel is not None:
            await text_channel_in_and_out_send.send(f'{member.name} が {after.channel.name} に入室したよ。')
        # 退室時の処理
        elif before.channel is not None:
            await text_channel_in_and_out_send.send(f'{member.name} が {before.channel.name} から退室したよ。')
    