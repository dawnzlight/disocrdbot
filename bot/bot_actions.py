
from .utils import extract_changed_files_from_diff


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

def pull_request_summary_action(github, gemini):
    """
    プルリクエストの要約を行う関数
    :param
        github: Github
        gemini: Gemini
    """

    pull_requests = github.get_pull_requests('all-you-can-drink')

    if len(pull_requests) == 0:
        return ['プルリクエストを確認したら、見つからなかったよ。']

    messages = []

    for i, pull_request in enumerate(pull_requests):

        reviewers = github.assign_reviewer('all-you-can-drink', pull_request['number'], pull_request['user']).json()
        reviewers = [github.get_disocrd_member_id(reviewer['login']) for reviewer in reviewers['requested_reviewers']][0]

        response = github.get_diff('all-you-can-drink', pull_request['number']).text
        changed_files = extract_changed_files_from_diff(response)

        prompt = f'{i+1}つ目のプルリクエストの変更ファイルを見て、その内容について要約してください。' + \
        f"5行程度にまとめてください。また回答は「{pull_request['user']}さんからのプルリクだよ。」で始めてください。" \
        '変更があったファイルは以下の通りです。元気よくお願いします！！' + \
        ' '.join([f"{file['file_name']}、追加された行：{file['diff']['plus']}、削除された行：{file['diff']['minus']}" for file in changed_files])

        response = gemini.generate_content(prompt=prompt)

        message = response['candidates'][0]['content']['parts'][0]['text']

        try:
            github.comment_to_pull_request('all-you-can-drink', pull_request['number'], message)
        except Exception as e:
            print(e)

        if len(reviewers) == 0:
            message = message + f"\nURL：{pull_request['html_url']}"
        else:
            message = message + f"\n<@{reviewers}>さん。レビューお願いね！！。" + \
            f"\nURL：{pull_request['html_url']}"
            
        messages.append(message)

    return messages

    