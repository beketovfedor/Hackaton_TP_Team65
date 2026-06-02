import json
import sys
from pathlib import Path
from src.processing.parser import parse_file
from src.processing.cleaner import process_raw_email
from .theme import CATEGORY_ICONS

BASE_DIR = Path(__file__).resolve().parents[3]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

PROCESSED_DIR = BASE_DIR / "data" / "processed"
CATEGORIES_PATH = BASE_DIR / "data" / "config" / "categories.json"


def load_categories_config():
    if not CATEGORIES_PATH.exists():
        return {}

    with open(CATEGORIES_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("categories", {})


def find_category_by_folder(folder_name, categories_config):
    for category_name, category_data in categories_config.items():
        if category_data.get("folder") == folder_name:
            return category_name, category_data

    return folder_name, {
        "folder": folder_name,
        "title": folder_name,
        "priority": 0,
    }


def has_attachment(raw_text):
    if not raw_text:
        return False

    text = raw_text.lower()
    markers = [
        "вложение",
        "во вложении",
        "прикрепил",
        "прикрепляю",
        "attachment",
        ".pdf",
        ".docx",
        ".xlsx",
        ".png",
        ".jpg",
        "invoice",
        "contract",
        "screenshot",
    ]

    for marker in markers:
        if marker in text:
            return True

    return False


def get_file_size_kb(file_path):
    try:
        return round(file_path.stat().st_size / 1024, 1)
    except OSError:
        return 0


def get_mail_info(file_path, category_name, folder_name):
    raw_text = parse_file(str(file_path))

    if raw_text is None:
        return {
            "id": file_path.name,
            "file_name": file_path.name,
            "subject": "Не удалось прочитать файл",
            "sender": "",
            "to": "",
            "date": "",
            "body": "",
            "has_attachment": False,
            "size_kb": get_file_size_kb(file_path),
            "category": category_name,
            "folder": folder_name,
        }

    cleaned_mail = process_raw_email(raw_text, file_path.name)
    subject = cleaned_mail.get("subject", "") or cleaned_mail.get("mail_theme", "")

    return {
        "id": file_path.name,
        "file_name": cleaned_mail.get("mail_name", file_path.name),
        "subject": subject,
        "sender": cleaned_mail.get("from", ""),
        "to": cleaned_mail.get("to", ""),
        "date": cleaned_mail.get("date", ""),
        "body": cleaned_mail.get("mail_txt", ""),
        "has_attachment": has_attachment(raw_text),
        "size_kb": get_file_size_kb(file_path),
        "category": category_name,
        "folder": folder_name,
    }


def get_viewer_data():
    categories_config = load_categories_config()
    categories = []

    if not PROCESSED_DIR.exists():
        return categories

    for folder_path in sorted(PROCESSED_DIR.iterdir()):
        if not folder_path.is_dir():
            continue

        folder_name = folder_path.name
        category_name, category_data = find_category_by_folder(folder_name, categories_config)
        mails = []

        for file_path in sorted(folder_path.iterdir()):
            if file_path.is_file():
                mails.append(get_mail_info(file_path, category_name, folder_name))

        categories.append({
            "id": category_name,
            "folder": folder_name,
            "title": category_data.get("title", category_name),
            "priority": category_data.get("priority", 0),
            "icon": CATEGORY_ICONS.get(category_name, "□"),
            "count": len(mails),
            "mails": mails,
        })

    return categories
