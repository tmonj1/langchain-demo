import os
import tkinter as tk
from tkinter import ttk, filedialog
from attr import AttrsInstance, attributes
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
        self.db_path = db_path
        
        # ウィンドウのタイトルを設定
        root.title("Chroma Database Viewer")

        # メニューバーの作成
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Fileメニューの作成
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.open_chroma_database)

        # スクリーンサイズを取得
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # ウィンドウの初期サイズをスクリーンサイズの70%に設定
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)
        root.geometry(f"{window_width}x{window_height}")

        #
        # 上段のフレーム
        #

        # Frame を使ってマージンを確保
        frame_top = tk.Frame(self.root, height=30, padx=10, pady=0)  # 余白を設定
        frame_top.pack(fill="x")
        frame_top.pack_propagate(True)

        # フレームのカラムを設定（ラベルの幅を統一）
        frame_top.columnconfigure(0, minsize=100)  # ラベル列の幅を100pxに固定
        frame_top.columnconfigure(1, weight=1)  # Entry をウィンドウ幅に応じて拡張

        # ラベルとテキストボックスを配置
        label_texts = [
            "Database File:",
            "Collection:",
            "Total Documents:",
            "Enter Document Number:"
        ]
        entry_attributes = [
            {"state": "readonly", "stickey": "ew", "value": f"{db_path}"},
            {"state": "readonly", "stickey": "ew", "value": f"{chroma_db._collection_name}"},
            {"state": "readonly", "stickey": "w",  "value": f"{len(doc_ids)}"},
            {"state": "normal",   "stickey": "w",  "value": ""}
        ]
        entries = []

        for i, label_text in enumerate(label_texts):
            label = tk.Label(frame_top, text=label_text, anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=0)

            attributes = entry_attributes[i]
            entry = tk.Entry(
                frame_top,
                textvariable=tk.StringVar(value=attributes["value"]),
                state=attributes["state"])
            entry.grid(row=i, column=1, sticky=attributes["stickey"], padx=5, pady=0)
            entries.append(entry)

        doc_number_entry = entries[-1]
        self.entry = doc_number_entry

        # キーイベントのバインド
        self.entry.bind("<Up>", self.increment_entry)
        self.entry.bind("<Down>", self.decrement_entry)
        self.entry.bind("<Return>", lambda event: self.search_document())  # Enterキーのバインド
        self.entry.bind("<KeyRelease>", lambda event: self.search_document())  # キーリリースイベントのバインド

        #
        # 中段のフレーム
        #
        frame_middle = tk.Frame(self.root, padx=10, pady=0)
        frame_middle.pack(fill="x")

        ## 区切り線
        separator = ttk.Separator(frame_middle, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)

        #
        # 下段のフレーム
        #
        frame_bottom = tk.Frame(self.root, padx=10, pady=0)
        frame_bottom.pack(fill="both", expand=True)

        # フレームのカラムを設定（ラベルの幅を統一）
        frame_top.columnconfigure(0, minsize=100)  # ラベル列の幅を100pxに固定
        frame_top.columnconfigure(1, weight=1)  # Entry をウィンドウ幅に応じて拡張

        label_texts2 = [
            "Document ID:",
            "Embedding:",
            "Result Length:",
            "Search Result:"
        ]

        entry_attributes2 = [
            {"state": "readonly", "stickey": "w", "value": "-"},
            {"state": "readonly", "stickey": "w", "value": "-"},
            {"state": "readonly", "stickey": "w", "value": "0"},
            {"state": "readonly", "stickey": "w", "value": ""}
        ]
        entries2 = []

        for i, label_text in enumerate(label_texts2):
            label = tk.Label(frame_bottom, text=label_text, anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=0)

            attributes = entry_attributes2[i]
            entry = tk.Entry(
                frame_bottom,
                textvariable=tk.StringVar(value=attributes["value"]),
                state=attributes["state"])
            entry.grid(row=i, column=1, sticky=attributes["stickey"], padx=5, pady=0)
            entries2.append(entry)



        #$$$ Todo's
        #* frame_topはDBが変わったときに更新するようにする
        #  * update_database_frame(db_info) みたいな関数を作って、それを呼ぶようにする
        #* frame_bottomはdoc_number_entryが変わったときに更新するようにする
        #  * update_document_frame(doc_info) みたいな関数を作って、それを呼ぶようにする



        # ドキュメントIDの表示
        #frame_doc_id = tk.Frame(frame_bottom)
        #frame_doc_id.pack(anchor='w', fill='x')
        #self.doc_id_label = tk.Label(frame_doc_id, text="Document ID: ")
        #self.doc_id_label.pack(side='left')
        #self.doc_id_var = tk.StringVar(value="-")
        #self.doc_id_entry = tk.Entry(
        #    frame_doc_id,
        #    textvariable=self.doc_id_var,
        #    state="readonly",
        #    width=20,
        #    justify='left')
        #self.doc_id_entry.pack(side='left', fill='x', expand=True)

        # 埋め込みの表示
        #frame_embedding = tk.Frame(frame_bottom)
        #frame_embedding.pack(anchor='w', fill='x')
        #self.embedding_dimension_var = tk.StringVar(value="Embbeding (Array)")
        #self.embedding_label = tk.Label(frame_embedding, textvariable=self.embedding_dimension_var)
        #self.embedding_label.pack(side='left')
        #self.embedding_var = tk.StringVar(value="-")
        #self.embedding_entry = tk.Entry(
        #    frame_embedding,
        #    textvariable=self.embedding_var,
        #    state="readonly",
        #    width=20,
        #    justify='left')
        #self.embedding_entry.pack(side='left', fill='x', expand=True)

        ## テキスト長の表示
        #frame_result_length = tk.Frame(frame_bottom)
        #frame_result_length.pack(anchor='w')
        #self.result_length_label = tk.Label(frame_result_length, text="Result Length:")
        #self.result_length_label.pack(side='left')
        #self.result_length_var = tk.StringVar(value="0")
        #self.result_length_entry = tk.Entry(
        #    frame_result_length,
        #    textvariable=self.result_length_var,
        #    state="readonly",
        #    width=10,
        #    justify='left')
        #self.result_length_entry.pack(side='left', fill='x', expand=True)

        ## 結果表示用のテキストボックス
        #frame_search_result = tk.Frame(frame_bottom)
        #frame_search_result.pack(anchor='w', fill='both', expand=True)
        #self.result_text_label = tk.Label(frame_search_result, text="Search Result:")
        #self.result_text_label.pack(side='left', anchor='n')
        #self.result_text = tk.Text(frame_search_result, height=10, width=50, wrap='word')
        #self.result_text.pack(side='left', fill='both', expand=True)

        ## 縦スクロールバーの追加
        #self.scrollbar = tk.Scrollbar(self.result_text, command=self.result_text.yview)
        #self.scrollbar.pack(side='right', fill='y')

        ## テキストボックスにスクロールバーを設定
        #self.result_text.config(yscrollcommand=self.scrollbar.set)

        ## データが存在する場合は最初のドキュメントを表示
        #if len(doc_ids) > 0:
        #    self.entry.insert(0, "0")
        #    self.search_document()

    def open_chroma_database(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.db_path = directory_path
            self.db_label.config(text=f"Database File: {self.db_path}")
            # Chromaデータベースのロード
            self.load_chroma_db()

    def load_chroma_db(self):
        global chroma_db, data, doc_ids
        chroma_db = Chroma(
            collection_name="default",
            embedding_function=embeddings,
            persist_directory=self.db_path)
        data = chroma_db.get(
            include=["metadatas", "embeddings", "documents"])
        doc_ids = data["ids"]
        self.count_label.config(text=f"Total Documents: {len(doc_ids)}")
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