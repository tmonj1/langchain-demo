import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# スクリプトがあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データベースの保存先
db_path = os.path.join(script_dir, "../db/chroma_db")

# OpenAIのEmbeddingsモデルの生成
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Chromaデータベースのロード
chroma_db = Chroma(
    collection_name="default",
    embedding_function=embeddings,
    persist_directory=db_path
)
print(f"Chroma database loaded from '{db_path}'.")

query = "What is LangChain?"

results = chroma_db.similarity_search_with_score(
    query=query,
    k=3
)

print(f"Query: '{query}'")
print("Results:")
for i, (doc, score) in enumerate(results):
    print(f"{i+1}: score: {score:4f}, docId: {doc.id[:8]}, text: {doc.page_content[:25]}..")
