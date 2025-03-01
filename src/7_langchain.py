import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pydantic_settings import ForceDecode

# スクリプトがあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データベースの保存先
db_path = os.path.join(script_dir, "../db/chroma_db")

# OpenAIのEmbeddingsモデルの生成
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Chromaデータベースのロード
chroma_db = Chroma(embedding_function=embeddings, persist_directory=db_path)
print(f"Chroma database loaded from '{db_path}'.")

# データベースの内容を確認
print(f"doc count= {chroma_db._collection.count()}")