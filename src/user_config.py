# src/user_config.py
"""
ユーザー固有の設定ファイル
このファイルで設定を変更することで、アプリケーションの動作をカスタマイズできます。
"""

from src.config import OpenAIModel

# 使用するOpenAIのモデル
# 利用可能なモデルは、config.pyのOpenAIModelを参照してください
MODEL_NAME:str = OpenAIModel.gpt_4o.value

# RAGで使用するドキュメントディレクトリ名（docs/ 以下のディレクトリ名）
DOCS_DIR:str = "default"