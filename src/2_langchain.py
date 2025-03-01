import os
from langchain_community.document_loaders import DirectoryLoader

def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")

# スクリプトがあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# スクリプトのあるディレクトリを基準に相対パスを作成
directory_path = os.path.join(script_dir, "../docs")

loader = DirectoryLoader(
    path = directory_path,
    glob = "**/*.mdx"
)

raw_docs = loader.load()
print(len(raw_docs))