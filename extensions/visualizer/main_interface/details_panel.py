import tkinter as tk
from tkinter import ttk

from . import actions
from .theme import COLORS


def build_details_panel(viewer):
    viewer.details_panel = ttk.Frame(viewer.content, style="Panel.TFrame", height=290)
    viewer.details_panel.pack(fill=tk.X, pady=(0, 0))
    viewer.details_panel.pack_propagate(False)

    header = ttk.Frame(viewer.details_panel, style="Panel.TFrame")
    header.pack(fill=tk.X, padx=18, pady=(14, 8))

    ttk.Label(header, text="ИНФОРМАЦИЯ О ПИСЬМЕ", style="Header.TLabel").pack(side=tk.LEFT)
    action_frame = ttk.Frame(header, style="Panel.TFrame")
    action_frame.pack(side=tk.RIGHT)

    buttons = [
        ("↗", lambda: actions.open_selected_mail_file(viewer)),
        ("⇩", lambda: actions.save_selected_mail_text(viewer)),
        ("⧉", lambda: actions.copy_selected_mail_info(viewer)),
        ("⋮", lambda: actions.show_selected_mail_info(viewer)),
    ]

    for text, command in buttons:
        ttk.Button(action_frame, text=text, width=3, style="Action.TButton", command=command).pack(side=tk.LEFT, padx=3)

    body = ttk.Frame(viewer.details_panel, style="Panel.TFrame")
    body.pack(fill=tk.X, padx=18, pady=(0, 14))

    build_file_card(viewer, body)
    build_meta_block(viewer, body)
    build_body_block(viewer, body)


def build_file_card(viewer, parent):
    viewer.file_card = tk.Frame(parent, bg=COLORS["panel_bg"], width=150, bd=0, highlightthickness=0)
    viewer.file_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
    viewer.file_card.pack_propagate(False)

    viewer.file_icon = tk.Label(
        viewer.file_card,
        text="📄\nTXT",
        bg=COLORS["purple"],
        fg=COLORS["text_main"],
        font=("Arial", 14, "bold"),
        width=6,
        height=4,
        bd=0,
        highlightthickness=0,
    )
    viewer.file_icon.pack(pady=(14, 8))

    viewer.file_name_label = tk.Label(
        viewer.file_card,
        text="",
        bg=COLORS["panel_bg"],
        fg=COLORS["text_main"],
        font=("Arial", 11, "bold"),
        bd=0,
        highlightthickness=0,
        wraplength=135,
    )
    viewer.file_name_label.pack()

    viewer.file_type_label = tk.Label(
        viewer.file_card,
        text="",
        bg=COLORS["panel_bg"],
        fg=COLORS["text_soft"],
        font=("Arial", 9),
        bd=0,
        highlightthickness=0,
    )
    viewer.file_type_label.pack(pady=(4, 0))

    viewer.file_size_label = tk.Label(
        viewer.file_card,
        text="",
        bg=COLORS["panel_bg"],
        fg=COLORS["text_muted"],
        font=("Arial", 9),
        bd=0,
        highlightthickness=0,
    )
    viewer.file_size_label.pack()


def build_meta_block(viewer, parent):
    viewer.meta_frame = ttk.Frame(parent, style="Panel.TFrame", width=390)
    viewer.meta_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
    viewer.meta_frame.pack_propagate(False)

    viewer.subject_value = create_meta_row(viewer, "Тема:")
    viewer.sender_value = create_meta_row(viewer, "Отправитель:")
    viewer.to_value = create_meta_row(viewer, "Получатель:")
    viewer.date_value = create_meta_row(viewer, "Дата:")


def create_meta_row(viewer, label):
    row = ttk.Frame(viewer.meta_frame, style="Panel.TFrame")
    row.pack(fill=tk.X, pady=7)

    tk.Label(
        row,
        text=label,
        bg=COLORS["panel_bg"],
        fg=COLORS["text_muted"],
        font=("Arial", 10),
        width=13,
        anchor="w",
        bd=0,
        highlightthickness=0,
    ).pack(side=tk.LEFT)

    value = tk.Label(
        row,
        text="",
        bg=COLORS["panel_bg"],
        fg=COLORS["text_main"],
        font=("Arial", 10),
        anchor="w",
        justify=tk.LEFT,
        bd=0,
        highlightthickness=0,
        wraplength=270,
    )
    value.pack(side=tk.LEFT, fill=tk.X, expand=True)
    return value


def build_body_block(viewer, parent):
    text_frame = ttk.Frame(parent, style="Panel.TFrame")
    text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    ttk.Label(
        text_frame,
        text="Текст письма:",
        background=COLORS["panel_bg"],
        foreground=COLORS["purple"],
        font=("Arial", 11),
    ).pack(anchor="w", pady=(0, 6))

    viewer.body_text = tk.Text(
        text_frame,
        height=9,
        bg="#0b1527",
        fg=COLORS["text_soft"],
        insertbackground=COLORS["text_main"],
        relief=tk.FLAT,
        wrap=tk.WORD,
        font=("Arial", 11),
        bd=0,
        highlightthickness=0,
    )
    viewer.body_text.pack(fill=tk.BOTH, expand=True)
    viewer.body_text.config(state=tk.DISABLED)


def render_mail_details(viewer, mail):
    viewer.selected_mail = mail
    viewer.file_name_label.config(text=mail["file_name"])
    viewer.file_type_label.config(text="Текстовый файл")
    viewer.file_size_label.config(text=f'{mail["size_kb"]} КБ')
    viewer.subject_value.config(text=mail["subject"])
    viewer.sender_value.config(text=mail["sender"])
    viewer.to_value.config(text=mail["to"])
    viewer.date_value.config(text=mail["date"])

    viewer.body_text.config(state=tk.NORMAL)
    viewer.body_text.delete("1.0", tk.END)
    viewer.body_text.insert(tk.END, mail["body"])
    viewer.body_text.config(state=tk.DISABLED)


def clear_details(viewer):
    viewer.selected_mail = None
    viewer.file_name_label.config(text="")
    viewer.file_type_label.config(text="")
    viewer.file_size_label.config(text="")
    viewer.subject_value.config(text="")
    viewer.sender_value.config(text="")
    viewer.to_value.config(text="")
    viewer.date_value.config(text="")
    viewer.body_text.config(state=tk.NORMAL)
    viewer.body_text.delete("1.0", tk.END)
    viewer.body_text.insert(tk.END, "Выберите письмо из таблицы.")
    viewer.body_text.config(state=tk.DISABLED)
