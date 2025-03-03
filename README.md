# langchain-demo

LangChainの学習に作ったサンプルプログラムです。

## 実行環境

* Python 3.12 で実行確認
* 環境変数`OPENAI_API_KEY`にOpenAIのAPIキーを設定して実行すること
* OSXの場合、事前に `brew install libmagic` で `libmagic` をインストールしてください

## ファイルの説明

ファイル | 説明
:--|:--
1_langchain.py | OpenAIのChatモデルを使ってみる (OpenAI)
2_langchain.py | DocumentLoaderを使ってみる (DirectoryLoader)
3_langchain.py | Splitterを使ってみる (MarkdownTextSplitter)
4_langchain.py | OpenAIのEmbeddingモデルを使ってみる (OpenAIEmbeddings)
5_langchain.py | Vector DBのChromaを使ってみる (Chroma, Retriever)
6_langchain.py | ChromaDBのデータベースの永続化 (Chroma, Loader)
7_langchain.py | ChromaDBのデータベースのロード (Chroma, Loader)
8_langchain.py | Simple RAG (LCEL) ※ 6を実行してChromaのデータベースを作成しておくこと

