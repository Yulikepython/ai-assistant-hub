# AI Assistant Hub

AI Assistant Hub は LangChain と OpenAI を活用した RAG（Retrieval-Augmented Generation）ベースの AI アシスタントアプリケーションです。ドキュメント解析と高度な対話機能を提供します。

## 主な機能

- 🤖 OpenAI GPT モデルを活用した高度な対話機能
- 📚 複数形式のドキュメント解析とインデックス化
- 🔍 RAG（Retrieval-Augmented Generation）による的確な回答生成
- ⚡ 非同期処理による効率的な応答
- 🛡️ 包括的な健全性チェックシステム
- ⚙️ 簡単なカスタマイズ設定

## システム要件

- Python 3.9+
- OpenAI API キー
- 十分なストレージ容量（ベクトルストア用）

## インストール方法

1. リポジトリのクローン:
```bash
git clone https://github.com/Yulikepython/ai-assistant-hub.git
cd ai-assistant-hub
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

3. パッケージのインストール:
```bash
pip install -r requirements.txt  # 依存パッケージのインストール
pip install -e .  # 開発モードでプロジェクトをインストール
```

4. 環境変数の設定:
`.env.sample` をコピーして `.env` ファイルを作成し、以下の変数を設定:
```env
OPENAI_API_KEY=your_api_key_here
DOCS_PATH=/path/to/your/documents
```
★重要★ **DOCS_PATHはcloneした環境内のdocsディレクトリを指定してください。**

コマンドにより読み取るディレクトリは、この中に設置します。（デフォルトでは、"default"がサンプルとして入っています。）

5. アプリケーション設定の確認:
`src/user_config.py` で使用するモデルとドキュメントディレクトリを設定できます:
```python
from src.config import OpenAIModel

# 使用するOpenAIのモデル
MODEL_NAME = OpenAIModel.gpt_4o.value  # または OpenAIModel.o1.value

# RAGで使用するドキュメントディレクトリ名
DOCS_DIR = "your_docs_directory"  # docs/ 以下に作成した実際に読み取るファイルが入っているディレクトリ名
```

## 使用方法

アプリケーションは以下のいずれかの方法で実行できます：

### 方法1: モジュールとして実行
```bash
python -m src.main
```

### 方法2: コマンドラインツールとして実行（インストール後）
```bash
ai-assistant
```

プログラムを起動すると：
1. 健全性チェックが実行されます
2. 指定されたドキュメントディレクトリが確認・作成されます
3. 対話型インターフェースが起動します
   - 質問を入力してEnterキーを押してください
   - 終了するには 'q' を入力してください

"default"ディレクトリを指定している場合、以下の質問を入力することで、正しくファイルが読み取れているかを書くにできます。
```text
各ファイルの秘密キーを抜き出してください。
```
以下のような回答が得られれば、正しくファイルは読み取れています。
```text
- **テキストファイルの秘密キーワード**: 「test-itc-api-assistant-txt-file-key」
- **Markdownファイルの秘密キーワード**: 「test-secret-keyword-for-md-file」

```
生成AIで動的に回答が作られているため、多少文面等には違いがあるかもしれませんが、秘密キーワードが含まれていることを確認してください。

## プロジェクト構造

```
ai-assistant-hub/
├── src/
│   ├── __init__.py         # バージョン情報
│   ├── main.py             # メインアプリケーション
│   ├── config.py           # 基本設定
│   ├── user_config.py      # ユーザー設定
│   ├── document_processor.py # ドキュメント処理
│   └── health_check.py     # 健全性チェック
├── tests/                  # テストスイート
├── docs/                   # 処理対象ドキュメント
├── .env.sample            # 環境変数サンプル
├── .env                   # 環境変数（作成必要）
├── requirements.txt       # 依存関係
├── pyproject.toml        # プロジェクト設定
└── README.md
```

## 開発者向け情報

### テストの実行

```bash
# 基本的なテスト実行
pytest tests/test_ai_assistant.py -v

# カバレッジレポート
pytest --cov=src tests/test_ai_assistant.py

# 詳細なカバレッジレポート
pytest --cov=src --cov-report=term-missing tests/test_ai_assistant.py

# HTMLカバレッジレポート
pytest --cov=src --cov-report=html tests/test_ai_assistant.py
```

### カスタマイズ可能な設定

1. `src/config.py`：
   - 基本設定（環境変数、モデル、ドキュメント処理）
   - 除外パターン
   - ローダー設定

2. `src/user_config.py`：
   - 使用するGPTモデル
   - ドキュメントディレクトリ

3. `src/document_processor.py`：
   - チャンクサイズ
   - オーバーラップ設定
   - プロンプトテンプレート

## トラブルシューティング

1. インポートエラー:
   - 仮想環境が有効化されているか確認
   - `pip install -e .` が正常に完了しているか確認
   - PYTHONPATH が正しく設定されているか確認

2. OpenAI API エラー:
   - API キーが正しく設定されているか確認
   - `.env` ファイルが正しい場所にあるか確認
   - 環境変数が読み込まれているか確認

3. ドキュメント読み込みエラー:
   - `DOCS_PATH` が正しく設定されているか確認
   - 指定ディレクトリのアクセス権限を確認
   - ファイルのエンコーディングを確認

4. メモリ関連の問題:
   - チャンクサイズの調整
   - 処理対象ドキュメント数の確認
   - システムリソースの確認

## ライセンスと謝辞

- MIT ライセンスで公開（詳細は [LICENSE](LICENSE) を参照）
- OpenAI GPTモデル使用
- LangChain フレームワーク活用

## サポートと連絡先

- バグ報告: [Issue Tracker](https://github.com/Yulikepython/ai-assistant-hub/issues)
- 連絡先: developer@itc.tokyo