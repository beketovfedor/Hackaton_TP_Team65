import os
import platform
import subprocess
from pathlib import Path
from tkinter import filedialog, messagebox


def get_selected_mail(viewer):
    if viewer.selected_mail is None:
        messagebox.showinfo("Письмо не выбрано", "Сначала выберите письмо из таблицы.")
        return None
    return viewer.selected_mail


def build_mail_text(mail):
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


def find_mail_file_path(mail):
    base_dir = Path(__file__).resolve().parents[3]
    processed_dir = base_dir / "data" / "processed"
    file_path = processed_dir / mail["folder"] / mail["file_name"]

    if file_path.exists():
        return file_path

    return None


def open_selected_mail_file(viewer):
    mail = get_selected_mail(viewer)
    if mail is None:
        return

    file_path = find_mail_file_path(mail)
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


def save_selected_mail_text(viewer):
    mail = get_selected_mail(viewer)
    if mail is None:
        return

    default_name = Path(mail["file_name"]).stem + "_export.txt"
    save_path = filedialog.asksaveasfilename(
        title="Сохранить текст письма",
        defaultextension=".txt",
        initialfile=default_name,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if not save_path:
        return

    try:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(build_mail_text(mail))
        messagebox.showinfo("Готово", "Текст письма сохранён.")
    except OSError as error:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{error}")


def copy_selected_mail_info(viewer):
    mail = get_selected_mail(viewer)
    if mail is None:
        return

    viewer.root.clipboard_clear()
    viewer.root.clipboard_append(build_mail_text(mail))
    messagebox.showinfo("Скопировано", "Информация о письме скопирована в буфер обмена.")


def show_selected_mail_info(viewer):
    mail = get_selected_mail(viewer)
    if mail is None:
        return

    info = (
        f'Файл: {mail["file_name"]}\n'
        f'Категория: {mail["category"]}\n'
        f'Папка: {mail["folder"]}\n'
        f'Размер: {mail["size_kb"]} КБ\n'
        f'Есть вложение: {"да" if mail["has_attachment"] else "нет"}'
    )
    messagebox.showinfo("Дополнительная информация", info)
