import sys
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

#
# 引数の処理
#

# 第1引数から質問を取得
if len(sys.argv) < 2:
    print("引数にLangChainに関する質問を指定してください。")
    exit(1)
question = sys.argv[1]

#
# データベースのロード
#

# データベースファイルのパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "../db/chroma_db")

# OpenAIのEmbeddingsモデルの生成
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Chromaデータベースのロード
db = Chroma(embedding_function=embeddings, persist_directory=db_path)
print(f"Chroma database loaded from '{db_path}'.")

#
# チェーンの構築
#

# Prompt
prompt = ChatPromptTemplate.from_template('''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
''')

# Model
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Retriever
retriever = db.as_retriever()

# Chain
chain = (
    {"question": RunnablePassthrough(), "context": retriever}
    | prompt
    | model
    | StrOutputParser()
)

#
# 実行
#
result = chain.invoke(question)
print(result)