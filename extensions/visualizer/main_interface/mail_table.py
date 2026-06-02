import tkinter as tk
from tkinter import ttk


def build_mail_table(viewer):
    viewer.mail_panel = ttk.Frame(viewer.content, style="Panel.TFrame")
    viewer.mail_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    header = ttk.Frame(viewer.mail_panel, style="Panel.TFrame")
    header.pack(fill=tk.X, padx=18, pady=(16, 8))

    viewer.category_title_label = ttk.Label(header, text="ВЫБЕРИТЕ КАТЕГОРИЮ", style="Header.TLabel")
    viewer.category_title_label.pack(side=tk.LEFT)

    search_box = ttk.Frame(header, style="Panel.TFrame")
    search_box.pack(side=tk.RIGHT)

    viewer.search_entry = ttk.Entry(search_box, textvariable=viewer.search_var, width=34, style="Search.TEntry")
    viewer.search_entry.pack(side=tk.LEFT)

    viewer.filter_button = ttk.Button(search_box, text="⌕", style="Action.TButton", width=3)
    viewer.filter_button.pack(side=tk.LEFT, padx=(8, 0))

    table_frame = ttk.Frame(viewer.mail_panel, style="Panel.TFrame")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 16))

    columns = ("file", "subject", "sender", "attachment", "date")
    viewer.mail_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Mail.Treeview",
        selectmode="browse",
    )

    viewer.mail_tree.heading("file", text="Файл", command=lambda: viewer.sort_by_column("file_name"))
    viewer.mail_tree.heading("subject", text="Тема письма", command=lambda: viewer.sort_by_column("subject"))
    viewer.mail_tree.heading("sender", text="Отправитель", command=lambda: viewer.sort_by_column("sender"))
    viewer.mail_tree.heading("attachment", text="↗", command=lambda: viewer.sort_by_column("has_attachment"))
    viewer.mail_tree.heading("date", text="Дата и время", command=lambda: viewer.sort_by_column("date"))

    viewer.mail_tree.column("file", width=145, minwidth=120, anchor="w")
    viewer.mail_tree.column("subject", width=360, minwidth=220, anchor="w")
    viewer.mail_tree.column("sender", width=290, minwidth=200, anchor="w")
    viewer.mail_tree.column("attachment", width=60, minwidth=50, anchor="center")
    viewer.mail_tree.column("date", width=170, minwidth=140, anchor="w")
    viewer.mail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=viewer.mail_tree.yview, style="Dark.Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    viewer.mail_tree.configure(yscrollcommand=scrollbar.set)
    viewer.mail_tree.bind("<<TreeviewSelect>>", viewer.on_mail_select)


def render_mail_table(viewer):
    viewer.mail_tree.delete(*viewer.mail_tree.get_children())

    if not viewer.current_category:
        viewer.category_title_label.config(text="ВЫБЕРИТЕ КАТЕГОРИЮ")
        return

    title = f'{viewer.current_category["title"]} — {len(viewer.filtered_mails)} писем'
    viewer.category_title_label.config(text=title.upper())

    for index, mail in enumerate(viewer.filtered_mails):
        attachment = "↗" if mail["has_attachment"] else ""
        viewer.mail_tree.insert(
            "",
            tk.END,
            iid=str(index),
            values=(mail["file_name"], mail["subject"], mail["sender"], attachment, mail["date"]),
        )


def sort_by_column(viewer, column_name):
    if not viewer.filtered_mails:
        return

    if viewer.sort_column == column_name:
        viewer.sort_reverse = not viewer.sort_reverse
    else:
        viewer.sort_column = column_name
        viewer.sort_reverse = False

    viewer.filtered_mails.sort(
        key=lambda mail: str(mail.get(column_name, "")).lower(),
        reverse=viewer.sort_reverse,
    )

    render_mail_table(viewer)
    viewer.clear_details()
