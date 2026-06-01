from pathlib import Path

from src.processing.parser import parse_file
from src.processing.cleaner import process_raw_email
from src.analyzer.classifier import MailClassifier
from src.analyzer.file_manager import FileManager


BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"


def sort_mails():
    if not INBOX_DIR.exists():
        print(f"Папка с письмами не найдена: {INBOX_DIR}")
        return

    classifier = MailClassifier()
    file_manager = FileManager()

    file_manager.create_category_folders(classifier.categories)

    total_files = 0
    sorted_files = 0
    unreadable_files = 0
    error_files = 0

    category_counter = {}

    for file_path in sorted(INBOX_DIR.iterdir()):
        if not file_path.is_file():
            continue

        total_files += 1

        try:
            raw_text = parse_file(str(file_path))

            if raw_text is None:
                classification_result = classifier.classify(None)
                unreadable_files += 1
            else:
                cleaned_mail = process_raw_email(raw_text, file_path.name)
                classification_result = classifier.classify(cleaned_mail)

            move_result = file_manager.move_file_to_category(
                file_path,
                classification_result
            )

            category = classification_result.get("category", "other")

            if category not in category_counter:
                category_counter[category] = 0

            category_counter[category] += 1

            if move_result["success"]:
                sorted_files += 1
                print(
                    f'{file_path.name} -> '
                    f'{classification_result["folder"]} '
                    f'[{classification_result["category"]}]'
                )
            else:
                error_files += 1
                print(f'Ошибка: {file_path.name} — {move_result["message"]}')

        except Exception as error:
            error_files += 1
            print(f"Ошибка при обработке файла {file_path.name}: {error}")

    print_summary(
        total_files,
        sorted_files,
        unreadable_files,
        error_files,
        category_counter
    )


def print_summary(total_files, sorted_files, unreadable_files, error_files, category_counter):
    print()
    print("ИТОГИ СОРТИРОВКИ")
    print("=" * 40)
    print(f"Всего файлов найдено: {total_files}")
    print(f"Файлов перемещено: {sorted_files}")
    print(f"Нечитаемых файлов: {unreadable_files}")
    print(f"Ошибок обработки: {error_files}")

    print()
    print("Распределение по категориям:")
    print("-" * 40)

    if not category_counter:
        print("Нет обработанных категорий.")
        return

    for category in sorted(category_counter):
        print(f"{category}: {category_counter[category]}")


if __name__ == "__main__":
    sort_mails()