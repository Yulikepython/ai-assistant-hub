# AI Assistant Hub

LangChainとOpenAIを活用したAIアシスタントアプリケーション。ドキュメント解析とインテリジェントな対話を実現します。

## 機能

- OpenAI GPTモデルとの対話機能
- 環境設定の健全性チェック
- ドキュメント解析とRAG（Retrieval-Augmented Generation）機能

## セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/ai-assistant-hub.git
cd ai-assistant-hub
```

2. 仮想環境の作成と依存関係のインストール:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 環境変数の設定:
`.env`ファイルをプロジェクトルートに作成し、以下の内容を設定:
```
OPENAI_API_KEY=your_api_key_here
```

## 使用方法

1. 健全性チェックの実行:
```bash
python -m src.health_check
```

2. メインアプリケーションの実行:
```bash
python -m src.main
```

## プロジェクト構造

```
ai-assistant-hub/
├── src/
│   ├── __init__.py
│   ├── main.py              # メインアプリケーション
│   ├── config.py            # 設定ファイル
│   ├── health_check.py      # 健全性チェック機能
│   └── document_processor.py # ドキュメント処理機能
├── docs/                    # 処理対象ドキュメント
├── tests/                   # テストファイル
├── .env                     # 環境変数
└── requirements.txt         # 依存関係
```

## 開発環境

- Python 3.9+
- LangChain
- OpenAI GPT

## ライセンス

MIT

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成