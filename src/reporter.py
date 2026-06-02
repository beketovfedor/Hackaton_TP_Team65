try:
    from src.visualizer import Visualizer
except ImportError:
    from visualizer import Visualizer


class Reporter:
    category_counter = {}
    keywords_counter = {}
    total_amount_of_letters = 0

    @staticmethod
    def add_category(category: str) -> None:
        Reporter.category_counter[category] = Reporter.category_counter.get(category, 0) + 1
        Reporter.total_amount_of_letters += 1

    @staticmethod
    def add_keywords(word_list: list) -> None:
        for word in set(word_list):
            Reporter.keywords_counter[word] = Reporter.keywords_counter.get(word, 0) + 1

    @staticmethod
    def create_report(filename: str = "report.txt") -> None:
        sorted_categories = sorted(Reporter.category_counter.items(), key=lambda item: (-item[1], item[0]))
        sorted_keywords = sorted(Reporter.keywords_counter.items(), key=lambda item: (-item[1], item[0]))

        with open(filename, "w", encoding="utf-8") as f:
            f.write("ОТЧЁТ О КЛАССИФИКАЦИИ ПИСЕМ\n")
            f.write(f"Всего обработано файлов: {Reporter.total_amount_of_letters}\n")
            f.write("--- Распределение по категориям ---\n")

            if not sorted_categories:
                f.write("No categories recorded.\n")
            else:
                for category, count in sorted_categories:
                    percent = (count / Reporter.total_amount_of_letters) * 100
                    f.write(f"{category}: {count} писем ({percent:5.1f}%)\n")

            f.write("\n--- Число уникальных писем с ключевыми словами ---\n")

            if not sorted_keywords:
                f.write("No keywords recorded.\n")
            else:
                for index, (keyword, count) in enumerate(sorted_keywords):
                    if index == 20:
                        break
                    percent = (count / Reporter.total_amount_of_letters) * 100
                    f.write(f"{keyword}: {count} писем ({percent:5.1f}%)\n")


if __name__ == "__main__":
    Reporter.add_category("news")
    Reporter.add_category("sports")
    Reporter.add_category("news")
    Reporter.add_keywords(["python", "code", "python", "data"])
    Reporter.create_report("test_report.txt")
    Visualizer.visualize_categories(Reporter.category_counter)
    Visualizer.visualize_keywords(Reporter.keywords_counter)
