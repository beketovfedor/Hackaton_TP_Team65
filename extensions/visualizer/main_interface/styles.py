import tkinter as tk
from tkinter import ttk

from .theme import COLORS


def setup_styles(root):
    style = ttk.Style(root)

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
        relief="flat",
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
        font=("Arial", 11),
    )
    style.configure(
        "Category.Treeview.Heading",
        background=COLORS["panel_header"],
        foreground=COLORS["text_muted"],
        font=("Arial", 10),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Category.Treeview",
        background=[("selected", COLORS["purple_dark"])],
        foreground=[("selected", COLORS["text_main"])],
    )

    style.configure(
        "Mail.Treeview",
        background=COLORS["panel_bg_2"],
        fieldbackground=COLORS["panel_bg_2"],
        foreground=COLORS["text_soft"],
        rowheight=30,
        borderwidth=0,
        relief="flat",
        font=("Arial", 10),
    )
    style.configure(
        "Mail.Treeview.Heading",
        background=COLORS["panel_header"],
        foreground=COLORS["text_muted"],
        font=("Arial", 10),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Mail.Treeview",
        background=[("selected", COLORS["purple_hover"])],
        foreground=[("selected", COLORS["text_main"])],
    )

    style.configure(
        "Dark.Vertical.TScrollbar",
        background=COLORS["panel_bg"],
        troughcolor=COLORS["window_bg"],
        bordercolor=COLORS["window_bg"],
        arrowcolor=COLORS["text_soft"],
        relief="flat",
    )

    style.configure(
        "Action.TButton",
        background="#111d31",
        foreground=COLORS["text_soft"],
        borderwidth=0,
        focusthickness=0,
        font=("Arial", 11),
    )
    style.map(
        "Action.TButton",
        background=[("active", COLORS["purple_dark"])],
        foreground=[("active", COLORS["text_main"])],
    )
