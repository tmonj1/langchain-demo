import os
import tkinter as tk
from tkinter import messagebox
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
    persist_directory=db_path)

# 全てのドキュメントを取得
data = chroma_db.get(
    include=["metadatas", "embeddings", "documents"])

# 全てのドキュメントのIDを取得
doc_ids = data["ids"]

# GUIの作成
class ChromaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chroma Database Viewer")

        # データベースファイル名の表示
        self.db_label = tk.Label(root, text=f"Database File: {os.path.basename(db_path)}")
        self.db_label.pack()

        # データの総件数の表示
        self.count_label = tk.Label(root, text=f"Total Documents: {len(doc_ids)}")
        self.count_label.pack()

        # 番号指定用のテキストボックス
        self.entry_label = tk.Label(root, text="Enter Document Number:")
        self.entry_label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()

        # 検索ボタン
        self.search_button = tk.Button(root, text="Search", command=self.search_document)
        self.search_button.pack()

        # 結果表示用のテキストボックス
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack()

    def search_document(self):
        try:
            doc_number = int(self.entry.get())
            if 0 <= doc_number < len(doc_ids):
                doc_id = doc_ids[doc_number]
                text = data['documents'][doc_number]
                embedding = data['embeddings'][doc_number]
                result = f"Text: {text}\nLength: {len(text)}\nEmbedding (first 10 elements): {embedding[:10]}"
                #result = f"Text: {text}\nLength: {len(text)}\n"
            else:
                result = "Document not found."
        except ValueError:
            result = "Please enter a valid number."
        except Exception as e:
            result = f"Error: {str(e)}"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChromaApp(root)
    root.mainloop()