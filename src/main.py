import sys
import argparse
from pathlib import Path
from src.processing.parser import parse_file
from src.processing.cleaner import process_raw_email
from src.analyzer.classifier import MailClassifier
from src.analyzer.file_manager import FileManager
from extensions.visualizer.main_interface.tk_viewer import MailViewer

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

INBOX_DIR = BASE_DIR / "data" / "inbox"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def sort_mails():
    if not INBOX_DIR.exists():
        print(f"Папка с письмами не найдена: {INBOX_DIR}")
        return {
            "total_files": 0,
            "sorted_files": 0,
            "unreadable_files": 0,
            "error_files": 0,
            "category_counter": {}
        }

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
            category_counter[category] = category_counter.get(category, 0) + 1
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

    result = {
        "total_files": total_files,
        "sorted_files": sorted_files,
        "unreadable_files": unreadable_files,
        "error_files": error_files,
        "category_counter": category_counter
    }

    print_summary(result)

    return result


def get_category_counter_from_processed():
    category_counter = {}

    if not PROCESSED_DIR.exists():
        return category_counter

    for folder_path in sorted(PROCESSED_DIR.iterdir()):
        if not folder_path.is_dir():
            continue
        files_count = 0
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                files_count += 1
        if files_count > 0:
            category_counter[folder_path.name] = files_count

    return category_counter


def print_summary(result):
    print()
    print("ИТОГИ СОРТИРОВКИ")
    print("=" * 40)
    print(f"Всего файлов найдено: {result['total_files']}")
    print(f"Файлов перемещено: {result['sorted_files']}")
    print(f"Нечитаемых файлов: {result['unreadable_files']}")
    print(f"Ошибок обработки: {result['error_files']}")

    print()
    print("Распределение по категориям:")
    print("-" * 40)

    category_counter = result["category_counter"]

    if not category_counter:
        print("Нет обработанных категорий.")
        return

    for category in sorted(category_counter):
        print(f"{category}: {category_counter[category]}")


def show_graphs(category_counter):
    if not category_counter:
        print("Нет данных для построения графиков.")
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Для отображения графиков установите matplotlib: pip install matplotlib")
        return
    categories = list(category_counter.keys())
    counts = list(category_counter.values())
    show_bar_chart(plt, categories, counts)
    show_pie_chart(plt, categories, counts)
    plt.show(block=False)


def show_bar_chart(plt, categories, counts):
    plt.figure(figsize=(12, 6))
    plt.bar(categories, counts)
    plt.title("Распределение писем по категориям")
    plt.xlabel("Категории")
    plt.ylabel("Количество писем")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()


def show_pie_chart(plt, categories, counts):
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Доля писем по категориям")
    plt.tight_layout()


def launch_visualizer():
    viewer = MailViewer()
    viewer.run()


def run_full_process():
    sort_result = sort_mails()
    category_counter = get_category_counter_from_processed()
    if not category_counter:
        category_counter = sort_result["category_counter"]
    show_graphs(category_counter)
    launch_visualizer()


def run_visualizer_only():
    launch_visualizer()


def run_graphs_only():
    category_counter = get_category_counter_from_processed()
    show_graphs(category_counter)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Автоматическая сортировка писем по категориям"
    )

    parser.add_argument(
        "--sort-only",
        action="store_true",
        help="Только распределить письма по папкам"
    )

    parser.add_argument(
        "--visualize-only",
        action="store_true",
        help="Только открыть визуализатор без сортировки"
    )

    parser.add_argument(
        "--graphs-only",
        action="store_true",
        help="Только показать графики по data/processed"
    )

    parser.add_argument(
        "--no-graphs",
        action="store_true",
        help="Запустить полный процесс без графиков"
    )

    parser.add_argument(
        "--no-visualizer",
        action="store_true",
        help="Запустить полный процесс без визуализатора"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.visualize_only:
        run_visualizer_only()
        return
    if args.graphs_only:
        run_graphs_only()
        return
    sort_result = sort_mails()
    if args.sort_only:
        return
    category_counter = get_category_counter_from_processed()
    if not category_counter:
        category_counter = sort_result["category_counter"]
    if not args.no_graphs:
        show_graphs(category_counter)
    if not args.no_visualizer:
        launch_visualizer()


if __name__ == "__main__":
    main()