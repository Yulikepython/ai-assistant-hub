import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.messages import SystemMessage, HumanMessage

from src.document_processor import DocumentProcessor, create_document_processor
from src.health_check import check_environment, check_chat_completion, run_health_check
from src.config import EnvironmentalVariable as Env


@pytest.fixture(autouse=True)
def mock_openai_env():
    """OpenAI環境変数のモック"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy_key'}):
        yield


@pytest.fixture
def mock_model():
    """Chat モデルのモック"""
    model = Mock()
    model.invoke.return_value = Mock(content="Test response")
    return model


class TestDocumentProcessor:
    @pytest.fixture
    def temp_docs_dir(self):
        # テスト用の一時ディレクトリを作成
        temp_dir = tempfile.mkdtemp()

        # テスト用のファイルを作成
        test_files = {
            'test1.txt': 'This is test document 1.',
            'test2.md': '# Test Document 2\nThis is a markdown file.',
            'subfolder/test3.txt': 'This is test document 3 in a subfolder.'
        }

        for filepath, content in test_files.items():
            full_path = os.path.join(temp_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

        yield temp_dir
        # テスト後にディレクトリを削除
        shutil.rmtree(temp_dir)

    def test_load_documents(self, temp_docs_dir):
        processor = DocumentProcessor(temp_docs_dir)
        documents = processor.load_documents()

        # ドキュメントが正しく読み込まれているか確認
        assert len(documents)==3
        # メタデータが正しく設定されているか確認
        assert all('source' in doc.metadata for doc in documents)

    @pytest.mark.asyncio
    async def test_ask_question(self):
        with patch('langchain_community.vectorstores.Chroma.from_documents') as mock_chroma:
            # モックの設定
            mock_qa_chain = AsyncMock()
            mock_qa_chain.ainvoke.return_value = {"result": "Test answer"}

            processor = DocumentProcessor("dummy_path")
            processor.qa_chain = mock_qa_chain

            # 質問と回答のテスト
            result = await processor.ask_question("Test question")
            assert result=="Test answer"
            mock_qa_chain.ainvoke.assert_called_once()

    def test_create_document_processor(self, temp_docs_dir):
        with patch('src.document_processor.OpenAIEmbeddings', autospec=True) as mock_embeddings, \
                patch('langchain_community.vectorstores.Chroma.from_documents') as mock_chroma:
            processor = create_document_processor(temp_docs_dir)
            assert isinstance(processor, DocumentProcessor)
            assert processor.docs_dir==temp_docs_dir
            mock_embeddings.assert_called_once()


class TestHealthCheck:
    def test_check_environment_with_api_key(self):
        with patch.dict(os.environ, {Env.OPENAI_API_KEY.name: 'dummy_key'}):
            result, message = check_environment()
            assert result is True
            assert message is None

    def test_check_environment_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            result, message = check_environment()
            assert result is False
            assert "OpenAI APIキー" in message

    def test_chat_completion_check_success(self, mock_model):
        result, message = check_chat_completion(mock_model)
        assert result is True
        assert message=="Test response"

        # 正しいメッセージが送られたか確認
        called_messages = mock_model.invoke.call_args[0][0]
        assert isinstance(called_messages[0], SystemMessage)
        assert isinstance(called_messages[1], HumanMessage)

    def test_chat_completion_check_failure(self, mock_model):
        mock_model.invoke.side_effect = Exception("API Error")

        result, message = check_chat_completion(mock_model)
        assert result is False
        assert "エラー" in message

    def test_run_health_check_success(self, mock_model):
        with patch.dict(os.environ, {Env.OPENAI_API_KEY.name: 'dummy_key'}):
            result = run_health_check(mock_model)
            assert result is True

    def test_run_health_check_failure(self, mock_model):
        mock_model.invoke.side_effect = Exception("API Error")

        with patch.dict(os.environ, {}, clear=True):
            result = run_health_check(mock_model)
            assert result is False


class TestMain:
    def test_get_docs_full_path(self):
        from src.main import get_docs_full_path

        with patch.dict(os.environ, {'DOCS_PATH': '/test/path'}):
            result = get_docs_full_path()
            assert result==os.path.join('/test/path', 'default')

    def test_get_docs_full_path_error(self):
        from src.main import get_docs_full_path

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="DOCS_PATH が環境変数に設定されていません"):
                get_docs_full_path()

    def test_create_chat_model(self):
        from src.main import create_chat_model

        with patch.dict(os.environ, {Env.OPENAI_API_KEY.name: 'dummy_key'}):
            model = create_chat_model()
            assert model is not None
            assert hasattr(model, 'invoke')


if __name__=='__main__':
    pytest.main([__file__])