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

    def initialLayout(self):
        root = self.root
        
        # ウィンドウのタイトルを設定
        root.title("Chroma Database Viewer")

        # スクリーンサイズを取得
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # ウィンドウの初期サイズをスクリーンサイズの70%に設定
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)
        root.geometry(f"{window_width}x{window_height}")

        # Frame を使ってマージンを確保
        frame = tk.Frame(self.root, padx=20, pady=20)  # 余白を設定
        frame.pack(fill="both", expand=True)

        # データベースファイル名の表示
        self.db_label = tk.Label(frame, text=f"Database File: {os.path.basename(db_path)}")
        self.db_label.pack(anchor='w')

        # データの総件数の表示
        self.count_label = tk.Label(frame, text=f"Total Documents: {len(doc_ids)}")
        self.count_label.pack(anchor='w')

        # 番号指定用のテキストボックス
        frame_number_entry = tk.Frame(frame)
        frame_number_entry.pack(anchor='w')
        self.entry_label = tk.Label(frame_number_entry, text="Enter Document Number:")
        self.entry_label.pack(side='left')
        vcmd = (root.register(self.validate_entry), '%P')
        self.entry = tk.Entry(
            frame_number_entry,
            validate='key',
            validatecommand=vcmd,
            width=5,
            justify='right')
        self.entry.pack(side='left', fill='x', expand=True)

        # 検索ボタン
        self.search_button = tk.Button(frame, text="Search", command=self.search_document)
        self.search_button.pack(side='top', anchor='w')
        
        # テキスト長の表示
        frame_result_length = tk.Frame(frame)
        frame_result_length.pack(anchor='w')
        self.result_length_label = tk.Label(frame_result_length, text="Result Length:")
        self.result_length_label.pack(side='left')
        self.result_length = tk.StringVar(value="0")
        self.result_length_entry = tk.Entry(
            frame_result_length,
            textvariable=self.result_length,
            state="readonly",
            width=10,
            justify='right')
        self.result_length_entry.pack(side='left', fill='x', expand=True)

        # 結果表示用のテキストボックス
        frame_search_result = tk.Frame(frame)
        frame_search_result.pack(anchor='w', fill='both', expand=True)
        self.result_text_label = tk.Label(frame_search_result, text="Search Result:")
        self.result_text_label.pack(side='left', anchor='n')
        self.result_text = tk.Text(frame_search_result, height=10, width=50, wrap='word')
        self.result_text.pack(side='left', fill='both', expand=True)

        # 縦スクロールバーの追加
        self.scrollbar = tk.Scrollbar(self.result_text, command=self.result_text.yview)
        self.scrollbar.pack(side='right', fill='y')

        # テキストボックスにスクロールバーを設定
        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def validate_entry(self, new_value):
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False

    def update_readonly_entry(self, entry: tk.Entry, entry_var: tk.StringVar, value):
        entry.config(state="normal")  # 一時的に書き込み可能にする
        entry_var.set(value)
        entry.config(state="readonly")  # 再び読み取り専用にする

    def search_document(self):
        try:
            doc_number = int(self.entry.get())
            if 0 <= doc_number < len(doc_ids):
                doc_id = doc_ids[doc_number]
                text = data['documents'][doc_number]
                embedding = data['embeddings'][doc_number]
                result_text = text
                result_embedding = embedding[:10]
            else:
                result = "Document not found."
        except ValueError:
            result = "Please enter a valid number."
        except Exception as e:
            result = f"Error: {str(e)}"
        
        self.update_readonly_entry(
            self.result_length_entry,
            self.result_length,
            f"{len(result_text)}")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
    
# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = ChromaApp(root)
    app.initialLayout()
    root.mainloop()