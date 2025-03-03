import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")

# スクリプトがあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# スクリプトのあるディレクトリを基準に相対パスを作成
directory_path = os.path.join(script_dir, "../docs")

# ディレクトリ内のファイルを読み込む
loader = DirectoryLoader(
    path = directory_path,
    glob = "**/*.mdx"
)

raw_docs = loader.load()
print(f"number of raw docs = {len(raw_docs)}")

# テキストをチャンク化
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)

chunked_docs = text_splitter.split_documents(raw_docs)
print(f"number of chunks = {len(chunked_docs)}")

# OpenAIのEmbeddingsモデルの生成
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# データベースの保存先
db_path = os.path.join(script_dir, "../db/chroma_db")

# すでにデータベースがあれば削除
if os.path.exists(db_path):
    shutil.rmtree(db_path)
    print("Old Chroma database removed.")

# Chromaデータベースの作成と保存
chroma_db = Chroma(embedding_function=embeddings, persist_directory=db_path)
chroma_db.add_documents(chunked_docs)
print(f"Chroma database created and saved to '{db_path}'.")