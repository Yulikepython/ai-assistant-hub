# AI Assistant Hub

AI Assistant Hub は LangChain と OpenAI を活用した RAG（Retrieval-Augmented Generation）ベースの AI アシスタントアプリケーションです。ドキュメント解析と高度な対話機能を提供します。

## 主な機能

- 🤖 OpenAI GPT モデルを活用した高度な対話機能
- 📚 複数形式のドキュメント解析とインデックス化
- 🔍 RAG（Retrieval-Augmented Generation）による的確な回答生成
- ⚡ 非同期処理による効率的な応答
- 🛡️ 包括的な健全性チェックシステム

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

3. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

4. 環境変数の設定:
src内の `.env.sample`をコピーして、`.env` ファイルを作成。以下の変数に正しい値を入れます。:
```env
OPENAI_API_KEY=your_api_key_here
DOCS_PATH=/path/to/your/documents
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

3. 対話の開始:
- プロンプトが表示されたら、質問を入力してください
- 終了するには 'q' を入力してください

## 開発者向け情報

### プロジェクト構造

```
ai-assistant-hub/
├── src/
│   ├── __init__.py
│   ├── .env.sample          # 環境変数のサンプル
│   ├── .env                 # サンプルから自身で作成してください
│   ├── main.py              # メインアプリケーション
│   ├── config.py            # 設定ファイル
│   ├── health_check.py      # 健全性チェック機能
│   └── document_processor.py # ドキュメント処理機能
├── tests/
│   └── test_ai_assistant.py # テストスイート
├── docs/                    # 処理対象ドキュメント
└── requirements.txt         # 依存関係
```

### テストの実行

基本的なテスト実行:
```bash
python -m pytest tests/test_ai_assistant.py -v
```

カバレッジレポートの取得:
```bash
# 基本的なカバレッジレポート
python -m pytest --cov=src tests/test_ai_assistant.py

# 未カバー行を表示する詳細レポート
python -m pytest --cov=src --cov-report=term-missing tests/test_ai_assistant.py

# HTMLレポートの生成
python -m pytest --cov=src --cov-report=html tests/test_ai_assistant.py
```

### ドキュメント処理の設定

`config.py` で以下の設定をカスタマイズできます：
- 対応するファイル形式
- 除外パターン
- チャンクサイズとオーバーラップ
- 並行処理の設定

## トラブルシューティング

1. OpenAI API エラー:
   - API キーが正しく設定されているか確認
   - 環境変数が適切に読み込まれているか確認

2. ドキュメント読み込みエラー:
   - ファイルパスが正しく設定されているか確認
   - ファイルのエンコーディングを確認
   - アクセス権限を確認

3. メモリエラー:
   - チャンクサイズの調整を検討
   - 処理対象ドキュメントの量を確認

## 貢献方法

1. このリポジトリをフォーク
2. 新しい機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## サポートと連絡先

- Issue Tracker: https://github.com/Yulikepython/ai-assistant-hub/issues
- メール: developer@itc.tokyo

## 謝辞

- OpenAI - GPTモデルの提供
- LangChain - フレームワークの提供
- すべてのコントリビューター