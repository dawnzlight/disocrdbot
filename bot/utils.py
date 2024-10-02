import re


def extract_changed_files_from_diff(diff_output):
    """
    diff 出力から、変更されたファイルの詳細情報を抽出する関数

    Args:
        diff_output (str): diff 出力文字列

    Returns:
        list: 変更ファイルの情報のリスト (JSON形式)
    """

    result = []
    file_info = {}
    
    # diff 出力の一行ずつ処理
    for line in diff_output.splitlines():
        # ファイル名の抽出
        match = re.match(r"diff --git a/(.+)\sb/(.+)", line)
        if match:
            if file_info:
                result.append(file_info)
            file_info = {"file_name": match.group(2), "diff": {"plus": '', "minus": ''}}
        
        # 変更行の抽出
        elif line.startswith("+ "):
            file_info["diff"]["plus"] += line[1:].strip() + ' '
        elif line.startswith("- "):
            file_info["diff"]["minus"] += line[1:].strip() + ' '

    # 最後のファイルの情報を追加
    if file_info:
        result.append(file_info)

    return result