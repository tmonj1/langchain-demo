import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownTextSplitter

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

print("Example:")
print(raw_docs[0].page_content)
print("----")
print(chunked_docs[0].page_content)