from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
import asyncio

from src.health_check import run_health_check
from src.config import EnvironmentalVariable as Ev
from src.document_processor import create_document_processor
from src.user_config import MODEL_NAME, DOCS_DIR

# Envの読み込み
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(ENV_PATH)

# 環境変数の値を取得
OpenAI_KEY = os.getenv(Ev.OPENAI_API_KEY.name)

def get_docs_full_path() -> str:
    """ドキュメントの完全パスを取得"""
    docs_path = os.getenv(Ev.DOCS_PATH.name)
    if not docs_path:
        raise ValueError("DOCS_PATH が環境変数に設定されていません")
    return os.path.join(docs_path, DOCS_DIR)

def create_chat_model():
    """ChatOpenAIモデルのインスタンスを作成"""
    return ChatOpenAI(
        openai_api_key=OpenAI_KEY,
        model_name=MODEL_NAME
    )

async def interactive_qa(processor):
    """対話型Q&A sessionを実行"""
    while True:
        question = input("\n★ 質問を入力してください（終了する場合は 'q' を入力）: ") #ターミナル上で質問を見つけやすく
        if question.lower() == 'q':
            break

        try:
            answer = await processor.ask_question(question)
            print(f"\n★★ 回答: {answer}") #ターミナル上で質問を見つけやすく
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

async def main():
    try:
        # 健全性チェック
        model = create_chat_model()
        if not run_health_check(model):  # 健全性チェックの結果を確認
            print("健全性チェックに失敗しました。プログラムを終了します。")
            return

        # フルパスの取得とディレクトリの存在確認
        docs_full_path = get_docs_full_path()
        print(f"\n使用するドキュメントパス: {docs_full_path}")

        if not os.path.exists(docs_full_path):
            print(f"ディレクトリが存在しません。作成します: {docs_full_path}")
            os.makedirs(docs_full_path, exist_ok=True)

        # ドキュメントの存在確認
        files = os.listdir(docs_full_path)
        print(f"ディレクトリ内のファイル: {files}")

        # ドキュメントプロセッサの初期化
        processor = create_document_processor(docs_full_path)
        processor.setup_qa_chain(model)

        # 対話型Q&Aの実行
        await interactive_qa(processor)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())