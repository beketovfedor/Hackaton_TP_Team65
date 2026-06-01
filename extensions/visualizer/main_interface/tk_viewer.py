import os
import platform
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox

from extensions.visualizer.main_interface.data_provider import get_viewer_data
from .theme import COLORS


class MailViewer:
    def __init__(self):
        self.categories = get_viewer_data()

        self.current_category = None
        self.current_mails = []
        self.filtered_mails = []

        self.selected_mail = None

        self.sort_column = None
        self.sort_reverse = False

        self.category_sort_column = None
        self.category_sort_reverse = False

        self.block_category_event = False

        self.root = tk.Tk()
        self.root.title("Распределение писем по категориям")
        self.root.geometry("1320x780")
        self.root.minsize(1500, 810)
        self.root.configure(bg=COLORS["window_bg"])

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)

        self.setup_styles()
        self.build_interface()
        self.load_categories()

        if self.categories:
            self.select_category_by_index(0)

    def setup_styles(self):
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Main.TFrame", background=COLORS["window_bg"], borderwidth=0, relief="flat")
        style.configure("Panel.TFrame", background=COLORS["panel_bg"], borderwidth=0, relief="flat")
        style.configure("Header.TLabel", background=COLORS["panel_bg"], foreground=COLORS["text_main"], font=("Arial", 13, "bold"))
        style.configure("Small.TLabel", background=COLORS["panel_bg"], foreground=COLORS["text_muted"], font=("Arial", 10))
        style.configure("Info.TLabel", background=COLORS["panel_bg"], foreground=COLORS["text_soft"], font=("Arial", 11))

        style.configure(
            "Search.TEntry",
            fieldbackground="#0b1527",
            background="#0b1527",
            foreground=COLORS["text_main"],
            borderwidth=0,
            relief="flat"
        )

        style.layout("Category.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.layout("Mail.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        style.configure(
            "Category.Treeview",
            background=COLORS["panel_bg"],
            fieldbackground=COLORS["panel_bg"],
            foreground=COLORS["text_soft"],
            rowheight=38,
            borderwidth=0,
            relief="flat",
            font=("Arial", 11)
        )

        style.configure(
            "Category.Treeview.Heading",
            background=COLORS["panel_header"],
            foreground=COLORS["text_muted"],
            font=("Arial", 10),
            relief="flat",
            borderwidth=0
        )

        style.map(
            "Category.Treeview",
            background=[("selected", COLORS["purple_dark"])],
            foreground=[("selected", COLORS["text_main"])]
        )

        style.configure(
            "Mail.Treeview",
            background=COLORS["panel_bg_2"],
            fieldbackground=COLORS["panel_bg_2"],
            foreground=COLORS["text_soft"],
            rowheight=30,
            borderwidth=0,
            relief="flat",
            font=("Arial", 10)
        )

        style.configure(
            "Mail.Treeview.Heading",
            background=COLORS["panel_header"],
            foreground=COLORS["text_muted"],
            font=("Arial", 10),
            relief="flat",
            borderwidth=0
        )

        style.map(
            "Mail.Treeview",
            background=[("selected", COLORS["purple_hover"])],
            foreground=[("selected", COLORS["text_main"])]
        )

        style.configure(
            "Dark.Vertical.TScrollbar",
            background=COLORS["panel_bg"],
            troughcolor=COLORS["window_bg"],
            bordercolor=COLORS["window_bg"],
            arrowcolor=COLORS["text_soft"],
            relief="flat"
        )

        style.configure(
            "Action.TButton",
            background="#111d31",
            foreground=COLORS["text_soft"],
            borderwidth=0,
            focusthickness=0,
            font=("Arial", 11)
        )

        style.map(
            "Action.TButton",
            background=[("active", COLORS["purple_dark"])],
            foreground=[("active", COLORS["text_main"])]
        )

    def build_interface(self):
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        self.sidebar = ttk.Frame(self.main_frame, style="Panel.TFrame", width=360)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        self.sidebar.pack_propagate(False)

        self.content = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_sidebar()
        self.build_mail_table()
        self.build_details_panel()

    def build_sidebar(self):
        title = ttk.Label(self.sidebar, text="КАТЕГОРИИ", style="Header.TLabel")
        title.pack(anchor="w", padx=18, pady=(18, 12))

        self.category_tree = ttk.Treeview(
            self.sidebar,
            columns=("count",),
            show="tree headings",
            style="Category.Treeview",
            selectmode="browse"
        )

        self.category_tree.heading(
            "#0",
            text="Категория",
            command=lambda: self.sort_categories_by_column("title")
        )

        self.category_tree.heading(
            "count",
            text="Писем",
            command=lambda: self.sort_categories_by_column("count")
        )
        self.category_tree.column("#0", width=285, minwidth=250, stretch=True, anchor="w")
        self.category_tree.column("count", width=48, minwidth=45, stretch=False, anchor="center")

        self.category_tree.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.category_tree.bind("<<TreeviewSelect>>", self.on_category_select)

        self.summary_frame = tk.Frame(self.sidebar, bg="#0f1f38", bd=0, highlightthickness=0)
        self.summary_frame.pack(fill=tk.X, padx=18, pady=(0, 18))

        self.summary_icon = tk.Label(
            self.summary_frame,
            text="▣",
            bg="#0f1f38",
            fg="#ffd84d",
            font=("Arial", 28),
            bd=0,
            highlightthickness=0
        )
        self.summary_icon.pack(side=tk.LEFT, padx=14, pady=14)

        summary_text = tk.Frame(self.summary_frame, bg="#0f1f38", bd=0, highlightthickness=0)
        summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            summary_text,
            text="Найдено категорий",
            bg="#0f1f38",
            fg=COLORS["text_soft"],
            font=("Arial", 11),
            bd=0,
            highlightthickness=0
        ).pack(anchor="w", pady=(14, 0))

        self.total_categories_label = tk.Label(
            summary_text,
            text="0",
            bg="#0f1f38",
            fg=COLORS["text_main"],
            font=("Arial", 25, "bold"),
            bd=0,
            highlightthickness=0
        )
        self.total_categories_label.pack(anchor="w")

    def build_mail_table(self):
        self.mail_panel = ttk.Frame(self.content, style="Panel.TFrame")
        self.mail_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        header = ttk.Frame(self.mail_panel, style="Panel.TFrame")
        header.pack(fill=tk.X, padx=18, pady=(16, 8))

        self.category_title_label = ttk.Label(header, text="ВЫБЕРИТЕ КАТЕГОРИЮ", style="Header.TLabel")
        self.category_title_label.pack(side=tk.LEFT)

        search_box = ttk.Frame(header, style="Panel.TFrame")
        search_box.pack(side=tk.RIGHT)

        self.search_entry = ttk.Entry(search_box, textvariable=self.search_var, width=34, style="Search.TEntry")
        self.search_entry.pack(side=tk.LEFT)

        self.filter_button = ttk.Button(search_box, text="⌕", style="Action.TButton", width=3)
        self.filter_button.pack(side=tk.LEFT, padx=(8, 0))

        table_frame = ttk.Frame(self.mail_panel, style="Panel.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 16))

        columns = ("file", "subject", "sender", "attachment", "date")

        self.mail_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Mail.Treeview",
            selectmode="browse"
        )

        self.mail_tree.heading("file", text="Файл", command=lambda: self.sort_by_column("file_name"))
        self.mail_tree.heading("subject", text="Тема письма", command=lambda: self.sort_by_column("subject"))
        self.mail_tree.heading("sender", text="Отправитель", command=lambda: self.sort_by_column("sender"))
        self.mail_tree.heading("attachment", text="↗", command=lambda: self.sort_by_column("has_attachment"))
        self.mail_tree.heading("date", text="Дата и время", command=lambda: self.sort_by_column("date"))

        self.mail_tree.column("file", width=145, minwidth=120, anchor="w")
        self.mail_tree.column("subject", width=360, minwidth=220, anchor="w")
        self.mail_tree.column("sender", width=290, minwidth=200, anchor="w")
        self.mail_tree.column("attachment", width=60, minwidth=50, anchor="center")
        self.mail_tree.column("date", width=170, minwidth=140, anchor="w")

        self.mail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.mail_tree.yview, style="Dark.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.mail_tree.configure(yscrollcommand=scrollbar.set)
        self.mail_tree.bind("<<TreeviewSelect>>", self.on_mail_select)

    def build_details_panel(self):
        self.details_panel = ttk.Frame(self.content, style="Panel.TFrame", height=290)
        self.details_panel.pack(fill=tk.X, pady=(0, 0))
        self.details_panel.pack_propagate(False)

        header = ttk.Frame(self.details_panel, style="Panel.TFrame")
        header.pack(fill=tk.X, padx=18, pady=(14, 8))

        ttk.Label(header, text="ИНФОРМАЦИЯ О ПИСЬМЕ", style="Header.TLabel").pack(side=tk.LEFT)

        actions = ttk.Frame(header, style="Panel.TFrame")
        actions.pack(side=tk.RIGHT)

        buttons = [
            ("↗", self.open_selected_mail_file),
            ("⇩", self.save_selected_mail_text),
            ("⧉", self.copy_selected_mail_info),
            ("⋮", self.show_selected_mail_info)
        ]

        for text, command in buttons:
            ttk.Button(actions, text=text, width=3, style="Action.TButton", command=command).pack(side=tk.LEFT, padx=3)

        body = ttk.Frame(self.details_panel, style="Panel.TFrame")
        body.pack(fill=tk.X, padx=18, pady=(0, 14))

        self.file_card = tk.Frame(body, bg=COLORS["panel_bg"], width=150, bd=0, highlightthickness=0)
        self.file_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.file_card.pack_propagate(False)

        self.file_icon = tk.Label(
            self.file_card,
            text="📄\nTXT",
            bg=COLORS["purple"],
            fg=COLORS["text_main"],
            font=("Arial", 14, "bold"),
            width=6,
            height=4,
            bd=0,
            highlightthickness=0
        )
        self.file_icon.pack(pady=(14, 8))

        self.file_name_label = tk.Label(
            self.file_card,
            text="",
            bg=COLORS["panel_bg"],
            fg=COLORS["text_main"],
            font=("Arial", 11, "bold"),
            bd=0,
            highlightthickness=0,
            wraplength=135
        )
        self.file_name_label.pack()

        self.file_type_label = tk.Label(
            self.file_card,
            text="",
            bg=COLORS["panel_bg"],
            fg=COLORS["text_soft"],
            font=("Arial", 9),
            bd=0,
            highlightthickness=0
        )
        self.file_type_label.pack(pady=(4, 0))

        self.file_size_label = tk.Label(
            self.file_card,
            text="",
            bg=COLORS["panel_bg"],
            fg=COLORS["text_muted"],
            font=("Arial", 9),
            bd=0,
            highlightthickness=0
        )
        self.file_size_label.pack()

        self.meta_frame = ttk.Frame(body, style="Panel.TFrame", width=390)
        self.meta_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.meta_frame.pack_propagate(False)

        self.subject_value = self.create_meta_row("Тема:")
        self.sender_value = self.create_meta_row("Отправитель:")
        self.to_value = self.create_meta_row("Получатель:")
        self.date_value = self.create_meta_row("Дата:")

        text_frame = ttk.Frame(body, style="Panel.TFrame")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(
            text_frame,
            text="Текст письма:",
            background=COLORS["panel_bg"],
            foreground=COLORS["purple"],
            font=("Arial", 11)
        ).pack(anchor="w", pady=(0, 6))

        self.body_text = tk.Text(
            text_frame,
            height=9,
            bg="#0b1527",
            fg=COLORS["text_soft"],
            insertbackground=COLORS["text_main"],
            relief=tk.FLAT,
            wrap=tk.WORD,
            font=("Arial", 11),
            bd=0,
            highlightthickness=0
        )
        self.body_text.pack(fill=tk.BOTH, expand=True)
        self.body_text.config(state=tk.DISABLED)

    def create_meta_row(self, label):
        row = ttk.Frame(self.meta_frame, style="Panel.TFrame")
        row.pack(fill=tk.X, pady=7)

        label_widget = tk.Label(
            row,
            text=label,
            bg=COLORS["panel_bg"],
            fg=COLORS["text_muted"],
            font=("Arial", 10),
            width=13,
            anchor="w",
            bd=0,
            highlightthickness=0
        )
        label_widget.pack(side=tk.LEFT)

        value_widget = tk.Label(
            row,
            text="",
            bg=COLORS["panel_bg"],
            fg=COLORS["text_main"],
            font=("Arial", 10),
            anchor="w",
            justify=tk.LEFT,
            bd=0,
            highlightthickness=0,
            wraplength=270
        )
        value_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

        return value_widget

    def sort_categories_by_column(self, column_name):
        if not self.categories:
            return

        selected_category_id = None

        if self.current_category is not None:
            selected_category_id = self.current_category.get("id")

        if self.category_sort_column == column_name:
            self.category_sort_reverse = not self.category_sort_reverse
        else:
            self.category_sort_column = column_name
            self.category_sort_reverse = False

        if column_name == "count":
            self.categories.sort(
                key=lambda category: category.get("count", 0),
                reverse=self.category_sort_reverse
            )
        else:
            self.categories.sort(
                key=lambda category: str(category.get(column_name, "")).lower(),
                reverse=self.category_sort_reverse
            )

        self.load_categories()

        if selected_category_id is not None:
            for index, category in enumerate(self.categories):
                if category.get("id") == selected_category_id:
                    self.select_category_by_index(index)
                    return

        self.select_category_by_index(0)

    def load_categories(self):
        self.category_tree.delete(*self.category_tree.get_children())

        for index, category in enumerate(self.categories):
            text = f'{category["icon"]}  {category["title"]}'

            self.category_tree.insert(
                "",
                tk.END,
                iid=str(index),
                text=text,
                values=(category["count"],)
            )

        self.total_categories_label.config(text=str(len(self.categories)))

    def select_category_by_index(self, index, update_tree_selection=True):
        if not self.categories:
            return

        if index < 0 or index >= len(self.categories):
            return

        if update_tree_selection:
            self.block_category_event = True
            self.category_tree.selection_set(str(index))
            self.category_tree.focus(str(index))
            self.block_category_event = False

        self.current_category = self.categories[index]
        self.current_mails = self.current_category["mails"]
        self.filtered_mails = list(self.current_mails)

        self.sort_column = None
        self.sort_reverse = False

        self.render_mail_table()
        self.clear_details()

    def on_category_select(self, event):
        if self.block_category_event:
            return

        selected = self.category_tree.selection()

        if not selected:
            return

        index = int(selected[0])
        self.select_category_by_index(index, update_tree_selection=False)

    def render_mail_table(self):
        self.mail_tree.delete(*self.mail_tree.get_children())

        if not self.current_category:
            self.category_title_label.config(text="ВЫБЕРИТЕ КАТЕГОРИЮ")
            return

        title = f'{self.current_category["title"]} — {len(self.filtered_mails)} писем'
        self.category_title_label.config(text=title.upper())

        for index, mail in enumerate(self.filtered_mails):
            attachment = "↗" if mail["has_attachment"] else ""

            self.mail_tree.insert(
                "",
                tk.END,
                iid=str(index),
                values=(
                    mail["file_name"],
                    mail["subject"],
                    mail["sender"],
                    attachment,
                    mail["date"]
                )
            )

    def on_mail_select(self, event):
        selected = self.mail_tree.selection()

        if not selected:
            return

        index = int(selected[0])

        if index >= len(self.filtered_mails):
            return

        mail = self.filtered_mails[index]
        self.render_mail_details(mail)

    def render_mail_details(self, mail):
        self.selected_mail = mail

        self.file_name_label.config(text=mail["file_name"])
        self.file_type_label.config(text="Текстовый файл")
        self.file_size_label.config(text=f'{mail["size_kb"]} КБ')

        self.subject_value.config(text=mail["subject"])
        self.sender_value.config(text=mail["sender"])
        self.to_value.config(text=mail["to"])
        self.date_value.config(text=mail["date"])

        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert(tk.END, mail["body"])
        self.body_text.config(state=tk.DISABLED)

    def clear_details(self):
        self.selected_mail = None

        self.file_name_label.config(text="")
        self.file_type_label.config(text="")
        self.file_size_label.config(text="")

        self.subject_value.config(text="")
        self.sender_value.config(text="")
        self.to_value.config(text="")
        self.date_value.config(text="")

        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert(tk.END, "Выберите письмо из таблицы.")
        self.body_text.config(state=tk.DISABLED)

    def on_search(self, *args):
        if not self.current_category:
            return

        query = self.search_var.get().strip().lower()

        if not query:
            self.filtered_mails = list(self.current_mails)
        else:
            result = []

            for mail in self.current_mails:
                text = " ".join([
                    mail["file_name"],
                    mail["subject"],
                    mail["sender"],
                    mail["to"],
                    mail["date"],
                    mail["body"]
                ]).lower()

                if query in text:
                    result.append(mail)

            self.filtered_mails = result

        self.sort_column = None
        self.sort_reverse = False

        self.render_mail_table()
        self.clear_details()

    def sort_by_column(self, column_name):
        if not self.filtered_mails:
            return

        if self.sort_column == column_name:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column_name
            self.sort_reverse = False

        self.filtered_mails.sort(
            key=lambda mail: str(mail.get(column_name, "")).lower(),
            reverse=self.sort_reverse
        )

        self.render_mail_table()
        self.clear_details()

    def get_selected_mail_data(self):
        if self.selected_mail is None:
            messagebox.showinfo("Письмо не выбрано", "Сначала выберите письмо из таблицы.")
            return None

        return self.selected_mail

    def open_selected_mail_file(self):
        mail = self.get_selected_mail_data()

        if mail is None:
            return

        file_path = self.find_mail_file_path(mail)

        if file_path is None:
            messagebox.showerror("Ошибка", "Файл письма не найден.")
            return

        try:
            system_name = platform.system()

            if system_name == "Windows":
                os.startfile(file_path)
            elif system_name == "Darwin":
                subprocess.run(["open", str(file_path)], check=False)
            else:
                subprocess.run(["xdg-open", str(file_path)], check=False)

        except OSError as error:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{error}")

    def save_selected_mail_text(self):
        mail = self.get_selected_mail_data()

        if mail is None:
            return

        default_name = Path(mail["file_name"]).stem + "_export.txt"

        save_path = filedialog.asksaveasfilename(
            title="Сохранить текст письма",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not save_path:
            return

        text = self.build_mail_text(mail)

        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(text)

            messagebox.showinfo("Готово", "Текст письма сохранён.")

        except OSError as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{error}")

    def copy_selected_mail_info(self):
        mail = self.get_selected_mail_data()

        if mail is None:
            return

        text = self.build_mail_text(mail)

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        messagebox.showinfo("Скопировано", "Информация о письме скопирована в буфер обмена.")

    def show_selected_mail_info(self):
        mail = self.get_selected_mail_data()

        if mail is None:
            return

        info = (
            f'Файл: {mail["file_name"]}\n'
            f'Категория: {mail["category"]}\n'
            f'Размер: {mail["size_kb"]} КБ\n'
            f'Есть вложение: {"да" if mail["has_attachment"] else "нет"}'
        )

        messagebox.showinfo("Дополнительная информация", info)

    def build_mail_text(self, mail):
        return (
            f'Файл: {mail["file_name"]}\n'
            f'Тема: {mail["subject"]}\n'
            f'Отправитель: {mail["sender"]}\n'
            f'Получатель: {mail["to"]}\n'
            f'Дата: {mail["date"]}\n'
            f'Категория: {mail["category"]}\n'
            f'Папка: {mail["folder"]}\n'
            f'Размер: {mail["size_kb"]} КБ\n\n'
            f'Текст письма:\n{mail["body"]}'
        )

    def find_mail_file_path(self, mail):
        base_dir = Path(__file__).resolve().parents[2]
        processed_dir = base_dir / "data" / "processed"

        file_path = processed_dir / mail["folder"] / mail["file_name"]

        if file_path.exists():
            return file_path

        return None

    def run(self):
        self.root.mainloop()
