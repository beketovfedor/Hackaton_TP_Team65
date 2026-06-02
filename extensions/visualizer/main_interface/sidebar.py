import tkinter as tk
from tkinter import ttk

from .theme import COLORS


def build_sidebar(viewer):
    title = ttk.Label(viewer.sidebar, text="КАТЕГОРИИ", style="Header.TLabel")
    title.pack(anchor="w", padx=18, pady=(18, 12))

    viewer.category_tree = ttk.Treeview(
        viewer.sidebar,
        columns=("count",),
        show="tree headings",
        style="Category.Treeview",
        selectmode="browse",
    )

    viewer.category_tree.heading(
        "#0",
        text="Категория",
        command=lambda: viewer.sort_categories_by_column("title"),
    )
    viewer.category_tree.heading(
        "count",
        text="Писем",
        command=lambda: viewer.sort_categories_by_column("count"),
    )

    viewer.category_tree.column("#0", width=285, minwidth=250, stretch=True, anchor="w")
    viewer.category_tree.column("count", width=48, minwidth=45, stretch=False, anchor="center")
    viewer.category_tree.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
    viewer.category_tree.bind("<<TreeviewSelect>>", viewer.on_category_select)

    build_summary_card(viewer)


def build_summary_card(viewer):
    viewer.summary_frame = tk.Frame(viewer.sidebar, bg="#0f1f38", bd=0, highlightthickness=0)
    viewer.summary_frame.pack(fill=tk.X, padx=18, pady=(0, 18))

    viewer.summary_icon = tk.Label(
        viewer.summary_frame,
        text="▣",
        bg="#0f1f38",
        fg="#ffd84d",
        font=("Arial", 28),
        bd=0,
        highlightthickness=0,
    )
    viewer.summary_icon.pack(side=tk.LEFT, padx=14, pady=14)

    summary_text = tk.Frame(viewer.summary_frame, bg="#0f1f38", bd=0, highlightthickness=0)
    summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(
        summary_text,
        text="Найдено категорий",
        bg="#0f1f38",
        fg=COLORS["text_soft"],
        font=("Arial", 11),
        bd=0,
        highlightthickness=0,
    ).pack(anchor="w", pady=(14, 0))

    viewer.total_categories_label = tk.Label(
        summary_text,
        text="0",
        bg="#0f1f38",
        fg=COLORS["text_main"],
        font=("Arial", 25, "bold"),
        bd=0,
        highlightthickness=0,
    )
    viewer.total_categories_label.pack(anchor="w")


def load_categories(viewer):
    viewer.category_tree.delete(*viewer.category_tree.get_children())

    for index, category in enumerate(viewer.categories):
        text = f'{category["icon"]}  {category["title"]}'
        viewer.category_tree.insert("", tk.END, iid=str(index), text=text, values=(category["count"],))

    viewer.total_categories_label.config(text=str(len(viewer.categories)))


def sort_categories_by_column(viewer, column_name):
    if not viewer.categories:
        return

    selected_category_id = None
    if viewer.current_category is not None:
        selected_category_id = viewer.current_category.get("id")

    if viewer.category_sort_column == column_name:
        viewer.category_sort_reverse = not viewer.category_sort_reverse
    else:
        viewer.category_sort_column = column_name
        viewer.category_sort_reverse = False

    if column_name == "count":
        viewer.categories.sort(key=lambda category: category.get("count", 0), reverse=viewer.category_sort_reverse)
    else:
        viewer.categories.sort(
            key=lambda category: str(category.get(column_name, "")).lower(),
            reverse=viewer.category_sort_reverse,
        )

    load_categories(viewer)

    if selected_category_id is not None:
        for index, category in enumerate(viewer.categories):
            if category.get("id") == selected_category_id:
                viewer.select_category_by_index(index)
                return

    viewer.select_category_by_index(0)
