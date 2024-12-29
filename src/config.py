from enum import Enum, auto


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
        "**/.git/**",
        "**/__pycache__/**",
        "**/node_modules/**",
        "**/.env*",
        "**/venv/**",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
    ]

    # ローダーの基本設定
    LOADER_KWARGS = {
        "autodetect_encoding": True,
        "encoding": "utf-8",
        "encoding_errors": "ignore",
        "fallback_encodings": [
            "utf-8",
            "cp932",
            "shift_jis",
            "euc-jp",
            "iso-2022-jp"
        ]
    }

    # DirectoryLoaderの設定
    LOADER_CONFIG = {
        "recursive": True,
        "silent_errors": True,
        "load_hidden": False,
        "use_multithreading": True,
        "max_concurrency": 4,
        "show_progress": True
    }