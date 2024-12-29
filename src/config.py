from enum import Enum, auto
from typing import List


class EnvironmentalVariable(Enum):
    OPENAI_API_KEY = auto()
    DOCS_PATH = auto()

# https://platform.openai.com/docs/models/#current-model-aliases
class OpenAIModel(Enum):
    o1 = "o1"
    gpt_4o = "chatgpt-4o-latest"


class DocumentConfig:
    # 複数の拡張子をサポート
    GLOB_PATTERN = "*.*"

    # 除外するパターン
    EXCLUDE_PATTERN = [
        "**/.git/**",  # gitディレクトリを除外
        "**/__pycache__/**",  # pythonキャッシュを除外
        "**/node_modules/**",  # node.jsモジュールを除外
        "**/.env*"  # 環境設定ファイルを除外
    ]

    # ローダーの基本設定
    LOADER_KWARGS = {
        "autodetect_encoding": True,  # エンコーディングの自動検出
        "encoding": "utf-8",  # デフォルトエンコーディング
    }

    # DirectoryLoaderの設定
    LOADER_CONFIG = {
        "recursive": True,  # サブディレクトリも検索
        "silent_errors": True,  # エラーを無視して続行
        "load_hidden": False,  # 隠しファイルは読み込まない
        "use_multithreading": True,  # マルチスレッドを使用
        "max_concurrency": 4,  # 最大スレッド数
        "show_progress": True  # プログレスバーを表示
    }