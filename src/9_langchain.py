import os
import tkinter as tk
from tkinter import ttk
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# スクリプトがあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データベースの保存先
db_path = os.path.normpath(os.path.join(script_dir, "../db/chroma_db"))

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
        self.db_label = tk.Label(frame, text=f"Database File: {db_path}")
        self.db_label.pack(anchor='w')

        # コレクション名の表示
        self.db_label = tk.Label(frame, text=f"Collection: {chroma_db._collection_name}")
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

        # キーイベントのバインド
        self.entry.bind("<Up>", self.increment_entry)
        self.entry.bind("<Down>", self.decrement_entry)
        self.entry.bind("<Return>", lambda event: self.search_document())  # Enterキーのバインド
        self.entry.bind("<KeyRelease>", lambda event: self.search_document())  # キーリリースイベントのバインド

        # 区切り線
        separator = ttk.Separator(frame, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=10)

        # ドキュメントIDの表示
        frame_doc_id = tk.Frame(frame)
        frame_doc_id.pack(anchor='w', fill='x')
        self.doc_id_label = tk.Label(frame_doc_id, text="Document ID: ")
        self.doc_id_label.pack(side='left')
        self.doc_id_var = tk.StringVar(value="-")
        self.doc_id_entry = tk.Entry(
            frame_doc_id,
            textvariable=self.doc_id_var,
            state="readonly",
            width=20,
            justify='left')
        self.doc_id_entry.pack(side='left', fill='x', expand=True)

        # 埋め込みの表示
        frame_embedding = tk.Frame(frame)
        frame_embedding.pack(anchor='w', fill='x')
        self.embedding_dimension_var = tk.StringVar(value="Embbeding (Array)")
        self.embedding_label = tk.Label(frame_embedding, textvariable=self.embedding_dimension_var)
        self.embedding_label.pack(side='left')
        self.embedding_var = tk.StringVar(value="-")
        self.embedding_entry = tk.Entry(
            frame_embedding,
            textvariable=self.embedding_var,
            state="readonly",
            width=20,
            justify='left')
        self.embedding_entry.pack(side='left', fill='x', expand=True)

        # テキスト長の表示
        frame_result_length = tk.Frame(frame)
        frame_result_length.pack(anchor='w')
        self.result_length_label = tk.Label(frame_result_length, text="Result Length:")
        self.result_length_label.pack(side='left')
        self.result_length_var = tk.StringVar(value="0")
        self.result_length_entry = tk.Entry(
            frame_result_length,
            textvariable=self.result_length_var,
            state="readonly",
            width=10,
            justify='left')
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

        # データが存在する場合は最初のドキュメントを表示
        if len(doc_ids) > 0:
            self.entry.insert(0, "0")
            self.search_document()

    def validate_entry(self, new_value: str | int):
        # 値更新時、いったん空文字列になる場合があるのでTrueを返す
        if new_value == "":
            return True

        if isinstance(new_value, str):
            if new_value.isdigit():
                n = int(new_value)
            else:
                return False
        else:
            n = new_value

        if n >= 0 and n < len(doc_ids):
            return True
        else:
            return False

    def increment_entry(self, event):
        current_value = self.entry.get()
        if current_value.isdigit():
            new_value = int(current_value) + 1
            if self.validate_entry(new_value):
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(new_value))
                self.search_document()

    def decrement_entry(self, event):
        current_value = self.entry.get()
        if current_value.isdigit():
            new_value = int(current_value) - 1
            if self.validate_entry(new_value):
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(new_value))
                self.search_document()

    def update_readonly_entry(self, entry: tk.Entry, entry_var: tk.StringVar, value):
        entry.config(state="normal")  # 一時的に書き込み可能にする
        entry_var.set(value)
        entry.config(state="readonly")  # 再び読み取り専用にする

    def update_label_var(self, label_var: tk.StringVar, value):
        label_var.set(value)

    def search_document(self):
        try:
            # 空文字列のときは何もしない
            if not self.entry.get():
                return

            doc_number = int(self.entry.get())
            if 0 <= doc_number < len(doc_ids):
                text = data['documents'][doc_number]
                embedding = data['embeddings'][doc_number]
                result_text = text
                result_embedding_dimension = len(embedding)
                result_embedding = embedding[:10]
            else:
                result = "Document not found."
        except ValueError:
            result = "Please enter a valid number."
        except Exception as e:
            result = f"Error: {str(e)}"
        
        # ドキュメントIDの更新
        self.update_readonly_entry(
            self.doc_id_entry,
            self.doc_id_var,
            f"{doc_ids[doc_number]}")

        # 埋め込みの更新
        self.update_label_var(
            self.embedding_dimension_var,
            f"Embedding ({result_embedding_dimension})")
        self.update_readonly_entry(
            self.embedding_entry,
            self.embedding_var,
            f"{", ".join(map(str, result_embedding))}")

        # 検索結果テキストのテキスト長の更新
        self.update_readonly_entry(
            self.result_length_entry,
            self.result_length_var,
            f"{len(result_text)}")
        
        # 検索結果テキストの更新
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = ChromaApp(root)
    app.initialLayout()
    root.mainloop()