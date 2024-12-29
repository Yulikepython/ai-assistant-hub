from langchain_core.messages import HumanMessage, SystemMessage
import os
from typing import Optional

from config import EnvironmentalVariable as Ev


def check_environment() -> tuple[bool, Optional[str]]:
    """環境変数の設定を確認"""
    api_key = os.getenv(Ev.OPENAI_API_KEY.name)
    if not api_key:
        return False, "OpenAI APIキーが設定されていません"
    return True, None


def test_chat_completion(model) -> tuple[bool, Optional[str]]:
    """ChatGPTの基本機能テスト"""
    try:
        messages = [
            SystemMessage(content="あなたは親切なアシスタントです。"),
            HumanMessage(content="こんにちは")
        ]
        response = model.invoke(messages)
        if not response.content:
            return False, "応答が空です"
        return True, response.content
    except Exception as e:
        return False, f"エラーが発生しました: {str(e)}"


def run_health_check(model) -> bool:
    """全ての健全性チェックを実行"""
    print("健全性チェックを開始します...")

    # 環境変数チェック
    env_ok, env_message = check_environment()
    print(f"\n1. 環境変数チェック: {'✓' if env_ok else '✗'}")
    if env_message:
        print(f"   {env_message}")

    # Chat機能チェック
    chat_ok, chat_message = test_chat_completion(model)
    print(f"\n2. Chat完了機能チェック: {'✓' if chat_ok else '✗'}")
    if chat_message:
        print(f"   テスト応答: {chat_message}")

    all_checks_passed = all([env_ok, chat_ok])
    print(f"\n総合結果: {'✓ 全てのチェックに成功しました' if all_checks_passed else '✗ 一部のチェックに失敗しました'}")

    return all_checks_passed