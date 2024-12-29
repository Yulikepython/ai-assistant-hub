from typing import List, Optional
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
import os

from src.config import DocumentConfig


class DocumentProcessor:
    def __init__(self, docs_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """DocumentProcessorの初期化"""
        self.docs_dir = docs_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store = None
        self.qa_chain = None

    def load_documents(self) -> List:
        """指定ディレクトリからドキュメントを読み込む"""
        try:
            loader = DirectoryLoader(
                path=self.docs_dir,
                glob=DocumentConfig.GLOB_PATTERN,
                exclude=DocumentConfig.EXCLUDE_PATTERN,
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"}
            )

            documents = loader.load()

            if documents:
                print(f"\n読み込み完了: {len(documents)}個のドキュメント")
                self._print_document_summary(documents)
            else:
                print("\n警告: ドキュメントが読み込めませんでした")

            return documents

        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            return []

    def _print_document_summary(self, documents: List) -> None:
        """読み込んだドキュメントの要約を表示"""
        print("\n読み込んだファイル:")
        format_count = {}

        for doc in documents:
            filepath = doc.metadata['source']
            ext = os.path.splitext(filepath)[1].lower()
            format_count[ext] = format_count.get(ext, 0) + 1
            print(f"- {filepath}")

        print("\nファイル形式の集計:")
        for ext, count in format_count.items():
            print(f"- {ext}: {count}ファイル")

    def process_documents(self) -> None:
        """ドキュメントの処理とベクトルストアの作成"""
        documents = self.load_documents()

        if not documents:
            print("処理するドキュメントがありません")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        texts = text_splitter.split_documents(documents)
        print(f"{len(texts)}個のテキストチャンクを作成しました")

        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=OpenAIEmbeddings()
        )
        print("ベクトルストアを作成しました")

    def setup_qa_chain(self, model) -> None:
        """QA chainのセットアップ"""
        if not self.vector_store:
            raise ValueError("先にprocess_documents()を実行してください")

        template = """以下の情報を元に、質問に答えてください:

        コンテキスト: {context}

        質問: {question}

        回答は日本語で、できるだけ詳しく説明してください。"""

        prompt = ChatPromptTemplate.from_template(template)

        self.qa_chain = RetrievalQA.from_chain_type(
            model,
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )

    async def ask_question(self, question: str) -> str:
        """質問に対する回答を生成"""
        if not self.qa_chain:
            raise ValueError("先にsetup_qa_chain()を実行してください")

        response = await self.qa_chain.ainvoke({"query": question})
        return response["result"]


def create_document_processor(docs_dir: str) -> DocumentProcessor:
    """DocumentProcessorのインスタンスを作成して初期化"""
    processor = DocumentProcessor(docs_dir)
    processor.process_documents()
    return processor