import platform
import tkinter as tk
from tkinter import ttk

from .data_provider import get_viewer_data
from .details_panel import build_details_panel, clear_details, render_mail_details
from .mail_table import build_mail_table, render_mail_table, sort_by_column
from .sidebar import build_sidebar, load_categories, sort_categories_by_column
from .styles import setup_styles
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
        self.root.geometry("1320x720")
        self.root.minsize(1100, 680)
        self.root.configure(bg=COLORS["window_bg"])

        if platform.system() == "Windows":
            try:
                self.root.state("zoomed")
            except tk.TclError:
                pass

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)

        setup_styles(self.root)
        self.build_interface()
        self.load_categories()

        if self.categories:
            self.select_category_by_index(0)

    def build_interface(self):
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        self.sidebar = ttk.Frame(self.main_frame, style="Panel.TFrame", width=360)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        self.sidebar.pack_propagate(False)

        self.content = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        build_sidebar(self)
        build_mail_table(self)
        build_details_panel(self)

    def load_categories(self):
        load_categories(self)

    def sort_categories_by_column(self, column_name):
        sort_categories_by_column(self, column_name)

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
        render_mail_table(self)

    def sort_by_column(self, column_name):
        sort_by_column(self, column_name)

    def on_mail_select(self, event):
        selected = self.mail_tree.selection()
        if not selected:
            return

        index = int(selected[0])
        if index >= len(self.filtered_mails):
            return

        self.render_mail_details(self.filtered_mails[index])

    def render_mail_details(self, mail):
        render_mail_details(self, mail)

    def clear_details(self):
        clear_details(self)

    def on_search(self, *args):
        if not self.current_category:
            return

        query = self.search_var.get().strip().lower()
        if not query:
            self.filtered_mails = list(self.current_mails)
        else:
            self.filtered_mails = []
            for mail in self.current_mails:
                text = " ".join([
                    mail["file_name"],
                    mail["subject"],
                    mail["sender"],
                    mail["to"],
                    mail["date"],
                    mail["body"],
                ]).lower()
                if query in text:
                    self.filtered_mails.append(mail)

        self.sort_column = None
        self.sort_reverse = False
        self.render_mail_table()
        self.clear_details()

    def run(self):
        self.root.mainloop()
